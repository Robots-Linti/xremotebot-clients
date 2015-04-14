# -*- coding: utf-8 -*-
import json
import time
import websocket
import ssl

wait = time.sleep

if str is not bytes:
    unicode = str


class Server(object):

    def __init__(self, url, api_key='', wsbase=None, ignore_ssl=False):
        self.url = url
        if wsbase is not None:
            self.ws = wsbase()
        else:
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
        self.ws.send(msg)
        response = json.loads(self.ws.recv())
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

    def reserve(self, robot_model, robot_id):
        return self.send_ws_msg('global',
                                'reserve',
                                robot_model,
                                robot_id)



def timed(delayed_func, time_index=2):
    """
    Esta función toma como argumento una función que debe ejecutarse luego de
    un tiempo
    y opcionalmente un número que indica cúal es el argumento de la función
    decorada de la cuál se debe tomar el tiempo de demora.

    Retorna un decorador que extrae el argumento de tiempo de la lista de
    argumentos e invoca a la función decorada con el resto de los argumentos.
    Al finalizar el tiempo de demora ejecuta a la función demorada.
    """
    def _timed(wrapped_func):
        def _f(self, *args, **kwargs):
            _f.__name__ = wrapped_func.__name__ + '_wrapped'
            _f.__doc__ = wrapped_func.__doc__
            time = -1
            args = list(args)
            if len(args) == time_index:
                time = args.pop()
            elif 'time' in kwargs:
                time = kwargs.pop('time')

            wrapped_func(self, *args, **kwargs)
            if time >= 0:
                wait(time)
                delayed_func(self)

        return _f
    return _timed


def _stop_robot(s):
    s.stop()


class Robot(object):
    def __init__(self, server, robot_obj):
        self.server = server
        self.robot_model = robot_obj['robot_model']
        self.robot_id = robot_obj['robot_id']

    def send_ws_msg(self, msg, *args):
        return self.server.send_ws_msg(
            'robot',
            msg,
            {
                'robot_model': self.robot_model,
                'robot_id': self.robot_id,
            },
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
        self.send_ws_msg('stop')

    def ping(self):
        return self.send_ws_msg('ping')

    def getLine(self):
        return self.send_ws_msg('getLine')

    def getObstacle(self, *args):
        return self.send_ws_msg('getObstacle', *args)

if __name__ == '__main__':
    api_key = raw_input('api_key: ')
    server = Server('ws://xremotebot.example:8000/api', api_key)
    print(server.get_robots())
    robot = Robot(server, server.fetch_robot())
    robot.forward(100)
    wait(1)
    robot.stop()
    robot.turnRight(100, 2)
    print(robot.getObstacle())
    print(robot.getLine())
