require 'xremotebot/version'
#require 'xremotebot/web_socket'
#require 'xremotebot/ws_cli'
require 'websocket'
require 'json'

module XRemoteBot
  alias :wait :sleep

  class WS
    def initialize(host, port, path)
      @sock = TCPSocket.new host, port
      url = %Q(ws://#{host}:#{port}/#{path})
      @handshake = WebSocket::Handshake::Client.new(url: url)
      @sock.puts(@handshake)

      @handshake << @sock.recv(4096)
      while !@handshake.finished?
        @handshake << @sock.recv(4096)
      end

      raise Exception unless @handshake.valid?

    end

    def send(data)
      frame = WebSocket::Frame::Outgoing::Server.new(
        version: @handshake.version,
        data: data,
        type: :text
      )
      @sock.send frame.to_s, 0
    end

    def receive()
      frame = WebSocket::Frame::Incoming::Server.new(
        version: @handshake.version
      )
      frame << @sock.recv(4096)
      data = ''
      loop do
        part = frame.next
        break if part.nil?
        data += part.to_s
      end
      return data
    end

  end
  class Server
    attr_reader :ws
    def initialize(host, port, path, api_key)
      @ws = WS.new(host, port, path)
      if send_ws_msg('global', 'authentication_required')
        send_ws_msg('global', 'authenticate', api_key)
      end
    end

    def send_ws_msg(entity, method, *args)
      msg = JSON.dump({
        entity: entity,
        method: method,
        args: args,
      })
      ws.send(msg)
      response = JSON.load ws.receive
      raise Exception, response['message'] if response['response'] == 'error'
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
    def initialize(server, robot_obj)
      @server = server
      @robot_model = robot_obj['robot_model']
      @robot_id = robot_obj['robot_id']
    end

    def send_ws_msg(msg, *args)
      @server.send_ws_msg('robot',
                          msg,
                          {
                            'robot_model': @robot_model,
                            'robot_id': @robot_id,
                          },
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

    def getObstacle()
      send_ws_msg 'getObstacle'
    end

    def getLine()
      send_ws_msg 'getLine'
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

  def self.main
    puts 'api_key:'
    server = XRemoteBot::Server.new('xremotebot.example',
                                    8000,
                                    'api',
                                    gets.strip)
    print "Robots #{server.get_robots}\n"
    robot = Robot.new server, server.fetch_robot
    robot.forward 100, 1
    robot.turnRight 100, 1
    p robot.getLine
    p robot.getObstacle
  end
end

if __FILE__ == $0
  XRemoteBot.main
end
