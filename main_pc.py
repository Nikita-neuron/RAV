
from services import ServiceManager, Service

def pc():
    import service_interface as interface
    webserver = interface.root['webserver']
    while 'keyboard' not in webserver:
        pass
    keyboard_stream = webserver['keyboard']
    while True:
        print('Recv:', keyboard_stream.recv())


if __name__ == '__main__':
    manager = ServiceManager([
        Service('webserver', module_filename='web/server.py'),
        Service('pc', function=pc)
    ])
    manager.serve()

