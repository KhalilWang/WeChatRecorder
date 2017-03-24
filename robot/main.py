#!/usr/bin/python2.7
import flask
from robot import robot
from werobot.contrib.flask import make_view



app = flask.Flask(__name__)
app.add_url_rule(
    rule = '/robot/',
    endpoint = 'werobot',
    view_func = make_view(robot),
    methods = ['GET', 'POST']
)

@app.route('/')
def index():
  return 'helloWorld! <br/>'

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 80)
