import asyncio
ioloop = asyncio.get_event_loop()

async def f():
    await asyncio.sleep(1)
    print('f')
async def g():
    await asyncio.sleep(2)
    print('g')
tasks = map(asyncio.create_task, [f(), g()])

ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.close()
