
class WSMockBase:
    action = lambda x: x
    def __init__(self, *args, **kwargs):
        pass

    def send(self, msg):
        return self.action(msg)

    def close(self):
        pass

