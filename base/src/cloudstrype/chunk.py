from __future__ import absolute_import

import os
import uuid

from .base import sync_wrapper
from .base import BaseClient


CHUNK_URL = os.environ.get('CLOUDSTRYPE_CHUNK_URL', 'http://chunk/')


class ChunkClient(BaseClient):
    base_url = CHUNK_URL

    def __init__(self, *args, **kwargs, durability='none'):
        super().__init__(*args, **kwargs)
        self.durability = durability

    async def put(self, data, **params):
        params.setdefault('durability', self.durability)
        return self.request('PUT', '/chunk/', params=params, data=data)

    put_sync = sync_wrapper(put)

    async def delete(self, chunk_id):
        return self.request('DELETE', '/chunk/%s' % chunk_id)

    delete_sync = sync_wrapper(delete)

    async def get(self, chunk_id):
        return self.request('GET', '/chunk/%s' % chunk_id)

    get_sync = sync_wrapper(get)
