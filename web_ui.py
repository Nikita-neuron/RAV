import eel
import asyncio
import threading

# @eel.expose
# def say_hello_py(x):
#     print('Hello from %s' % x)


class MsgReceiver:
    def __init__(self):
        self._queue = asyncio.Queue(maxsize=256)
    async def __aiter__(self):
        while True:
            await self._queue.get()
    

messages = MsgReceiver()

@eel.expose
def process_keys(keys):
    print('keys:', keys)
    messages._queue.put(keys)


async def start_eel():
    eel.init('web')

    # say_hello_py('Python World!')
    # eel.say_hello_js('Python World!')
    
    eel.start('index.html', size=(300, 200))


    

