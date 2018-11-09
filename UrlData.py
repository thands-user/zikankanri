

'''
 接続先URL情報のクラス
'''

class UrlData:

    def __init__(self):
        self.followUrl = ""
        self.slackUrl = ""
        
    def setFollowUrl(self,followUrl):
        self.followUrl = followUrl

    def getFollowUrl(self):
        return self.followUrl
    
    def setSlackUrl(self,slackUrl):
        self.slackUrl = slackUrl
    
    def getSlackUrl(self):
        return self.slackUrl
    
    