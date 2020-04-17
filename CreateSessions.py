'''
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on May 25, 2016

@author: shurrey
'''

import sys
import os
import getopt
import datetime
import uuid
import logging
import logging.config
from logging.config import dictConfig
import csv
import click
import re

# Import Config
import Config

# Import Controllers
from controllers import AuthController
from controllers import UserController
from controllers import SessionController
from controllers import ContextController
from controllers import EmailController

# Import Models
from models import User
from models import Session
from models import Context
from models import EmailTemplate

def preflight(datadir,COURSES,USERS):
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists('logs'):
        os.makedirs('logs')

    if not os.path.exists('Config.py'):
        print("Please copy the ConfigTemplate.py file to Config.py and configure the app.")
        sys.exit()

    if not os.path.exists(datadir):
        print("Specified data dir " + datadir + " does not exist.")
        sys.exit()

    if COURSES:
        if not os.path.exists(datadir + '/course.csv'):
            print("Course data file " + datadir + "/course.csv does not exist.")
            sys.exit()

    if USERS:
        if not os.path.exists(datadir + '/student.csv'):
            print("Student data file " + datadir + "/student.csv does not exist.")
            sys.exit()

        if not os.path.exists(datadir + '/enrollment.csv'):
            print("Enrollment data file " + datadir + "/enrollment.csv does not exist.")
            sys.exit()
    

def validate_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex,email):
        return True
    
    return False

@click.command()
@click.option('--datadir', '-d', default='data', help='The data directory. Defaults to data in this project')
@click.option('--courses', '-c',  is_flag=True, default=False, help='Only create courses, teacher accounts, and moderator logins')
@click.option('--users', '-u',  is_flag=True, default=False, help='Only create student accounts')
def main(datadir,courses,users):

    COURSES = False
    USERS = False

    if not courses and not users:
        COURSES = True
        USERS = True
    else:
        if courses:
            COURSES = True
        if users:
            USERS = True

    preflight(datadir,COURSES,USERS)

    try:
        dictConfig(Config.logging)
        logger = logging.getLogger('main')
    except KeyError:
        print("Invalid configuration in Config.py: logging missing")
        sys.exit()

    logger.debug("datadir: " + datadir + ", COURSES: " + str(COURSES) + ", USERS: " + str(USERS))

    try:
        if Config.collab['verify_certs'] == 'True':
            VERIFY_CERTS = True
        else:
            VERIFY_CERTS = False
    except KeyError:
        errMsg = "Invalid configuration in Config.py: collab.verify_certs missing."
        print(errMsg)
        logger.error(errMsg)
        sys.exit()

    try:
        emlCtrl = EmailController.EmailController(Config.email)
    except KeyError:
        errMsg = "Invalid configuration in Config.py: email missing"
        print(errMsg)
        logger.error(errMsg)
        sys.exit()
    
    logger.info("Starting bulk creation process")

    try:
        authorized_session = AuthController.AuthController(Config.collab['collab_base_url'],Config.collab['collab_key'],Config.collab['collab_secret'],VERIFY_CERTS)
        authorized_session.setToken()
    except KeyError:
        errMsg = "Invalid configuration in Config.py: collab settings missing or incomplete"
        print(errMsg)
        logger.error(errMsg)
        sys.exit()

    ctxDict = {}
    usrDict = {}
    sesDict = {}

    try:
        ctxCtrl = ContextController.ContextController(Config.collab['collab_base_url'], authorized_session, VERIFY_CERTS)
        usrCtrl = UserController.UserController(Config.collab['collab_base_url'], authorized_session, VERIFY_CERTS)
        sesCtrl = SessionController.SessionController(Config.collab['collab_base_url'], authorized_session, VERIFY_CERTS)
    except KeyError:
        errMsg = "Invalid configuration in Config.py: collab settings missing or incomplete"
        print(errMsg)
        logger.error(errMsg)
        sys.exit()

    try:
        session_config = Config.session_settings
    except KeyError:
        errMsg = "Invalid configuration in Config.py: session settings missing"
        print(errMsg)
        logger.error(errMsg)
        sys.exit()

    if COURSES:
        with open(datadir + '/course.csv', newline='') as csvfile:
                courses = csv.reader(csvfile, delimiter=',', quotechar='"')

                next(courses)

                for course in courses:

                    crsId = course[0]
                    crsName = course[1]
                    insId = course[2]
                    insName = course[3]
                    insEmail = course[4]

                    if insEmail is None or insEmail == "" or validate_email(insEmail) == False:
                        logger.error("Instructor " + insName + " does not have a valid email address")
                        continue

                    logger.debug(crsId + ',' + crsName + ',' + insId + ',' + insName + ',' + insEmail)
                    

                    ctxId = ctxCtrl.getContext(crsName)

                    if ctxId['contextId'] is None:
                        ctx = Context.Context(crsName,crsName,crsName,crsId)
                        ctxres = ctxCtrl.createContext(ctx.getContextJson())

                        for k in ctxres:
                            result = k
                            break

                        if result == '200':
                            ctxId = { 'contextId' :  ctxres[result]}
                        else:
                            logger.error("Error creating context for course " + crsName + ", " + result + ": " + ctxres[result])
                            continue

                    logger.debug(ctxId['contextId'])

                    ctxDict[crsId] = ctxId['contextId']

                    ses = Session.Session(crsName, crsName, str(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")), None, session_config)
                    sesres = sesCtrl.createSession(ses.getSessionJson())

                    logger.debug(ses.getSessionJson())

                    for k in sesres:
                        result = k
                        break

                    if result == '200':
                        ses.setId(sesres[result])
                        logger.info("Session: " + ses.getId() + ", CREATED, for course " + crsName)
                    else:
                        logger.error("Error creating session for course " + crsName + ", " + result + ": " + sesres[result])
                        continue
                    
                    sesDict[crsId] = ses

                    if ctxCtrl.assignSessionToContext(ctxId['contextId'],ses.getId()) == False:
                        logger.error("Error assing session to context for course " + crsName + ", session: " + ses.getId() + ", context: " + ctxId['contextId'])
                        continue

                    teacher = User.User(insName,insId,insEmail)

                    teacherres = usrCtrl.createUser(teacher.getUserJson())

                    for k in teacherres:
                        result = k
                        break

                    if result == '200':
                        teacher.setId(teacherres[result])
                    else:
                        logger.error("Error creating user " + insName + " for course " + crsName + ", " + result + ": " + teacherres[result])
                        continue

                    logger.debug(teacher.getUserJson())
                    usrDict[insId] = teacher

                    urlres = sesCtrl.enrollUser(ses.getId(),teacher.getId(),'moderator')

                    for k in urlres:
                        result = k
                        break

                    if result == '200':
                        teacherUrl = urlres[result]
                    else:
                        logger.error("Error creating enrollment " + insName + " for course " + crsName + ", " + result + ": " + urlres[result])
                        continue

                    # TODO send email here
                    variables = {}
                    variables['insName'] = teacher.getDisplayName()
                    variables['clsName'] = ses.getName()
                    variables['link'] = teacherUrl
                    teacher_email_html = EmailTemplate.EmailTemplate('teacher-email-html', variables, True)

                    logger.debug(teacher_email_html.render())
                    
                    emlCtrl.sendmail(insEmail,teacher_email_html)

                    logger.info("Session link: " + teacherUrl + ", to User: " + insEmail + ", SENT for course " + crsName)

    if USERS:
        with open(datadir + '/student.csv', newline='') as csvfile:
                users = csv.reader(csvfile, delimiter=',', quotechar='|')

                next(users)

                for user in users:
                    logger.debug('Students: ' + str(user))

                    studentId = user[0]
                    studentName = user[1]
                    studentEmail = user[2]

                    if studentEmail is None or studentEmail == "" or validate_email(studentEmail) == False:
                        logger.error("Instructor " + insName + " does not have a valid email address")
                        continue

                    student = User.User(studentName,studentId,studentEmail)

                    studentres = usrCtrl.createUser(student.getUserJson())

                    for k in studentres:
                        result = k
                        break

                    if result == '200':
                        student.setId(studentres[result])
                    else:
                        logger.error("Error creating user " + studentName + ", " + result + ": " + teacherres[result])
                        continue

                    logger.debug(student.getUserJson())
                    usrDict[studentId] = student

        with open(datadir + '/enrollment.csv', newline='') as csvfile:
                enrollments = csv.reader(csvfile, delimiter=',', quotechar='|')

                next(enrollments)

                for enrollment in enrollments:
                    logger.debug('Enrollments: ' + str(enrollment))

                    courseId = enrollment[0]
                    studentId = enrollment[1]

                    try:
                        session = sesDict[courseId]
                    except KeyError:
                        logger.error("courseId " + courseId + " not found")
                        continue

                    try:
                        user = usrDict[studentId]
                    except KeyError:
                        logger.error("studentId " + studentId + " not found")
                        continue

                    urlres = sesCtrl.enrollUser(session.getId(),user.getId(),'participant')

                    for k in urlres:
                        result = k
                        break

                    if result == '200':
                        studentUrl = urlres[result]
                    else:
                        logger.error("Error creating enrollment " + user.getName() + " for course " + session.getName() + ", " + result + ": " + urlres[result])
                        continue


                    # TODO send email
                    variables = {}
                    variables['studentName'] = user.getDisplayName()
                    variables['clsName'] = session.getName()
                    variables['link'] = studentUrl
                    
                    student_email_html = EmailTemplate.EmailTemplate('student-email-html', variables, True)

                    logger.debug(student_email_html.render())
                    
                    emlCtrl.sendmail(user.getEmail(), student_email_html)

                    logger.info("Session link: " + studentUrl + ", to User: " + user.getEmail() + ", SENT for course " + session.getName())

    logger.info("Bulk creation processing complete")
        
if __name__ == "__main__":

    main()
    