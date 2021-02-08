
import unittest
from unittest import mock
import os
import threading
from services import ServiceManager, Service

class TestServiceManager(unittest.TestCase):
    temp_modules = {
        'test_services_webserver': '''

import logging
import multiprocessing as mp
import service_interface as interface
def service_main():
    this = interface.services_root['webserver']
    keyboard_pipe_recv, keyboard_pipe_send = mp.Pipe(False)
    this['keyboard'] = keyboard_pipe_recv
    interface.services_root['webserver'] = this
    print('Set pipe')
    while True:
        keyboard_pipe_send.send('Hello, World!')
    print('WEBSERVER')

''',
        'test_services_raspberry': '''

import service_interface as interface
def service_main():
    webserver = interface.services_root['webserver']
    print(webserver)
    while 'keyboard' not in webserver:
        # print(webserver)
        pass
    print('AAA')
    keyboard_pipe = webserver['keyboard']
    while True:
        print(keyboard_pipe.recv())
    # print('RASPBERRY')

'''
    }
    def _create_files(self):
        for filename, code in self.temp_modules.items():
            with open(filename+'.py', 'w') as f:
                f.write(code)
    def setUp(self):
        self._create_files()
    def test_main(self):
        manager = ServiceManager([
            Service('webserver', module_name='test_services_webserver'),
            Service('raspberry', module_filename='./test_services_raspberry.py')
        ])
        manager_thread = threading.Thread(target=manager.serve)
        manager_thread.start()
        
        manager_thread.join()
    def tearDown(self):
        for filename in self.temp_modules:
            os.remove(filename+'.py')


if __name__ == '__main__':
    unittest.main()
