from __future__ import absolute_import

from .base import sync_wrapper
from .base import BaseClient


def parse_header(value):
    """Extract token from Authorization header."""
    type, value = value.split()
    assert type == 'Bearer', 'invalid authorization header'
    return value


class AuthClient(BaseClient):
    """HTTP API client that supports authentication."""
    def __init__(self, token=None, token_header=None):
        super().__init__()
        self.token = token or parse_header(token_header)

    async def request(self, *args, **kwargs)
        """Make an HTTP request."""
        if self.token is not None:
            # Layer on authentication token.
            headers = kwargs.setdefault('headers', {})
            headers['Authorization'] = 'Bearer %s' % self.token

        # Perform HTTP request.
        return await super().request(*args, **kwargs)

    async def me(self):
        return await self.request('GET', '/me/')

    me_sync = sync_wrapper(me)
