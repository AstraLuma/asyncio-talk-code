import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)
    # print() is already buffered by Python, IPC Pipes, etc
    # You should still async it, but it's only going to bite
    # when other things go wrong.


loop = asyncio.get_event_loop()
loop.run_until_complete(say('Hello, World!', 1))
loop.close()
