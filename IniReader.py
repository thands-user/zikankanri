import configparser
import EmployerData
import UrlData
import re

"""
iniファイルを読み込み各種情報を保持するデータクラス
"""

class IniReader:
    employerData = EmployerData.EmployerData()
    urlData = UrlData.UrlData()
    
    def __init__(self, employerData, urlData):
        self.employerData = employerData
        self.urlData = urlData

    def readIniFile(self):
        conf = configparser.SafeConfigParser()
        conf.read('properties.ini',encoding='utf-8')
        for section in conf.sections():
            self.getSectionLinkedValue(conf, section)
        
    def getSectionLinkedValue(self, conf, section):
        for key in conf[section]:
            #kakunou
            self.isCheckValueOfCompanyID(conf.get(section,key),key)
        
    def isCheckValueOfCompanyID(self,linkdvalue,key):
        if not key.find("company"):
            return self.employerData.setCompanyID(linkdvalue)
        
        if not key.find("login"):
            return self.employerData.setLoginID(linkdvalue)
        
        if not key.find("passwd"):
            return self.employerData.setPasswdID(linkdvalue)
        
        if not key.find("follow"):
            return self.urlData.setFollowUrl(linkdvalue)
        
        if not key.find("slack"):
            return self.urlData.setSlackUrl(linkdvalue)
        
        return
    
#iniReader = IniReader().readIniFile()
