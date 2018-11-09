import sys
import re
import urllib
import requests
import json
import calendar
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import IniReader
import EmployerData
import UrlData
import CalculateOverTime
import InformSlack

'''
    followから残業時間をとる
'''
class MainCalculateOverTime:
    employerData = EmployerData.EmployerData()
    urlData = UrlData.UrlData()
    #メイン処理
    def main(self):
        #iniファイルの読み込み
        iniReader = IniReader.IniReader(main.employerData, main.urlData)
        iniReader.readIniFile()
        
        #urlの取得
        options = Options()
        options.add_argument('--user-agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')
        options.add_argument('--headless')
        options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        driver = webdriver.Chrome(chrome_options=options,executable_path="C:\work\chromedriver.exe")
        driver.get(main.urlData.getFollowUrl())
        
        #idとpasswordの入力
        driver.find_element_by_id("companyID").send_keys(main.employerData.getCompanyID())
        driver.find_element_by_id("loginID").send_keys(main.employerData.getLoginID())
        driver.find_element_by_id("passwdID").send_keys(main.employerData.getPasswdID())
        driver.find_element_by_class_name("btn-login ").click()
        driver.find_element_by_class_name("navi-category").click()
        driver.execute_script("javascript:doExecuteMenu('KNM','1010','1000',0);")
        #残業時間の集計
        caluclataOverTime = CalculateOverTime.CalculateOverTime()
        caluclataOverTime.calcutaleTheHalf(driver)
        
        #slackで通知
        InformSlack.InformSlack().informTime(caluclataOverTime.totalTime,main.urlData.slackUrl)

main = MainCalculateOverTime()
main.main()