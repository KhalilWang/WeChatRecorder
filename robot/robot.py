# -*- coding:utf-8 -*-
import sys
import werobot
import os
import sqlite3
import datetime
import pickle

basedir = os.path.dirname(os.path.abspath(__file__))
reload(sys)
sys.setdefaultencoding('utf-8')
robot = werobot.WeRoBot(token = 'helloworld')

conf = werobot.config.Config()
conf.from_pyfile(basedir + '/config.py')
client = werobot.client.Client(conf)

print basedir

conn = sqlite3.connect(basedir + '/db/data.db')
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
                "name":"我要交作业",
                "key":"HOMEWORK"
            },
            {
                "name":"其他",
                "sub_button":[
                    #{
                    #    "type":"click",
                    #    "name":"查找录音",
                    #    "key":"SEEK"
                    #},
                    {
                        "type":"click",
                        "name":"我的信息",
                        "key":"MSG"
                    },
                    {
                        "type":"click",
                        "name":"更改班级",
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

@robot.key_click('MSTUDENT')
def my_student(message, session):
    if session['user'] == 'teacher':
        session['status'] = 'tcr_seek_mstudent'

        return u'请输入班级代码'

    else:
        return u'你不是老师!'


@robot.key_click('CHANGE_CID')
def change_cid(message, session):
    if session['user'] == 'student':
        session['status'] = 'input_cid'
        return u'请输入你的班级代码!'

    else:
        return u'你不是学生或者还未登录!'


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

#@robot.key_click('SEEK')
#def seek(message, session):
#    session['status'] = 'seek_id'
#    return u'请输入音频id'

@robot.key_click('TEACHER_KEY')
def teacher_key(message, session):
    session['status'] = 'input_tid'
    return u'请输入教师号'

@robot.key_click('MSG')
def get_msg(message, session):
    if session['user']:
        if session['user'] == 'student':


            sql = "select cname from student,class where sname='"+session['student_name']+"' and  class.cid=student.cid ;"
            cr.execute(sql)
            r = cr.fetchone()


            if r:
                return u'你好, ' + session['student_name'] + u'同学！\n你的班级是:' + r['cname']

            return u'你好' + session['student_name'] + u'同学！'

        if session['user'] == 'teacher':
            return u'你好,'+session['teacher_name']+u'老师'

    else:
        return '你还没登陆!\n老师请输入 我是老师\n学生请输入 我是学生'


@robot.key_click('HOMEWORK')
def homework_key(message, session):
    if session['user'] == 'student':
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

        sql = "select * from student where sname = '"+session['student_name']+"';"
        cr.execute(sql)

        r = cr.fetchone()

        if r['cid'] == '':
            return u'你还未选择班级!\n点击【其他】 - 【更改班级】 选择你的班级!'


        session['status'] = 'record'
        return u'你可以开始录音啦!'



        '''
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
        '''


    else:
        return u'你还未登陆或者不是学生!'

@robot.filter(u"我是学生")
def student(message, session):
    session['status'] = 'input_student_name'
    return u'请输入你的名字!'

@robot.filter(u"我是老师")
def teacher(message, session):
    session['status'] = 'input_tid'
    return u'请输入教师代码'

#@robot.filter(u"msg")
#def return_today(message, session):
#    return werobot.replies.VoiceReply(message = message,
#                                      media_id = lst.pop())

@robot.voice
def voice_input(message, session):
    #if session['status'] == 'recv_homework':

    if session['status'] != 'record':
        return u'学生请点击【我要交作业】来提交语音!'
    else:


        rid = message.media_id
        sname = session['student_name']
        rtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #删掉以前有的语音
        sql = "delete from record where sname='"+sname+"';"
        cr.execute(sql)
        sql = "insert into record values ('%s', '%s', '%s');" % (sname, rid, rtime)
        print sql
        cr.execute(sql)
        conn.commit()

        session['status'] = ''

        return u'作业已经提交啦! 你好棒! :)'





    #else:
        #print message.media_id
        #msg = new Message
        #lst.append(message.media_id)
        #return werobot.replies.VoiceReply(message = message,
        #                                  media_id = message.media_id)
     #   return u'你还没说要叫交作业呢!'


@robot.text
def check_input(message, session):

    _content = message.content

    if '"' in _content:
        return u'非法字符输入!'

    if '\''  in _content:
        return u'非法字符输入!'

    if '%'  in _content:
        return u'非法字符输入!'

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
            cname = r['cname']
            cr.execute('update student set cid = ? where sname = ?;', (cid, session['student_name']))
            conn.commit()
            return u'更改成功!\n你的班级是【' + cname + u'】'
        else:
            return u'不存在该班级代码!'



    if session['status'] == 'input_student_name':
        name = message.content


        session['status'] = ''
        session['student_name'] = name
        session['user'] = 'student'

        sql = "select * from student where sname ='" + name + "';"
        cr.execute(sql)
        r = cr.fetchone()

        if r:
            print '\nStudent ' + name + ' log in '

            return u'欢迎回来,' + name + u'\n请点击【我要交作业】\n开始录音!'
        else:
            print '\nStudent ' + name +' registe'
            cr.execute("insert into student values (?, ?);", (name, ''))
            conn.commit()
            return u'欢迎第一次登陆,' + name + u'\n请点击【其他】- 【更改班级】输入班级代码\n然后点击【我要交作业】开始录音!'

    if session['status'] == 'input_tid':
        tid = message.content

        sql = "select * from teacher where tid='" + tid + "';"

        print sql
        cr.execute(sql)

        r = cr.fetchone()

        if r:
            session['user'] = 'teacher'
            session['teacher_name'] = r['tname']
            return u'欢迎回来,'+ r['tname']  + u'老师!'
        else:
            return u'不存在的教师代码'

    #if session['status'] == 'seek_id':
    #    session['status'] = ''
    #    media_id = message.content
    #    return werobot.replies.VoiceReply(message = message,
    #                                      media_id = media_id)

    if session['status'] == 'tcr_seek_mstudent':
        cid = message.content

        sql = "select * from class where cid='" + cid + "'"
        cr.execute(sql)

        r = cr.fetchone()
        if r == None:
            return u'不存在的课程代码'

        cname = r['cname']

        sql = "select * from student where cid = '" + cid + "'"
        cr.execute(sql)

        r = cr.fetchone()

        rst = u'【'+ cname + u'】班级的学生有:\n'

        if r:
            while r:
                rst += r['sname'] + ' '
                r = cr.fetchone()

            return rst
        else:
            return u'该班级还没有学生!'

    if session['status'] == 'tcr_input_cid':
        cid = message.content

        sql = "select * from class where cid='" + cid + "'"
        cr.execute(sql)

        r = cr.fetchone()
        if r == None:
            return u'不存在的课程代码'

        cname = r['cname']

        sql = "select * from student where cid = '" + cid + "'"
        cr.execute(sql)

        r = cr.fetchone()

        rst = u'【'+ cname + u'】班级的学生有:\n'

        seq = 0
        student_dict = {}

        if r:
            while r:
                rst += str(seq) + r['sname'] + '  '
                student_dict[str(seq)] = r['sname']

                seq += 1
                r = cr.fetchone()

            str_dict = pickle.dumps(student_dict)
            session['str_dict'] = str_dict
            session['status'] = 'listen_homework'
            rst += u'\n输入学生名称前【序号】收听作业!\n如未响应说明该学生没有提交作业!'
            return rst
        else:
            return u'该班级还没有学生!'

    if session['status'] == 'listen_homework':

        seq = message.content

        str_dict = session['str_dict']
        student_dict = pickle.loads(str_dict)
        print student_dict
        sname = student_dict.get(seq)

        if sname == None:
            return u'错误的序号'

        sql = "select * from record where sname='"+sname+"';"

        print sql

        cr.execute(sql)
        r = cr.fetchone()

        if r:
            return werobot.replies.VoiceReply(message = message,
                                              media_id = r['rid'])
        else:
            return u'可能还没交作业或不存在!'



    return u'你好, ' + usr['nickname'] + u'''\n如果是学生请输入我是学生\n如果是老师请输入我是老师!'''


@robot.subscribe
def subscribe(message):
    return u'欢迎关注英贝佳国际少儿英语!\n请点击【我是?】来登录:)'


#robot.config['HOST'] = '0.0.0.0'
#robot.config['PORT'] = 80
#robot.run()
