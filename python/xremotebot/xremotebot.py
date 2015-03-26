import json
import time
import websocket
import ssl

wait = time.sleep



if str is not bytes:
    unicode = str

class Server(object):
    def __init__(self, url, api_key, ignore_ssl = False):
        self.url= url
        if ignore_ssl:
            self.ws = websocket.create_connection(url)
        else:
            self.ws = websocket.create_connection(
                url,
                sslopt={"cert_reqs": ssl.CERT_NONE}
            )

        if self.authentication_required():
            if not self.authenticate(api_key):
                raise Exception('Authentication failed')

    def send_ws_msg(self, entity, method, *args):
        msg = json.dumps({
            'entity': entity,
            'method': method,
            'args': args,
        })
        print(msg) # FIXME
        self.ws.send(msg)
        response = json.loads(self.ws.recv())
        print(response) # FIXME
        if response['response'] == 'error':
            raise Exception(response['message'])

        return response['value']

    def authentication_required(self):
        return self.send_ws_msg('global', 'authentication_required')

    def authenticate(self, api_key):
        return self.send_ws_msg('global', 'authenticate', api_key)

    def get_robots(self):
        return self.send_ws_msg('global', 'get_robots')

    def fetch_robot(self):
        return self.send_ws_msg('global', 'fetch_robot')


def timed(delayed_func, time_index=2):
    def _timed(wrapped_func):
        def _f(self, *args, **kwargs):
            _f.__name__ = wrapped_func.__name__ + '_wrapped'
            _f.__doc__ = wrapped_func.__doc__
            time = None
            args = list(args)
            if len(args) == time_index:
                time = args.pop()
            elif 'time' in kwargs:
                time = kwargs.pop('time')

            wrapped_func(self, *args, **kwargs)
            if time is not None:
                wait(time)
                delayed_func(self)

        return _f
    return _timed

def _stop_robot(s):
    s.stop()

class Robot(object):
    def __init__(self, server, robot_model, robot_id):
        self.server = server
        self.robot_model = robot_model
        self.robot_id = robot_id

    def send_ws_msg(self, msg, *args):
        self.server.send_ws_msg(
            'robot',
            msg,
            self.robot_model,
            self.robot_id,
            *args
        )

    @timed(_stop_robot)
    def forward(self, speed=50, time=-1):
        self.send_ws_msg('forward', speed)

    @timed(_stop_robot)
    def backward(self, speed=50, time=-1):
        self.send_ws_msg('backward', speed)

    @timed(_stop_robot)
    def turnLeft(self, speed=50, time=-1):
        self.send_ws_msg('turnLeft', speed)

    @timed(_stop_robot)
    def turnRight(self, speed=50, time=-1):
        self.send_ws_msg('turnRight', speed)

    def stop(self):
        self.send_ws_msg('stop', speed)

    def ping(self):
        return self.send_ws_msg('ping', speed)

    def getObstacle(self, *args):
        return self.send_ws_msg('getObstacle', *args)

if __name__ == '__main__':
    server = Server('ws://xremotebot.example:8000/api', '33dfb770-b3d2-49da-81f2-745af2c643f1')
    print(server.get_robots())
    robot = server.fetch_robot()
    robot.forward(100)
    wait(1)
    robot.stop()
    robot.turnRight(100, 2)
