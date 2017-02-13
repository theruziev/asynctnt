import asyncio
# import uvloop; asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import logging

from asynctnt.instance import TarantoolInstance, TarantoolDockerInstance


async def main(t, loop):
    await t.start()
    data = await t.command("box.info.status")
    print(data)
    await t.stop()

    await t.start()
    data = await t.command("box.info.status")
    print(data)
    await t.stop()
    # await t.wait_stopped()


logging.basicConfig(level=logging.DEBUG)
event_loop = asyncio.get_event_loop()
asyncio.set_event_loop(None)
asyncio.get_child_watcher().attach_loop(event_loop)

t = TarantoolInstance(
    host='unix/',
    port='/tmp/_mytnt.sock',
    console_host='127.0.0.1',
    loop=event_loop,
    applua=open('../tests/files/app.lua').read())
try:
    event_loop.run_until_complete(main(t, event_loop))
    # event_loop.run_until_complete(t.start())
    # event_loop.run_until_complete(t.wait_stopped())
except KeyboardInterrupt:
    event_loop.run_until_complete(t.stop())
finally:
    event_loop.close()
