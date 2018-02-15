from __future__ import absolute_import

import os

from .base import sync_wrapper
from .auth import AuthClient


ARRAY_URL = os.environ.get('CLOUDSTRYPE_ARRAY_URL', 'http://array/')


class ArrayClient(AuthClient):
    base_url = ARRAY_URL

    def __init__(self, *args, **kwargs, replicas=1):
        super().__init__(*args, **kwargs)
        self.replicas = replicas

    async def put(self, chunk_id, params=None, replicas=None):
        replicas = replicas or self.replicas
        params = params or {}
        params.setdefault('replicas', replicas)
        return await self.request('POST', '/chunk/', params=params)

    put_sync = sync_wrapper(put)

    async def get(self, chunk_id, params=None):
        return await self.request(
            'GET', '/chunk/%s/' % chunk_id, params=params)

    get_sync = sync_wrapper(get)
