import os
import json
import uuid

import aioredis

from aiohttp import web

from cloudstrype import AuthClient
from cloudstrype import ArrayClient
from cloudstrype import CloudClient


REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis')


def _raid(chunk_id, data, scheme):
    """Build raid replicas."""
    scheme, count = scheme.split('-')

    try:
        count = int(count)
    except ValueError:
        raise AssertionError('invalid raid count: %s' % count)

    if scheme == 'raid1':
        for i in range(count):
            yield '%s-%s-%i' % (chunk_id, scheme, i), data

    else:
        raise AssertionError('unsupported raid level: %s' % scheme)


def replicate(chunk_id, data, scheme):
    """
    Builds replica blocks for storage.

    Supports various raid levels now. In the future, may support EC.
    """
    if scheme == 'none':
        yield chunk_id, data

    elif scheme.startswith('raid'):
        yield from _raid(chunk_id, data, scheme)

    else:
        raise AssertionError('unsupported durability scheme: %s' % scheme)


async def get_chunk(request):
    chunk_id = request.match_info.get('chunk_id')


class ChunkApi(object):
    def __init__(self):
        self.redis = await aioredis.create_redis(REDIS_URL)

    async def put(self, request):
        auth = AuthClient(token_header=request['Authorization'])

        # TODO: check authorization, raise.
        user_info = auth.me()

        clients = repeat([
            ArrayClient(token=auth.token),
            CloudClient(token=auth.token),
        ])

        data = await request.data()
        durability = request.params['durability']

        chunk_id = str(uuid.uuid4())

        futures = []
        for replica_id, replica in replicate(chunk_id, data, durability)
            client = next(client)
            futures.append(client.put(replica_id, replica))

        done, _ = await asyncio.wait(futures)

        obj = {
            'chunk_id': chunk_id,
        }

        for future in done:
            try:
                r = future.result()
            except Exception as e:
                raise
            obj.setdefault('replicas', []).append(r)

        # Store data into redis transactionally.
        pipe = self.redis.pipeline()
        pipe.set()
        pipe.set()

        await pip.execute()

        return web.Response(
            json.dumps(obj), content_type='application/json', status=201)

    async def get(self, request):
        chunk_id = request.match_info.get('id')
        chunk_info = await self.redis.get(chunk_id)

        # TODO: try to read data from client.

    async def delete(self, request):
        pass


def main():
    app, api = web.Application(), ChunkApi()

    app.router.add_put('/chunk/', api.put)
    app.router.add_delete('/chunk/{id}/', api.delete)
    app.router.add_get('/chunk/{id}/', api.get)

    web.run_app(app)


if __name__ == '__main__':
    main()
