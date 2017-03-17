import web


urls = (
    '/wx', 'Handle',
)

class Handle(object):
    def GET(self):
        return "<h1>Hello World!</h1>"

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()