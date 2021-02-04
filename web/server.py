from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import livereload
import time

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super secret!!!!'
socketio = SocketIO(app, async_mode=async_mode)

def update():
    i = 0
    with app.app_context(), app.test_request_context():
        while True:
            yield render_template('index.html', tim=str(i))
            # yield f'{i}<br/>'
            i += 1
            time.sleep(1)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html', async_mode=socketio.async_mode)
    # return Response(update())

@socketio.on('keyboard')
def handle_event(data):
    print('RECEIVED:', data)

@socketio.on('connect')
def handle_connect():
    print('CONNECT')

def run():
    app.debug = True
    # livereload.Server(app.wsgi_app).serve(port=5500)
    # app.run(host='localhost'    , port=5500)
    socketio.run(app, host='localhost', port=5500)

if __name__ == '__main__':
    run()    
