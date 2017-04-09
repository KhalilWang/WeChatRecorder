#!/usr/bin/python2.7
import flask
from robot import robot
from werobot.contrib.flask import make_view
import sys
import os

basedir = os.path.dirname(os.path.abspath(__file__))
reload(sys)
sys.setdefaultencoding('utf-8')


app = flask.Flask(__name__)
app.add_url_rule(
    rule = '/robot',
    endpoint = 'werobot',
    view_func = make_view(robot),
    methods = ['GET', 'POST']
)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/student')
def student():
    name = flask.request.args.get(u'name', 'Stranger')
    return 'Welcome, ' + name + '!'

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 80)
