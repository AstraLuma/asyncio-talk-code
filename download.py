import asyncio
import aiohttp
import aiofiles
import traceback
import sys


async def get_urllist():
    async with aiofiles.open('urls.txt', 'rt') as fo:
        async for line in fo:
            yield line.strip()


async def fetch(session, url):
    async with session.get(url) as response:
        return len(await response.read())


async def main(argv):
    urls = [url async for url in get_urllist()]

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(fetch(session, url))
            for url in urls
        ]

        size = 0
        for fut in asyncio.as_completed(tasks):
            try:
                size += await fut
            except Exception:
                traceback.print_exc()
            else:
                print("So far:", size)

    print("Total download:", size)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    loop.close()
