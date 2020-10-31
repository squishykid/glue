from actor import BaseActor

class Actor(BaseActor):
    def subscriptions(self):
        return ['http/req/#']

    async def event(self, topic, event):
        print('event', topic, event)
        topic = f'http/resp/{topic[9:]}'
        self.publish(topic, "hello")