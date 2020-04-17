

class User():

    def __init__(self, displayName, extId, email):

        self.id = None
            
        if displayName != None:
            self.displayName = displayName
        else:
            self.displayName = None
        
        if extId != None:
            self.extId = extId
        else:
            self.extId = None
        
        if email != None:
            self.email = email
        else:
            self.email = None


    def getId(self):
        
        if self.id != None:
            return(self.id)
        else:
            return(None)
    
    def setId(self, id):

        self.id = id

    def getDisplayName(self):
        
        if self.displayName != None:
            return(self.displayName)
        else:
            return(None)
    
    def setDisplayName(self, displayName):

        self.displayName = displayName

    def getExtId(self):
        
        if self.extId != None:
            return(self.extId)
        else:
            return(None)
    
    def setExtId(self, extId):

        self.extId = extId

    def getEmail(self):
        
        if self.email != None:
            return(self.email)
        else:
            return(None)
    
    def setEmail(self, email):

        self.email = email

    def getUserJson(self):

        return(
            {
                "id": self.id,
                "displayName": self.displayName,
                "extId": self.extId,
                "email": self.email
            }
        )