#!/usr/bin/env python3.6

import aio


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
    loop.run_until_complete(aio.sleep(1), tick(0.01, 10), aio.suspend(0))
    loop.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
