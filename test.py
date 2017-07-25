#!/usr/bin/env python3
import socket

import aio
from aio.traps import IO


async def server(addr):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(100)
    sock.setblocking(False)
    print('Waiting for connection on {}'.format(addr))
    await IO.readable(sock)
    conn, addr = sock.accept()
    sock.close()
    print('Connection from {!r}'.format(addr))
    conn.setblocking(False)
    conn.close()


async def tick(interval, count):
    jitter = 0
    tick = aio.time()
    for i in range(count):
        tick += interval
        actual = await aio.suspend(tick)
        offset = actual - tick
        print('tick {} (offset: {})'.format(i, offset))
        jitter += offset
    return jitter / count


def main():
    loop = aio.EventLoop()
    tasks = [
        aio.sleep(1),
        tick(0.01, 10),
        aio.suspend(0),
        server(('127.0.0.1', 1111)),
    ]
    loop.run_until_complete(*tasks)
    loop.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
