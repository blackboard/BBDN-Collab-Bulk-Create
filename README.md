# BBDN-Collab-Bulk-Create
This is an open source Python project that allows an institution with a Blackboard Collaborate license to bulk create contexts, users, sessions, and enrollments.

This project is built with Python 3.7. You have two choices to build. You can use virtualenv. From the commandline on a Mac:

```bash
source venv/bin/activate
python CreateSessions.py
deactivate
```

If you are running on Windows, here is a [document describing the use of virtualenv](https://docs.python.org/3.7/library/venv.html).

You can also just install the libraries locally:

```bash
pip install -r requirements.txt
```

Before running, you must copy ConfigTemplate.py to Config.py and insert your credentials.

Step one is to configure the collab API connection with your key, secret, and base url. The base url should not contain the schema, for example: `techpreview.bbcollab.com`, not `https://techpreview.bbcollab.com`.

```json
collab = {
    "collab_key" : "YOURKEY",
    "collab_secret" : "YOURSECRET",
    "collab_base_url" : "COLLAB_URI",
    "verify_certs" : "True"
}
```

Next, verify your session settings match your expectations. For more information on session settings, see [Collaborate Session Definitions](https://docs.blackboard.com/collab/CollaborateSessionDefinitions.html). It is important to note that not all settings are configurable. As this is meant to bulk create consistent sessions, it will create a room that starts immediately and has no end date. As such, you cannot set recurrence rules either.

```json
session_settings = {
    "createdTimezone" : "America/New_York",
    "courseRoomEnabled" : "false",
    "boundaryTime": "15",
    "participantCanUseTools": "false",
    "occurrenceType": "S",
    "allowInSessionInvitees": "false",
    "allowGuest": "false",
    "guestRole": "participant",
    "canAnnotateWhiteboard": "false",
    "canDownloadRecording": "false",
    "canPostMessage": "false",
    "canShareAudio": "false",
    "canShareVideo": "false",
    "mustBeSupervised": "true",
    "openChair": "false",
    "raiseHandOnEnter": "true",
    "showProfile": "false"
}
```

The rest of the settings in this file are related to logging. It is set to log INFO and above, though you can certainly change to DEBUG if you wish to see more data. Logs go to `logs/session-creation.log`, but if you have DEBUG level set and you are running a large dataset, expect a large log file. 

**NOTE**: Students are enrolled as participants. The teacher can elevate these priviliges in the session, should they so choose.


## To Use This Script

This script is meant to allow you to bulk create contexts, users, sessions, and enrollments. To do this, the script looks in the `data` directory for three files:

* course.csv - This file contains information about the course and the instructor
* student.csv - This file contains information about the students
* enrollment.csv - This file contains a mapping of course Id to student Id in order to generate enrollments

For templates for these files, see the `datatemplates` directory. 

### course.csv

This file requires the following information:
* COURSEID - this will be used to create a Context in Collaborate. The course Id will be set as the external Id for the context
* COURSENAME - this will be used to set the session name and the context name
* TEACHERID - this will be used to as the external Id for the moderator user
* TEACHERNAME - this will be used as the display name for the moderator user
* TEACHEREMAIL - this is added to the moderator user, as well as being added to the output file for ease of communication of the moderator's collaborate link

### student.csv

This file requires the following information:
* STUDENTID - this will be used as the external Id for the student user
* STUDENTNAME - this will be used as the display name for the student user
* STUDENTEMAIL - this is added to the student user, as well as being added to the output file for ease of communication of the strudent's collaborate link

### enrollment.csv

This file requires the following information:
* COURSEID - the same course Id from the course.csv file
* STUDENTID - the same student Id from the student.csv file

## Output

Upon completion of the script, you will see in the `output` directory, two files:

* studentenrollments.csv contains all of the information to map a student to a course to a teacher, and provide the unique URL for accessing the Collaborate session for that user in that course.
* teacherenrollments.csv contains the information mapping a course to a teacher to a unique moderator link

These are purposely kept separate to prevent a user from accidentally sending a student the moderator link.

### studentenrollments.csv

This file contains the following information:
* COURSEID - The course Id provided in the course.csv file
* TEACHERID - The teacher Id provided in the course.csv file
* TEACHERNAME - The teacher name provided in the course.csv file
* STUDENTID - The student Id provided in the student.csv file
* STUDENTNAME - The student name provided in the student.csv file
* STUDENTEMAIL - The student email address provided in the student.csv file
* COURSENAME - The course name provided in the course.csv file
* URL - The student's unique Collaborate URL for this course

### teacherenrollments.csv

This file contains the following information:
* TEACHERID - The teacher Id provided in the course.csv file
* TEACHEREMAIL - The teacher email address provided in the course.csv file
* COURSENAME - The course name provided in the course.csv file
* URL - The teacher's unique Collaborate moderator URL for this course
