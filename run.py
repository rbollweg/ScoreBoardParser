__author__ = 'The Gibs'

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app import app
from app import parser


def main():
    parser.load_item_numbers()
    parser.load_special_champ_names()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)

    IOLoop.instance().start()


if __name__ == "__main__":
    main()