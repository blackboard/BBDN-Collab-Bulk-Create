import datetime

class Session():

    def __init__(self, name, description, startTime, endTime, session_config):
        
        self.id = None

        self.name = name
        self.description = description
        self.startTime = startTime

        if endTime is not None:
            self.endTime = endTime
            self.noEndDate = False
        else:
            self.endTime = None
            self.noEndDate = True

        self.session_config = session_config
        
    def getId(self):
        return self.id

    def setId(self, sesId):
        self.id = sesId

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description
    
    def getStartTime(self):
        return self.startTime

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getEndTime(self):
        return self.endTime

    def setEndTime(self, endTime):
        if endTime is not None:
            self.endTime = endTime
            self.noEndDate = False
        else:
            self.endTime = None
            self.noEndDate = True

    def getSessionConfig(self):
        return self.session_config

    def setSessionConfig(self, session_config):
        self.session_config = session_config

    def getSessionJson(self):
        
        sessionJson = {
            "createdTimezone" : self.session_config['createdTimezone'],
            "allowInSessionInvitees": self.session_config['allowInSessionInvitees'],
            "openChair": self.session_config['openChair'],
            "mustBeSupervised": self.session_config['mustBeSupervised'],
            "description": self.description,
            "canPostMessage": self.session_config['canPostMessage'],
            "participantCanUseTools": self.session_config['participantCanUseTools'],
            "courseRoomEnabled": self.session_config['courseRoomEnabled'],
            "canAnnotateWhiteboard": self.session_config['canAnnotateWhiteboard'],
            "canDownloadRecording": self.session_config['canDownloadRecording'],
            "canShareVideo": self.session_config['canShareVideo'],
            "name": self.name,
            "raiseHandOnEnter": self.session_config['raiseHandOnEnter'],
            "allowGuest": self.session_config['allowGuest'],
            "showProfile": self.session_config['showProfile'],
            "canShareAudio": self.session_config['canShareAudio'],
            "startTime" : self.startTime,
            "boundaryTime" : self.session_config['boundaryTime'],
            "occurrenceType" : self.session_config['occurrenceType']
        }

        if(self.noEndDate):
            sessionJson['noEndDate'] = self.noEndDate
        else:
            sessionJson['endTime'] = self.endTime

        recurrenceEndType = self.session_config['recurrenceEndType']

        if recurrenceEndType is not None:

            recurrenceRuleJson = {
                "recurrenceEndType" : recurrenceEndType,
                "recurrenceType" : self.session_config['recurrenceType'],
                "daysOfTheWeek" : self.session_config['daysOfTheWeek'],
                "interval" : self.session_config['interval']
            }

            if recurrenceEndType == 'on_date':
                recurrenceRuleJson['endDate'] = self.session_config['endDate']

            if recurrenceEndType == 'after_occurrence_count':
                recurrenceRuleJson['numberOfOccurences'] = self.session_config['numberOfOccurences']

            sessionJson['recurrenceRule'] = recurrenceRuleJson
        
        return sessionJson