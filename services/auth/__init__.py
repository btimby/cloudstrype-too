import asyncio
import os

from aiopg.sa import create_engine

from aiohttp import web

from . import models


POSTGRES_URL = os.environ.get('POSTGRES_URL', 'postgresql://postgres')


class AuthApi(object):
    def __init__(self):
        self.pgsql = await create_engine(POSTGRES_URL)
        models.create_tables(self.pgsql)

    async def on_shutdown(self):
        self.pgsql.close()
        await self.pgsql.wait_closed()

    async def put(self, request):
        pass

    async def delete(self, request):
        pass

    async def get(self, request):
        id = request.match_info.get('id')

        async with self.pgsql.acquire() as c:
            await c.execute(User.select(id=id))

    async def me(self, request):
        pass


class ArrayServer(object):
    def __init__(self):
        self.clients = {}

    async def handle_client(self, request, writer):
        pass


def main():
    app, api = web.Application(), AuthApi() 

    app.router.add_put('/user/', api.put)
    app.router.add_delete('/user/{id}/', api.delete)
    app.router.add_get('/user/me/', api.me)
    app.router.add_get('/user/{id}/', api.get)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        asyncio.start_server(server.handle_client, bind, port))
    loop.create_server(app.make_handler(), bind, 8080)


if __name__ == '__main__':
    main()
