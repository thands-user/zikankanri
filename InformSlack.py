import json
import requests
'''
 残業時間をslackで通知する処理
'''

class InformSlack:

    def informTime(self,overTime,slackUrl):
        message = 'あなたの残業時間は'+overTime
         #slackへ通知
        json_msg = json.dumps({
                               'text'      : message,
                               'channel'   : '#notification_test',
                               'username'  : 'oshirase',
                               'icon_emoji': ':lawson:',
                          })
       
        requests.post( slackUrl
                  ,data = json_msg
                 )
                