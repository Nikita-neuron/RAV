
from services import ServiceManager, Service

if __name__ == '__main__':
    manager = ServiceManager([
        Service('webserver', module_name='test_AAA_ws'),
        Service('pc', module_name='test_AAA_pc')
    ])
    manager.serve()

