from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import livereload
import time

async_mode = None

app = Flask(__name__, template_folder='web/templates/')
# app = Flask(__name__)

# app.config['SECRET_KEY'] = 'Super secret!!!!'
socketio = SocketIO(app, async_mode=async_mode)

# def update_index():
#     i = 0
#     with app.app_context(), app.test_request_context():
#         while True:
#             yield render_template('index.html', tim=str(i))
#             yield f'{i}<br/>'
#             i += 1
#             time.sleep(1)

@app.route('/')
def hello_world():
    return render_template('index.html', async_mode=socketio.async_mode)
    # return Response(update_index())

class SocketIOEvents:
    def __init__(self, keyboard_out):
        self.keyboard_out = keyboard_out
        # self.socketio = SocketIO(app)
        socketio.on_event('keyboard', self.handle_keyboard, namespace='/')
    def handle_keyboard(self, data):
        print('RECEIVED:', data)
        self.keyboard_out.send(data)

@socketio.on('connect')
def handle_connect():
    print('CONNECT')

def run():
    # app.debug = True
    # livereload.Server(app.wsgi_app).serve(port=5500)
    # app.run(host='localhost'    , port=5500)
    # TODO: GAVNOOOOOOOOOOOOOOOO ГАВНИИИИИ
    SocketIOEvents(None)
    socketio.run(app, port=22869, debug=False)

def service_main():
    import service_interface as interface
    from service_interface import root
    import time


    keyboard_stream = root.setup_interface({
        'keyboard': interface.Pipe
    })[0]

    print('out', keyboard_stream)
    print('in', root['webserver'])
    print('WEBSERVER', interface.root)
    # while True:
    #     keyboard_stream.send('Hello, PC!')
    #     time.sleep(1)
    SocketIOEvents(keyboard_stream)
    socketio.run(app, host='localhost', port=22869)


if __name__ == '__main__':
    run()    
