import json
import requests
import time

wait = time.sleep



if str is not bytes:
    unicode = str

class Server(object):
    def __init__(self, host, port, protocol = 'http'):
        self.session = requests.Session()
        self.url= ''.join((protocol, '://', host, ':', str(port)))

    def send(self, methods):
        methods = json.dumps(methods)
        response = self.session.post(self.url, data={u'commands': methods})
        response = response.json()
        if response['type'] != 'returnvalues':
            raise Exception

        return response['values']


    def boards(self):
        response = self.send([{
            u'target': u'module',
            u'command': u'boards'
         }])
        return response[0]



class Board(object):
    def __init__(self, server, device='/dev/ttyUSB0'):
        self.server = server
        self.device = unicode(device)
        self.server.send([{
            u'target': u'board',
            u'command': u'__init__',
            u'board': {u'device': self.device}
        }])

    def command(self, robot, command, *args):
        response = self.server.send([{
            u'target': u'robot',
            u'command': command,
            u'id': robot.robot_id,
            u'board': {u'device': self.device},
            u'args': args
        }])
        return response[0]

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
    def __init__(self, board, robot_id):
        self.board = board
        self.robot_id = robot_id
        self.board.command(self, u'__init__')

    @timed(_stop_robot)
    def forward(self, speed=50, time=-1):
        self.board.command(self, u'forward', speed)

    @timed(_stop_robot)
    def backward(self, speed=50, time=-1):
        self.board.command(self, u'backward', speed)

    @timed(_stop_robot)
    def turnLeft(self, speed=50, time=-1):
        self.board.command(self, u'turnLeft', speed)

    @timed(_stop_robot)
    def turnRight(self, speed=50, time=-1):
        self.board.command(self, u'turnLeft', speed)

    def stop(self):
        self.board.command(self, u'stop')

    def ping(self):
        return self.board.command(self, u'ping')

if __name__ == '__main__':
    server = Server('192.168.0.13', 8000)
    print(server.boards())
    board = Board(server, server.boards()[0])
    robot = Robot(board, 0)
    robot.forward(100)
    wait(1)
    robot.stop()
    robot.turnRight(100, 2)
