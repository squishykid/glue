class BaseActor():
    async def _hook_loop(self, loop):
        pass

    def subscriptions(self):
        raise NotImplementedError()

    async def event(self, topic, message):
        raise NotImplementedError()

    def publish(self, topic, message):
        raise NotImplementedError()
