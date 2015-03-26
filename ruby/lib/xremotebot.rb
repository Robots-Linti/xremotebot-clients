require 'xremotebot/version'
require 'xremotebot/web_socket'
require 'json'

module XRemoteBot
  alias :wait :sleep
  class Server
    attr_reader :ws
    def initialize(url, api_key)
      @ws = WebSocket.new(url)
      ws.handshake
    end

    def send_ws_msg(entity, method, *args)
      msg = JSON.dump({
        entity: entity,
        method: method,
        args: args,
      })
      ws.send(msg)
      response = JSON.load ws.receive
      raise Exception, response['error'] if response['response'] == 'error'
      response['value']
    end

    def authentication_required
      send_ws_msg 'global', 'authentication_required'
    end

    def authenticate
      send_ws_msg 'global', 'authenticate'
    end

    def get_robots
      send_ws_msg 'global', 'get_robots'
    end

    def fetch_robot
      send_ws_msg 'global', 'fetch_robot'
    end
  end

  class Robot
    def initialize(server, robot_model, robot_id)
      @server = server
      @robot_model = robot_model
      @robot_id = robot_id
    end

    def send_ws_msg(msg, *args)
      @server.send_ws_msg('robot',
                          msg,
                          @robot_model,
                          @robot_id,
                          *args)
    end

    def forward(speed=50, time=-1)
      move('forward', speed, time)
    end

    def backward(speed=50, time=-1)
      move('backward', speed, time)
    end
    
    def turnLeft(speed=50, time=-1)
      move('turnLeft', speed, time)
    end
    
    def turnRight(speed=50, time=-1)
      move('turnRight', speed, time)
    end

    def stop
      send_ws_msg 'stop'
    end

    def ping
      send_ws_msg 'ping'
    end

    def getObstacle(distance=10)
      send_ws_msg('getObstacle', distance)
    end

    private
    def move(direction, speed=50, time=-1)
      timed(time, self, :stop) do
        send_ws_msg(direction, 100)
      end
    end

    def timed(time, instance, method)
      yield
      if time >= 0
        sleep time
        instance.send method
      end
    end
  end
end


if __FILE__ == $0
  server = XRemoteBot::Server.new('ws://xremotebot.example:8000',
                                  'api_key')
  print server.get_robots
  robot = server.fetch_robot
  robot.forward 100, 1
  robot.turnRight 100, 1
end
