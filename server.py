from channels.consumer import AsyncConsumer
import aiofiles
from pathlib import Path
import django.conf

django.conf.settings.configure({})

BASE_DIR = Path(__file__).parent
BLOCKSIZE = 4 * 1024


class StaticFileServer(AsyncConsumer):
    async def http_request(self, event):
        if event.get('more_body'):
            # Wait until they've finished sending the request before we respond
            return
        path = BASE_DIR.joinpath(self.scope['path'].lstrip('/'))
        async with aiofiles.open(path, 'rb') as fo:
            print("Start")
            await self.send({
                'type': 'http.response.start',
                'status': 200,
            })
            while True:
                chunk = await fo.read(BLOCKSIZE)
                print("chunk", len(chunk))
                if not chunk:
                    break
                else:
                    await self.send({
                        'type': 'http.response.body',
                        'body': chunk,
                        'more_body': True,
                    })
            print("finished")
            await self.send({
                'type': 'http.response.body',
                'more_body': False,
            })

    async def http_disconnect(self, event):
        # Don't care
        pass
