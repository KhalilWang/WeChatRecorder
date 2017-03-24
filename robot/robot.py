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

client.create_menu({
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
    return u'你按下了我是学生按钮!'


@robot.key_click('TEACHER_KEY')
def teacher_key():
    return u'233'


@robot.filter(u"我是学生")
def student(message, session):
    session['status'] = 'input_student_name'
    return u'请输入你的名字!'

@robot.text
def check_input(message, session):
    if session['status'] == 'input_student_name':
        name = message.content
        session['status'] = ''
        return [
            u'欢迎' + name,
            u'点击这里开始提交',
            'img',
            u'khalilwang.tech/student?name=' + name
        ]



@robot.subscribe
def subscribe(message):
  return u'欢迎关注!'


#robot.config['HOST'] = '0.0.0.0'
#robot.config['PORT'] = 80
#robot.run()
