#! /usr/bin/python3

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import whois

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ResultHandler(tornado.web.RequestHandler):

    def get(self):
        domain = self.get_argument('domain')
        w = whois.whois(domain)
        info = w.text.splitlines()
        self.render('result.html', info=info)

    def post(self):
        domain = self.get_argument('domain')
        w = whois.whois(domain)
        info = w.text.splitlines()
        self.render('result.html', info=info)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/result', ResultHandler)]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
