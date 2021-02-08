import service_interface as interface
# from service_interface import root
webserver = interface.root['webserver']
print('PC', interface.root)
while 'keyboard' not in webserver:
    pass
keyboard_stream = webserver['keyboard']
while True:
    print('Recv:', keyboard_stream.recv())
