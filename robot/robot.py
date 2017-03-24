# -*- coding:utf-8 -*-
import sys
import werobot
import re
import os

basedir = os.path.dirname(os.path.abspath(__file__))
reload(sys)
sys.setdefaultencoding('utf-8')
robot = werobot.WeRoBot(token = 'helloworld')

conf = werobot.config.Config()
conf.from_pyfile('config.py')
client = werobot.client.Client(conf)

rst = client.create_menu({
                "button":[
                    {
                        "type":"click",
                        "name":"我是学生",
                        "key":"STUDENT_KEY"
                    },
                    {
                        "type":"click",
                        "name":"我是老师",
                        "key":"TEACHER_KEY"
                    },
                    {
                        "name":"我的信息",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"GOOD"
                            }
                        ]
                    }
                ]})



#不使用的请求
#params = {'grant_type':'client_credential', 'appid':str(_appID), 'secret':str(_appSecret)}
#req = requests.post('https://api.weixin.qq.com/cgi-bin/token', params)
#print req.text


@robot.key_click('STUDENT_KEY')
def student_key():
    return '你按下了我是学生按钮!'


@robot.text
def switch_text_msg(message, session):
  msg = message.content
  print 'msg :' + msg

  if re.compile('*网址*').match(msg):
    return 'http://khalilwang.tech'

  if msg == '我是学生':

    session['user'] = 'student'
    session['status'] = 'input_name'
    return '请输入你的名字'
  elif session['status'] == 'input_name':
    session['name'] = msg
    session['status'] = 'none'
    return msg + '同学, 欢迎!'


  elif msg == '我是老师':
    session['user'] = 'teacher'
    session['status'] = 'input_teacher_code'
    return '请输入老师密码!'
  elif session['status'] == 'input_teacher_code':
    # sql judgement
    session['status'] = 'none'
    return '你的密码是:' + msg
  else:
    return '学生请输入: 我是学生 \n老师请输入: 我是老师\n'

@robot.subscribe
def subscribe(message):
  return '欢迎关注点点!\n学生请输入: 我是学生\n老师请输入: 我是老师!\n感谢您的使用!'


#robot.config['HOST'] = '0.0.0.0'
#robot.config['PORT'] = 80
#robot.run()
