import werobot 

robot = werobot.WeRoBot(token = 'helloworld')

@robot.handler
def hello(message):
	return message.content

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
