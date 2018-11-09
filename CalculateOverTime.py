import sys
import re
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
 残業時間の集計をする
'''
class CalculateOverTime:
    def __init__(self):
        self.theMonthEndDay = 0
        self.theCurrentMonth = ""
        self.theFirstDayPoint = 0
        self.theOverTimeTotal = []
        self.hourList = []
        self.minutesList = []
        self.totalTime = ""

    def calcutaleTheHalf(self, driver):
        #当月の取得
        self.theCurrentMonth = self.parseMonth(driver)
        print(self.theCurrentMonth)
        #集計開始日を取得
        self.theFirstDayPoint = self.gettheFirstDayPoint(driver)
        print(self.theFirstDayPoint)
        print(type(self.theFirstDayPoint))
        self.theFirstDayPoint = int(re.sub('\(.*', '',self.theFirstDayPoint))
        #月の最終日取得
        self.theMonthEndDay = self.getTheMonthEndDay()
        #残業時間の集計
        #後半から前半まで
        if self.theFirstDayPoint == 1:
            self.secondHalfTime(driver)
            #先月に戻る
            driver.find_element_by_class_name("btn-primary").click()
            #firstdayの入れ替え
            self.theFirstDayPoint = self.searchFirstDayXpath(driver)
            self.firstHalfTime(driver)
        #前半のみ
        else:
            #戻るボタン
            driver.find_element_by_class_name("btn-primary").click()
            #return
            self.firstHalfTime(driver)
        
        print(self.hourList)
        print(self.minutesList)
        self.calculate()

    #16日から月末まで
    def secondHalfTime(self,driver): 
        for i in range(self.theMonthEndDay):
            #この書き方は..
            tmpEndDay = '//*[@id="listTable"]/tbody/tr['+str(i+self.theFirstDayPoint)+']/td[1]'
            tmpHoliday = '//*[@id="listTable"]/tbody/tr['+str(i+self.theFirstDayPoint)+']/td[3]'
            tmpWorkTime = '//*[@id="listTable"]/tbody/tr['+str(i+self.theFirstDayPoint)+']/td[4]'
            #残業時間を足していく
            self.appendHourMinutes(driver,tmpWorkTime)
            #月の最終日かどうか
            if(self.isCheckLastDay(driver,tmpEndDay)):
                break
            #休みなんていらないよ
            if(self.isCheckHoliday(driver,tmpHoliday)):
                continue

    #1日から15日まで
    def firstHalfTime(self,driver): 
        for i in range(15):
            #この書き方は..
            tmpEndDay = '//*[@id="listTable"]/tbody/tr['+str(i+self.theFirstDayPoint)+']/td[1]'
            tmpHoliday = '//*[@id="listTable"]/tbody/tr['+str(i+self.theFirstDayPoint)+']/td[3]'
            tmpWorkTime = '//*[@id="listTable"]/tbody/tr['+str(i+self.theFirstDayPoint)+']/td[4]'
            #残業時間を足していく
            self.appendHourMinutes(driver,tmpWorkTime)
            #15日かどうか
            if(self.isCheckLastDay(driver,tmpEndDay)):
                break
            #休みなんていらないよ
            if(self.isCheckHoliday(driver,tmpHoliday)):
                continue

    #残業時間を追加
    def appendHourMinutes(self,driver,tmpWorkTime):
       overTimeTotal = driver.find_element_by_xpath(tmpWorkTime).text.split(':')

       if 1 < len(overTimeTotal):
            self.hourList.append(overTimeTotal[0])
            self.minutesList.append(overTimeTotal[1])

    #その月の最終日取得処理
    def getTheMonthEndDay(self):
        return calendar.monthrange(int(datetime.now().strftime('%Y')),int(datetime.now().strftime('%m')))[1]
    
    #取得月のパース処理
    def parseMonth(self,driver):
        #当月
        theCurrentMonth = re.sub('.*年|月', '', driver.find_element_by_xpath('/html/body/div/div[2]/div/article/section/div[1]/div[1]/div/h3').text)
        
        if self.isCheckCurrentMonth(theCurrentMonth):
            theCurrentMonth = (datetime.now() - relativedelta(months=1)).strftime("%m")
        
        if(len(theCurrentMonth) < 2):
            theCurrentMonth = '0'+theCurrentMonth
        return theCurrentMonth

    #取得した月が現在月と一致しているかチェック
    def isCheckCurrentMonth(self,theCurrentMonth):
        if(theCurrentMonth == datetime.now().strftime("%m")):
            if(15 < int(datetime.now().strftime("%d"))):
                return True
        return False
        
    #休日チェック
    def isCheckHoliday(self,driver,tmpHoliday):
        return re.search('休日',driver.find_element_by_xpath(tmpHoliday).text)

    #月の最終日チェック
    def isCheckLastDay(self,driver,tmpEndDay):
        return re.search(str(self.theMonthEndDay),driver.find_element_by_xpath(tmpEndDay).text)
    
    #集計開始日の取得
    def gettheFirstDayPoint(self, driver):
        #16日のxpathを特定
        #if(15 < int(datetime.now().strftime("%d"))):
        #    return '1'
        return '1'
        #return self.searchFirstDayXpath(driver)
    
    #1日のxpathを特定
    def searchFirstDayXpath(self,driver):
        if re.compile("1\(").search(driver.find_element_by_xpath('//*[@id="listTable"]/tbody/tr[17]/td[1]/button/span/font').text):
            return 17
        if re.compile("1\(").search(driver.find_element_by_xpath('//*[@id="listTable"]/tbody/tr[16]/td[1]/button/span/font').text):
            return 16
        if re.compile("1\(").search(driver.find_element_by_xpath('//*[@id="listTable"]/tbody/tr[15]/td[1]/button/span/font').text):
            return 15
        if re.compile("1\(").search(driver.find_element_by_xpath('//*[@id="listTable"]/tbody/tr[14]/td[1]/button/span/font').text):
            return 14
        if re.compile("1\(").search(driver.find_element_by_xpath('//*[@id="listTable"]/tbody/tr[13]/td[1]/button/span/font').text):
            return 13
    
    #残業時間集計
    def calculate(self):
        minutes = sum(int(n) for n in self.minutesList) % 60
        hour = sum(int(n) for n in self.hourList) + int((sum(int(n) for n in self.minutesList) - minutes)/60)
        self.totalTime = str(hour)+':'+str(minutes)
