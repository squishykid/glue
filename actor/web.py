from actor import BaseActor
import random

me = random.randint(0,9)
reply = f"f{me}hello"

class Actor(BaseActor):
    def subscriptions(self):
        return ['$share/web/http/req/#']

    async def event(self, topic, event):
        print('event', topic, event)
        topic = f'http/resp/{topic[9:]}'
        self.publish(topic, reply)