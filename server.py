# From https://github.com/abourget/gevent-socketio/tree/master/examples
import os
from mindflex import MindFlexConnection

from gevent import monkey; monkey.patch_all()
import gevent

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

INTERFACE_FOLDER = 'interface'

def broadcast_msg(server, ns_name, event, *args):
    pkt = dict(type="event",
               name=event,
               args=args,
               endpoint=ns_name)

    for sessid, socket in server.sockets.iteritems():
        socket.send_packet(pkt)


def read_mindflex(server, connection):
    def broadcast_callback(data):
        print data
        broadcast_msg(server, '/mindflex', 'data', data)
    connection.read(broadcast_callback)


class Application(object):
    def __init__(self):
        self.buffer = []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

        if (path.startswith('static/') or 
            path == 'index.html' or 
            path == 'gif.html'):
            try:
                data = open(os.path.join(INTERFACE_FOLDER, path)).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/mindflex': BaseNamespace})
            print 'socketio ready'
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print '''Listening on port 8080 
             and on port 10843 (flash policy server)'''
    server = SocketIOServer(('0.0.0.0', 8080), 
                            Application(),
                            resource="socket.io", 
                            policy_server=True,
                            policy_listener=('0.0.0.0', 10843))
    connection = MindFlexConnection()
    gevent.spawn(read_mindflex, server, connection)
    server.serve_forever()
