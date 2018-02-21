
class EventHubMsgSender:
    
    API_VERSION = '2016-07'
    TOKEN_VALID_SECS = 10
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'
    
    def __init__(self, connectionString=None):
        if connectionString == None:
            config = configparser.ConfigParser()
            config.read('scheduledEventsInteractiveToolConfig.ini')
            connectionString = config['DEFAULT']['connectionstring']
            connectionString = connectionString.replace("sb://","")

        if connectionString != None:
            endPoint, keyName, keyValue, entityPath = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.endPoint = endPoint
            self.keyName = keyName
            self.keyValue = keyValue
            self.entityPath = entityPath
   
    def _buildEventHubSasToken (self):
        expiry = int(time.time() + 10000)
        string_to_sign = urllib.parse.quote_plus(self.endPoint) + '\n' + str(expiry)        
        key = self.keyValue.encode('utf-8')
        string_to_sign = string_to_sign.encode('utf-8')
        signed_hmac_sha256 = hmac.HMAC(key, string_to_sign, hashlib.sha256)
        signature = signed_hmac_sha256.digest()
        signature = base64.b64encode(signature)
        return 'SharedAccessSignature sr=' + urllib.parse.quote_plus(self.endPoint)  + '&sig=' + urllib.parse.quote(signature) + '&se=' + str(expiry) + '&skn=' + self.keyName

    def sendD2CMsg(self, message):
        sasToken = self._buildEventHubSasToken()
        url = 'https://%s%s/messages?api-version=%s' % (self.endPoint,  self.entityPath,self.API_VERSION)
        data = message.encode ('ascii')
        req = urllib.request.Request (url, headers={'Authorization': sasToken}, data=data, method='POST')
        with urllib.request.urlopen(req) as f:
            pass
        return f.read().decode('utf-8')

