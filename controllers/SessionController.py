
"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on May 25, 2016

@author: shurrey

"""

import json
import requests
import time
import jwt
import datetime
import ssl
import sys
import logging

class SessionController():

    def __init__(self, target_url, auth, verify_certs):
        self.target_url = target_url
        self.auth = auth
        self.verify_certs = verify_certs

        self.logger = logging.getLogger(name='sessions')

    def getSessionId(self):
        return self.SESSION_ID
    
    def getGuestUrl(self):
        return self.GUEST_URL
    
    def getModUrl(self):
        return self.MODERATOR_URL

    def createSession(self, payload):
        
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.auth.getToken()
        
        r = requests.post("https://" + self.target_url + '/sessions', headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=payload, verify=self.verify_certs)
        
        if r.status_code == 200:
            res = json.loads(r.text)
            self.logger.debug("Session: " + json.dumps(res,indent=4, separators=(',', ': ')))
            self.SESSION_ID = res['id']
            return({str(r.status_code) : self.SESSION_ID})
        else:
            self.logger.debug("Sessions.createSession ERROR: " + str(r))
            return({str(r.status_code) : r.text})

    def patchSession(self):
        #4b73a112a0914ed1a7fba0433c9c7e92
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.auth.getToken()

        payload = {
            "openChair": "true"
        }
        
        r = requests.patch("https://" + self.target_url + '/sessions/644472c8132c45bea1cade2ea1696fac', headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=payload, verify=self.verify_certs)
        
        if r.status_code == 200:
            res = json.loads(r.text)
            self.logger.debug("Session: " + json.dumps(res,indent=4, separators=(',', ': ')))
            self.SESSION_ID = res['id']
            return({str(r.status_code) : self.SESSION_ID})
        else:
            self.logger.debug("Sessions.createSession ERROR: " + str(r))
            return({str(r.status_code) : r.text})

    def enrollUser(self, session_id, userId, role):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.auth.getToken()

        editingPermission = 'reader'

        if role == 'moderator':
            editingPermission = 'writer'
        
        payload = {
            'launchingRole' : role,
            'editingPermission': editingPermission,
            'userId' : userId
        }

        self.logger.debug(payload)
        
        r = requests.post("https://" + self.target_url + '/sessions/' + session_id + "/enrollments", headers={'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json'}, json=payload, verify=self.verify_certs)
        
        if r.status_code == 200:
            res = json.loads(r.text)
            self.logger.debug(json.dumps(res,indent=4, separators=(',', ': ')))
            url = res['permanentUrl']
            return({str(r.status_code) : url})
        else:
            self.logger.debug("Sessions.enrollUser ERROR: " + str(r.status_code) + ": " + r.text)
            return({str(r.status_code) : r.text})