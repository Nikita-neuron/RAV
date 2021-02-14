
import sys
sys.path.append('..')
import rav.config

from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import livereload

import time
from twisted.internet import protocol, reactor
import threading


async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def hello_world():
    return render_template('index.html', async_mode=socketio.async_mode)
    # return Response(update_index())

@socketio.on('connect')
def handle_connect():
    print('WEBSOCKET CONNECT')


class PcClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print('Connected to main server!')
class PcClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        print('Connected to main pc', addr)
        return PcClientProtocol()
    def clientConnectionLost(self, connection, reason):
        print('Connection lost!', connection, reason)
    def clientConnectionFailed(self, connection, reason):
        print('Connection failed!', connection, reason)


def run_webserver():
    print('Starting webserver')
    socketio.run(app, host='localhost', port=rav.config.WEBSERVER_PORT, debug=False)

def main():
    # app.debug = True
    # livereload.Server(app.wsgi_app).serve(port=5500)
    # app.run(host='localhost'    , port=5500)
    # TODO: GAVNOOOOOOOOOOOOOOOO ГАВНИИИИИ
    threading.Thread(target=run_webserver).run()
    reactor.connectTCP(rav.config.MAIN_PC_IP, rav.config.MAIN_PC_PORT, PcClientFactory())
    reactor.run()
    


if __name__ == '__main__':
    main()    


# def service_main():
#     import service_interface as interface
#     from service_interface import root
#     import time


#     keyboard_stream = root.setup_interface({
#         'keyboard': interface.Pipe
#     })[0]

#     print('out', keyboard_stream)
#     print('in', root['webserver'])
#     print('WEBSERVER', interface.root)
#     # while True:
#     #     keyboard_stream.send('Hello, PC!')
#     #     time.sleep(1)
#     SocketIOEvents(keyboard_stream)
#     socketio.run(app, host='localhost', port=rav.config.WEBSERVER_PORT)