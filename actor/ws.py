from actor import BaseActor
from aiohttp import web
import asyncio

class Actor(BaseActor):
    async def _hook_loop(self, loop):
        self.conntrack = {}
        server = web.Server(self.handler)
        await loop.create_server(server, "127.0.0.1", 8081)

    async def handler(self, request):
        peername = request.transport.get_extra_info('peername')
        assert peername is not None
        host, port = peername

        event = asyncio.Event()
        self.conntrack[peername] = event
        self.publish(f'ws/req/{host}/{port}', request.rel_url)
        await event.wait()

        res = self.conntrack.get(peername)
        thing = 'something fucked up'
        if res is not None:
            thing = res
        del self.conntrack[peername]
        return web.Response(text=thing)

    def subscriptions(self):
        return ['ws/resp/#']

    async def event(self, topic, message: bytes):
        print('wsevent', topic, message)
        elements = topic.split('/')
        peername = elements[2], int(elements[3])
        event = self.conntrack.get(peername)
        if event is None:
            print('UNKNOWN', topic, message, self.conntrack, peername)
            return
        self.conntrack[peername] = str(message)
        event.set()
        
