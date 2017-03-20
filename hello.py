# -*- coding:utf-8 -*- 
import sys
import werobot
import re
import requests

_appSecret = '051a944644b2b0f6160acda353a18bed'
_appID = 'wx5b37d5578da05f94'

reload(sys)
sys.setdefaultencoding('utf-8')
robot = werobot.WeRoBot(token = 'helloworld')

def get_access_token():
  params = {'grant_type':'client_credential', 'appid':str(_appID), 'secret':str(_appSecret)}
  req = requests.get('https://api.weixin.qq.com/cgi-bin/token', params)



@robot.text
def switch_text_msg(message, session):
  msg = message.content
  print 'msg :' + msg
  if msg == '我是学生':
    
    session['user'] = 'student'
    session['islogined'] = 'none'
    return '请输入学号!'
  if re.compile('[0-9]{6}').match(msg) and session.get('user') == 'student':
    return '你的学号是:' + msg + ', 欢迎!'

@robot.subscribe
def subscribe(message):
  return '欢迎关注点点!\n学生请输入: 我是学生\n老师请输入: 我是老师!\n感谢您的使用!'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

