class BaseActor():
    async def _hook_loop(self, loop):
        pass

    def subscriptions(self):
        raise NotImplementedError()

    def share_subscriptions(self):
        return False

    async def event(self, topic, message):
        raise NotImplementedError()

    def publish(self, topic: str, message: bytes):
        raise NotImplementedError()
