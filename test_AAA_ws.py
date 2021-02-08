import service_interface as interface
from service_interface import root
import time
keyboard_stream = root.setup_interface({
    'keyboard': interface.Pipe
})[0]

print('out', keyboard_stream)
print('in', root['webserver'])
print('WEBSERVER', interface.root)
while True:
    keyboard_stream.send('Hello, PC!')
    time.sleep(1)
