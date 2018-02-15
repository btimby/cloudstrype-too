import asyncio
import aiohttp


def sync_wait(f, *args, **kwargs):
    """Run coroutine synchronously and return result."""
    loop = kwargs.pop('loop', None)

    if loop is None:
        loop = asyncio.get_event_loop()

    return loop.run_until_complete(f(*args, **kwargs))


def sync_wrapper(f):
    """Decorator that turns coroutine into blocking function."""
    def inner(*args, **kwargs):
        return sync_wait(f, *args, **kwargs)

    return inner


class BaseClient(object):
    base_url = None

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def request(self, method, url, params=None):
        url = urljoin(self.base_url, url)

        async with self.session as s:
            try:
                request = getattr(s, method)
            except AttributeError:
                raise AssertionError('Invalid HTTP method: %s' % method)

            async with request(url, params=data) as r:
                return r

    request_sync = sync_wrapper(request)
