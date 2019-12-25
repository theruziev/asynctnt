import secrets

import asyncio
import time

import uvloop

from asynctnt import Connection as ConnectionAsyncTnt

from aiotarantool import Connection as ConnectionAIOTarantool

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HOST = '127.0.0.1'
PORT = 3305
USERNAME = 't1'
PASSWORD = 't1'


async def main():
    datas = [
        [i, secrets.token_hex(15)] for i in range(10000)
    ]
    loop = asyncio.get_event_loop()
    conn_asynctnt = await create_asynctnt(loop)
    conn_aiotnt = await create_aiotarantool(loop)

    await conn_asynctnt.eval("box.space.tester:truncate()")
    await insert_asynctnt(conn_asynctnt, datas)
    await update_asynctnt(conn_asynctnt, datas)
    await select_asynctnt(conn_asynctnt, datas)
    await select_1k_asynctnt(conn_asynctnt, datas)
    await delete_asynctnt(conn_asynctnt, datas)

    await conn_asynctnt.eval("box.space.tester:truncate()")
    await insert_aiotarantool(conn_aiotnt, datas)
    await update_aiotarantool(conn_aiotnt, datas)
    await select_aiotarantool(conn_aiotnt, datas)
    await select_1k_aiotarantool(conn_aiotnt, datas)
    await delete_aiotarantool(conn_aiotnt, datas)


async def select_asynctnt(conn: ConnectionAsyncTnt, datas):
    t = time.monotonic()
    for (key, _) in datas:
        await conn.select("tester", [key])

    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[asynctnt] select Elapsed:{elapsed} RPS: {rps}")


async def select_1k_asynctnt(conn: ConnectionAsyncTnt, datas):
    t = time.monotonic()
    res = await conn.select("tester", limit=1000)
    elapsed = time.monotonic() - t
    print(f"[asynctnt] select 1k Elapsed:{elapsed}")


async def insert_asynctnt(conn: ConnectionAsyncTnt, datas):
    t = time.monotonic()
    for d in datas:
        await conn.insert("tester", d)

    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[asynctnt] insert Elapsed:{elapsed} RPS: {rps}")


async def update_asynctnt(conn: ConnectionAsyncTnt, datas):
    t = time.monotonic()
    for (key, _) in datas:
        await conn.update("tester", [key], [("=", 1, secrets.token_hex(15))])

    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[asynctnt] update Elapsed:{elapsed} RPS: {rps}")


async def delete_asynctnt(conn: ConnectionAsyncTnt, datas):
    t = time.monotonic()
    for (key, _) in datas:
        await conn.delete("tester", [key])
    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[asynctnt] delete Elapsed:{elapsed} RPS: {rps}")


# AIOTARANTOOL

async def select_aiotarantool(conn: ConnectionAIOTarantool, datas):
    t = time.monotonic()
    for (key, _) in datas:
        await conn.select("tester", [key])

    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[aiotarantool] select Elapsed:{elapsed} RPS: {rps}")


async def select_1k_aiotarantool(conn: ConnectionAsyncTnt, datas):
    t = time.monotonic()
    await conn.select("tester", limit=1000)
    elapsed = time.monotonic() - t
    print(f"[aiotarantool] select 1k Elapsed:{elapsed}")


async def insert_aiotarantool(conn: ConnectionAIOTarantool, datas):
    t = time.monotonic()
    for d in datas:
        await conn.insert("tester", d)

    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[aiotarantool] insert Elapsed:{elapsed} RPS: {rps}")


async def update_aiotarantool(conn: ConnectionAIOTarantool, datas):
    t = time.monotonic()
    for (key, _) in datas:
        await conn.update("tester", key, [("=", 1, secrets.token_hex(15))])

    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[aiotarantool] update Elapsed:{elapsed} RPS: {rps}")


async def delete_aiotarantool(conn: ConnectionAIOTarantool, datas):
    t = time.monotonic()
    for (key, _) in datas:
        await conn.delete("tester", key)
    elapsed = time.monotonic() - t
    rps = len(datas) / elapsed
    print(f"[aiotarantool] delete Elapsed:{elapsed} RPS: {rps}")


async def create_asynctnt(loop):
    import asynctnt
    conn = asynctnt.Connection(host=HOST,
                               port=PORT,
                               username=USERNAME,
                               password=PASSWORD,
                               reconnect_timeout=1,
                               fetch_schema=True,
                               auto_refetch_schema=True,
                               loop=loop)
    await conn.connect()
    return conn


async def create_aiotarantool(loop):
    import aiotarantool
    conn = aiotarantool.connect(HOST, PORT,
                                user=USERNAME,
                                password=PASSWORD,
                                loop=loop)
    await conn.connect()
    return conn


if __name__ == '__main__':
    asyncio.run(main())
