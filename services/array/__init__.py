import os

import asyncio
import aioredis

from aiohttp import web


REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis')


class ArrayApi(object):
    def __init__(self):
        self.redis = await aioredis.create_redis(REDIS_URL)

    async def on_shutdown(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def put(self, request):
        pass

    async def delete(self, request):
        pass

    async def get(self, request):
        pass


class ArrayServer(object):
    def __init__(self):
        self.clients = {}

    async def handle_client(self, request, writer):
        pass


def main():
    server = ArrayServer()
    app, api = web.Application(), ArrayApi(server) 

    app.router.add_put('/chunk/', api.put)
    app.router.add_delete('/chunk/{id}/', api.delete)
    app.router.add_get('/chunk/{id}/', api.get)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        asyncio.start_server(server.handle_client, bind, port))
    loop.create_server(app.make_handler(), bind, 8080)


if __name__ == '__main__':
    main()
