import asyncio
import os
import signal
import time

from gmqtt import Client as MQTTClient

# gmqtt also compatibility with uvloop  
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


STOP = asyncio.Event()


def ask_exit(*args):
    STOP.set()


def load_actor(name):
    import importlib
    module = importlib.import_module(name)
    return module


class ActorAdapter():
    def __init__(self, actor, client):
        self.actor = actor
        self.client = client
        self.actor.publish = self.publish
    def publish(self, topic, message):
        self.client.publish(topic, str(message), qos=1)

    def on_message(self, client, topic, payload, qos, properties):
        print('AAARECV MSG:', payload)

    def on_connect(self, client, flags, rc, properties):
        print('connected')
        for sub in self.actor.subscriptions():
            client.subscribe(sub, qos=0)

    async def on_message(self, client, topic, payload, qos, properties):
        print('aaaRECV MSG:', payload)
        await self.actor.event(topic, payload)
        return 0

    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_subscribe(self, client, mid, qos, properties):
        print('SUBSCRIBED')

async def main(broker_host, actor_name, loop):
    actor = load_actor(actor_name).Actor()
    client_name = f'{os.getpid()}:{actor_name}'
    client = MQTTClient(client_name)
    aa = ActorAdapter(actor, client)

    client.on_connect = aa.on_connect
    client.on_message = aa.on_message
    client.on_disconnect = aa.on_disconnect
    client.on_subscribe = aa.on_subscribe

    await client.connect(broker_host)
    await actor._hook_loop(loop)

    client.publish('TEST/TIME', str(time.time()), qos=1)

    await STOP.wait()
    await client.disconnect()


def enter(actor):
    loop = asyncio.get_event_loop()

    host = 'localhost'

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(host, actor, loop))

if __name__ == '__main__':
    enter('actor.echo.Echo')