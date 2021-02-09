
import multiprocessing as mp
import multiprocessing.managers as mp_managers
import logging
import sys
from pathlib import Path
import importlib
from types import ModuleType
import cmd
import time

from util import LoggerAsFile, first_not_none
# from services_cmd import ServiceManagerCmd
from services_root_manager import ServicesRootManager


def configure_logging():
    import logging.config
    import multiprocessing_logging

    # From: https://stackoverflow.com/a/11927374
    # Docs: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'mp_style': {
                'format': '[%(levelname)s/%(processName)s] %(message)s'
            }
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'stream': sys.stdout
            }
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                # 'propagate': False
            }
        }
    }
    logging.config.dictConfig(logging_config)

    multiprocessing_logging.install_mp_handler()
    mp_logger = mp.log_to_stderr()
    mp_logger.setLevel(logging.WARNING)
    # sys.stdout = LoggerAsFile(logging.getLogger(__name__))


class Service(mp.Process):
    def _load_main(self, function, module, module_name, module_filename) -> 'Callable':
        if function is not None:
            # self._needs_global_setup = False
            return function
        elif module is not None:
            pass
        elif module_name is not None:
            module = importlib.import_module(module_name)
        elif module_filename is not None:
            spec = importlib.util.spec_from_file_location(self.raw_name, module_filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            raise ValueError('Could not load main (no values specified)')
        
        if not hasattr(module, 'service_main'):
            raise ValueError(f'Could not load service_main (no "service_main" found in module "{module}")')
        return module.service_main
    def _interface_setup(self):
        import service_interface as interface
        interface.root = self.root_manager
        interface.service = self
    def __init__(self, name=None, function=None, module=None, module_name=None, module_filename=None):
        '''
        Параметры
        ----------
        name: str, optional
            Необязательно. Если значение не установлено, автоматически определяется из следующих параметров.
        function, module, module_name, module_filename
            Нужно задать один их этих параметров.
        '''
        self._init_args = (function, module, module_name, module_filename)

        if name is not None:
            pass
        elif (obj := first_not_none([function, module])) is not None:
            name = obj.__name__
        elif module_name is not None:
            name = module_name
        elif module_filename is not None:
            name = Path(module_filename).stem
        else:
            raise ValueError('Supply one of (function, module, module_name, module_filename)')
        self.raw_name = name
        name = f'Service{name.capitalize()}'
        
        self.logger = logging.getLogger(name)
        self.outputs = {}
        # self.manager = manager
        super().__init__(
            name=name,
        )
    def reload(self):
        self.terminate()
        self.start()
    def run(self):
        configure_logging()
        sys.stdout = LoggerAsFile(self.logger)

        self._interface_setup()
        self._target = self._load_main(*self._init_args)

        super().run()

'''
### WEBSERVER
this = services_root.setup_interface({
    'keyboard': interface.Pipe
})
keyboard = this['keyboard']
while True:
    keyboard.send('Hello, Raspberry!')

### RASPBERRY
keyboard = services_root['webserver']['keyboard']
while True:
    print('Received:', keyboard.recv())
'''

# if __name__ == "__main__":
#     import service_interface as interface
#     interface.service = Service('tezt')
    
#     root = ServicesRootManager(['tezt'])
#     keyboard, *_ = root.setup_interface({
#         'keyboard': interface.Pipe
#     })
#     print('out', keyboard)
#     print('in', root['tezt'])
#     raise 1

class ServiceManager:
    '''
    Главный класс сервисов.
    Параметры
    ---------
    services
        Список сервисов. Каждый элемент может быть `Service'ом`, функцией, модулем, именем модуля или его путём к файлу модуля.
        В каждом модуле должна быть функция `service_main` или `main` (`main` запускается если `service_main` не найдена)/
        !!!ВНИМАНИЕ!!!:
        Вложенные функции, лямбды и модули не работают т.к. говноpickle не может их сериализовать.
        TODO: Можно просто брать имя модуля и передавать конструктору Service'а. Для всего остального можно использовать модуль `dill`
    '''
    def __init__(self, services, command_prompt=False):
        configure_logging()
        self.services = []
        for service in services:
            if isinstance(service, Service):
                pass
            elif callable(service):
                service = Service(function=service)
            elif isinstance(service, ModuleType):
                service = Service(module=service)
            elif type(service) == str:
                service = Service(module_name=service)
            elif isinstance(service, Path):
                service = Service(module_filename=service)
            else:
                raise ValueError(f'Unknown object {service}')
            self.services.append(service)
        self.root_manager = ServicesRootManager(self.services)
        for service in self.services:
            service.root_manager = self.root_manager
    def serve(self):
        '''
        Начинает работу менеджера.
        '''
        print('Starting services...')
        for service in self.services:
            service.start()
        for service in self.services:
            service.join()
        # ServiceManagerCmd(self).cmdloop()

def webserver():
    import service_interface as interface
    from service_interface import root
    keyboard_stream = root.setup_interface({
        'keyboard': interface.Pipe
    })[0]

    print('out', keyboard_stream)
    print('in', root['webserver'])
    print('WEBSERVER', interface.root)
    while True:
        keyboard_stream.send('Hello, PC!')
        time.sleep(1)
def pc():
    import service_interface as interface
    # from service_interface import root
    webserver = interface.root['webserver']
    print('PC', interface.root)
    while 'keyboard' not in webserver:
        pass
    keyboard_stream = webserver['keyboard']
    while True:
        print('Recv:', keyboard_stream.recv())



def main():
    manager = ServiceManager([webserver, pc])
    manager.serve()
if __name__ == "__main__":
    main()

