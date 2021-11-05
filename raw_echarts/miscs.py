import sys
import threading
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from raw_echarts.bases import CONFIG


__all__ = ['serve_assets']


RUNNING_SERVERS = {}


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(*args):
        pass


def handler_from(folder):
    handler = functools.partial(SilentHandler, directory=folder)
    return handler


class ServerThread(threading.Thread):
    def __init__(self, ip='127.0.0.1', port=80, folder=None):
        super().__init__()
        port = int(port)
        self.ip = ip
        self.port = port
        self.folder = folder
        self.running = False
        self.server = HTTPServer((ip, port), handler_from(folder))
        self.setDaemon(True)

    def run(self):
        if self.port not in RUNNING_SERVERS:
            RUNNING_SERVERS[self.port] = self
            self.running = True
            self.server.serve_forever()
            self.running = False


def serve_assets(folder=None, port=80, ip='127.0.0.1'):
    t = ServerThread(ip, port, folder)
    print('start assets server on "{}:{}"\nfrom "{}"'.format(ip, port, folder))
    CONFIG.ECHARTS_ASSETS = 'http://{}:{}/assets/'.format(ip, port)
    t.start()


if __name__ == '__main__':
    serve_assets(folder=r'f:\myrepo\pyecharts-assets\assets')
