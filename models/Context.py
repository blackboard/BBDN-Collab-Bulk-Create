

class Context():

    def __init__(self, title, name, label, extId):

        self.id = None
            
        if title != None:
            self.title = title
        else:
            self.title = None
            
        if name != None:
            self.name = name
        else:
            self.name = None
            
        if label != None:
            self.label = label
        else:
            self.label = None
        
        if extId != None:
            self.extId = extId
        else:
            self.extId = None


    def getId(self):
        
        if id != None:
            return(self.id)
        else:
            return(None)
    
    def setId(self, id):

        self.id = id

    def getTitle(self):
        
        if title != None:
            return(self.title)
        else:
            return(None)
    
    def setTitle(self, title):

        self.title = title

    def getName(self):
        
        if name != None:
            return(self.name)
        else:
            return(None)
    
    def setName(self, name):

        self.name = name

    def getLabel(self):
        
        if label != None:
            return(self.label)
        else:
            return(None)
    
    def setLabel(self, label):

        self.label = label

    def getExtId(self):
        
        if extId != None:
            return(self.extId)
        else:
            return(None)
    
    def setExtId(self, extId):

        self.extId = extId

    def getContextJson(self):

        return(
            {
                "id": self.id,
                "title" : self.title,
                "name": self.name,
                "label" : self.label,
                "extId": self.extId
            }
        )