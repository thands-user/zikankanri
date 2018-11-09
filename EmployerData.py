
'''
 社員情報のクラス
'''

class EmployerData:

    def __init__(self):
        self.companyID = ""
        self.loginID = ""
        self.passwdID = ""
    
    def setCompanyID(self,companyID):
        self.companyID = companyID

    def getCompanyID(self):
        return self.companyID
    
    def setLoginID(self,loginID):
        self.loginID = loginID
    
    def getLoginID(self):
        return self.loginID
    
    def setPasswdID(self,passwdID):
        self.passwdID = passwdID
    
    def getPasswdID(self):
        return self.passwdID
    

    