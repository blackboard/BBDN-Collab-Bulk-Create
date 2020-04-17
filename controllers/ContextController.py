
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
import logging

class ContextController():

    def __init__(self, target_url, auth, verify_certs):
        self.target_url = target_url
        self.auth = auth
        self.verify_certs = verify_certs

        self.logger = logging.getLogger(name='contexts')

    def getContext(self, name):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.auth.getToken()
        
        r = requests.get("https://" + self.target_url + '/contexts?name=' + name, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, verify=self.verify_certs)

        if r.status_code == 200:
            res = json.loads(r.text)
            self.logger.debug(json.dumps(res,indent=4, separators=(',', ': ')))

            contextId = None

            if res['size'] > 0:
                contextId = res['results'][0]['id']
           
            return({'contextId' : contextId})
        else:
            self.logger.debug("Context.createContext ERROR: " + str(r))
            return({'contextId':None})

    def createContext(self, contextJson):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.auth.getToken()
        
        r = requests.post("https://" + self.target_url + '/contexts', headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=contextJson, verify=self.verify_certs)

        if r.status_code == 200:
            res = json.loads(r.text)
            self.logger.debug(json.dumps(res,indent=4, separators=(',', ': ')))
            contextId = res['id']
            return({str(r.status_code) : contextId})
        else:
            self.logger.debug("Context.createContext ERROR: " + str(r))
            return({str(r.status_code) : r.text})

    def assignSessionToContext(self, contextId, sessionId):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.auth.getToken()

        idJson = {
            'id' : sessionId
        }
        
        r = requests.post("https://" + self.target_url + '/contexts/' + contextId + '/sessions', headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=idJson, verify=self.verify_certs)

        if r.status_code == 200:
            return(True)
        else:
            self.logger.debug("Context.assignSessionToContext ERROR: " + str(r))
            return(False)