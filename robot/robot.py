# -*- coding:utf-8 -*-
import sys
import werobot
import os
import sqlite3
import pickle

basedir = os.path.dirname(os.path.abspath(__file__))
reload(sys)
sys.setdefaultencoding('utf-8')
robot = werobot.WeRoBot(token = 'helloworld')

conf = werobot.config.Config()
conf.from_pyfile('config.py')
client = werobot.client.Client(conf)

conn = sqlite3.connect('db/data.db')
conn.row_factory = sqlite3.Row
cr = conn.cursor()


client.create_menu({
        "button":[
            {
                "name":"我是?",
                "sub_button":[
                    {
                        "type":"click",
                        "name":"我是学生",
                        "key":"STUDENT_KEY"
                    },
                    {
                        "type":"click",
                        "name":"我是老师",
                        "key":"TEACHER_KEY"
                    }]
            },
            {
                "type":"click",
                "name":"今日作业",
                "key":"HOMEWORK"
            },
            {
                "name":"其他",
                "sub_button":[
                    {
                        "type":"click",
                        "name":"查找录音",
                        "key":"SEEK"
                    },
                    {
                        "type":"click",
                        "name":"我的信息",
                        "key":"MSG"
                    },
                    {
                        "type":"click",
                        "name":"我的班级",
                        "key":"CHANGE_CID"
                    },
                    {
                        "type":"click",
                        "name":"收听作业",
                        "key":"LISTEN_HW"
                    },
                    {
                        "type":"click",
                        "name":"我的学生",
                        "key":"MSTUDENT"
                    }

                ]
            }
        ]})



#不使用的请求
#params = {'grant_type':'client_credential', 'appid':str(_appID), 'secret':str(_appSecret)}
#req = requests.post('https://api.weixin.qq.com/cgi-bin/token', params)
#print req.text

#lst = []
@robot.key_click('LISTEN_HW')
def listen_homework(message, session):
    if session['user'] != 'teacher':
        return u'你不是老师!'




    return u'请输入想收听的学生姓名'



@robot.key_click('MSTUDENT')
def my_student(message, session):

    if session['user'] == 'teacher':
        pass


    else:
        return u'你不是老师!'


@robot.key_click('CHANGE_CID')
def change_cid(message, session):
    if session['user'] == 'student':
        session['status'] = 'input_cid'
        return u'请输入你的班级代码!'
    if session['user'] == 'teacher':
        session['status'] = 'input_cid'
        return u'请输入你想要听课的班级!'

    else:
        return u'你还未登录!'


@robot.key_click('LISTEN_HW')
def listen_hw(message, session):
    if session['user'] != 'teacher':
        return u'你不是老师或者还未登录!'

    else:
        session['status'] = 'tcr_input_cid'
        return u'请输入想收听的班级代码'


@robot.key_click('STUDENT_KEY')
def student_key(message, session):
    session['status'] = 'input_student_name'
    return u'请输入你的名字!'

@robot.key_click('SEEK')
def seek(message, session):
    session['status'] = 'seek_id'
    return u'请输入音频id'

@robot.key_click('TEACHER_KEY')
def teacher_key(message, session):
    session['status'] = 'input_teacher_code'
    return u'请输入教师代码'

@robot.key_click('MSG')
def get_msg(message, session):
    if session['user']:
        if session['user'] == 'student':
            return u'你好' + session['student_name'] + u'同学！'
        if session['user'] == 'teacher':
            return u'你好,老师,您的代码是' + session['teacher_code']
    else:
        return '你还没登陆!\n老师请输入 我是老师\n学生请输入 我是学生'


@robot.key_click('HOMEWORK')
def homework_key(message, session):
    if session['user'] == 'student' and session['status'] != 'listen':
        #session['status'] = 'recv_homework'
        #rply = werobot.replies.ArticlesReply(message = message)
        #article = werobot.replies.Article(
        #    title = u'欢迎' + session['student_name'],
        #    description = '点击开始听作业!',
        #    img = 'http://mmbiz.qpic.cn/mmbiz_jpg/ZP1NxmOywt5F4mYaR2XHd2tmlbsz5s0m2uYngul5LEdDWvNAjvQX5yXqyURa6QS8cxa7SribjwSsfU8qOsIjwFg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1',
        #    url = 'https://mp.weixin.qq.com/s?__biz=MzI2NDYxMzM3NQ==&tempkey=mR8TR0zHAhOT9xUzfChMhwxWwEfa2Vr%2BusabZT4C1G1VvmVF9Un6N8oj4YTG7bOJsXPUW3dxXgWzOipenJIu4o19h6aJ5g%2BOT3VK3Tf20ZPAYIRMiB9%2BxK92I72FR4ouOGk4m5TXFJ3FvC%2B3Le7laA%3D%3D&chksm=6aa8bd935ddf3485daf118efa3ddd8e7bfcba2f2227ceab10b01482677abaa9c82bf40d6493e##'
        #)
        #rply.add_article(article)
        #return rply

        sql = "select cid from student where sid='" + message.source + "';"
        cr.execute(sql)
        r = cr.fetchone()
        print r
        if r:
            cid = r[0]
            sql = "select * from homework where cid='"+ cid +"';"
            cr.execute(sql)

            r2 = cr.fetchone()
            hid = r2['hid']

            sql = "select * from homework_content where hid='" + hid + "';"
            cr.execute(sql)

            r3 = cr.fetchall()
            length = len(r3)

            print r3
            lst = []
            for each in r3:
                lst.append(each[1])

            pdata = pickle.dumps(lst)
            print pdata

            session['homework_lst'] = pdata
            session['status'] = 'listen'
            rst = u'你的班级代码是【'+ cid + u'】\n请继续点击【今日作业】收听作业!'
            rst += u'\n今天作业一共【'+str(length)+u'】条'
            return rst

        else:
            return u'你还没有输入班级代码!'

    elif session['status'] == 'listen':
        lst = pickle.loads(session['homework_lst'])

        if lst != []:
            trid = lst.pop(0)
            pdata = pickle.dumps(lst)
            session['homework_lst'] = pdata
            sql = "select * from trecord where trid='"+trid+"';"
            cr.execute(sql)
            r = cr.fetchone()
            media = r[0]

            return werobot.replies.VoiceReply(message = message, media_id = media)

        else:
            session['status'] = ''
            return u'你听完了本次作业!'

    else:
        return u'你还未登陆或者不是学生!'

@robot.filter(u"我是学生")
def student(message, session):
    session['status'] = 'input_student_name'
    return u'请输入你的名字!'

@robot.filter(u"我是老师")
def teacher(message, session):
    session['status'] = 'input_teacher_code'
    return u'请输入教师代码'

#@robot.filter(u"msg")
#def return_today(message, session):
#    return werobot.replies.VoiceReply(message = message,
#                                      media_id = lst.pop())

@robot.voice
def voice_input(message, session):
    #if session['status'] == 'recv_homework':
    return u'收到了语音!\n输入 我读完啦 来完成提交\nid:[在查找中输入可听]\n' + message.media_id


    #else:
        #print message.media_id
        #msg = new Message
        #lst.append(message.media_id)
        #return werobot.replies.VoiceReply(message = message,
        #                                  media_id = message.media_id)
     #   return u'你还没说要叫交作业呢!'


@robot.filter(u'我读完啦')
def over(message, session):
    if session['status'] == 'recv_homework':
        session['status'] = ''
        return u'您的作业已提交!'


@robot.text
def check_input(message, session):
    usrid = message.source
    usr = client.get_user_info(usrid, lang='zh_CN')

    if session['status'] == 'input_cid' and session['user'] == 'student':
        session['status'] = ''
        cid = message.content
        sql = "select * from class where cid='" + cid + "';"
        print sql
        cr.execute(sql)
        r = cr.fetchone()

        if r:
            cr.execute('update student set cid = ? where sid = ?;', (cid, usrid))
            conn.commit()
            return u'更改成功!'
        else:
            return u'不存在该班级代码!'

    if session['status'] == 'input_cid' and session['user'] == 'teacher':
        session['status'] = ''
        cid = message.content
        sql = "select * from class where cid='" + cid + "';"
        print sql
        cr.execute(sql)
        r = cr.fetchone()

        if r:
            cr.execute('update teacher set cid = ? where tid = ?;', (cid, usrid))
            conn.commit()
            return u'更改成功!'
        else:
            return u'不存在该班级代码!'



    if session['status'] == 'input_student_name':
        name = message.content
        session['status'] = ''
        session['student_name'] = name
        session['user'] = 'student'

        sql = "select * from student where sid ='" + usrid + "';"
        print sql
        cr.execute(sql)
        r = cr.fetchone()
        print r

        if r:
            return u'欢迎回来,' + name + u'\n请点击【今日作业】\n开始收听作业!'
        else:
            cr.execute("insert into student values (?, ?, ?);", (usrid, name, ''))
            conn.commit()
            return u'欢迎第一次登陆,' + name + u'\n请点击【其他】- 【我的班级】输入班级代码\n然后点击【今日作业】开始收听作业!'

    if session['status'] == 'input_teacher_code':
        code = message.content
        session['user'] = 'teacher'
        session['teacher_code'] = code
        return u'你输入的教师编号是' + code

    if session['status'] == 'seek_id':
        session['status'] = ''
        media_id = message.content
        return werobot.replies.VoiceReply(message = message,
                                          media_id = media_id)
    if session['student_name']:
        return u'你好' + session['student_name']

    if session['status'] == 'tcr_input_cid':
        cid = message.content
        sql = "select * from class where cid = '" + cid + "';"
        cr.execute(sql)
        ####################################################
        return u'学生列表'

    return u'你好, ' + usr['nickname'] + u'''\n如果是学生请输入我是学生\n如果是老师请输入我是老师!'''


@robot.subscribe
def subscribe(message):
    return u'欢迎关注起跑线!\n请点击【我是?】来登录:)'


#robot.config['HOST'] = '0.0.0.0'
#robot.config['PORT'] = 80
#robot.run()
