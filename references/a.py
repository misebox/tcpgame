import asyncio
import time

async def hello_world(n):
    await asyncio.sleep(1)
    print("{}: Hello World!".format(n))

async def call_hello_world1():
    print("call_hello_world1()")
    co = []
    co.append(hello_world(1))
    co.append(hello_world(1))
    co.append(hello_world(1))
    await asyncio.gather(*co)
    
    await asyncio.sleep(2)
    await hello_world(1)
    return 1

async def call_hello_world2():
    print("call_hello_world2()")
    await hello_world(2)
    await asyncio.sleep(2)
    return 2

# loop = asyncio.get_event_loop()
# loop.create_task(call_hello_world1())
async def main():
    rets = await asyncio.gather(call_hello_world1(), call_hello_world2())
    print(rets)
# loop.run_until_complete(call_hello_world2())

asyncio.run(main())
