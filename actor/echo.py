from actor import BaseActor

class Actor(BaseActor):
    def subscriptions(self):
        return ['ping/#']

    async def event(self, topic, event):
        print('event', topic, event)
        self.publish(f'pong/{topic}', event)