# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'xremotebot/version'

Gem::Specification.new do |spec|
  spec.name          = "xremotebot"
  spec.version       = XRemoteBot::VERSION
  spec.authors       = ["'Fernando López'"]
  spec.email         = ["'soportelihuen@linti.unlp.edu.ar'"]

  spec.summary       = %q{Ruby client for XRemoteBot}
  spec.description   = %q{Ruby client to control robots through the XRemoteBot server.}
  spec.homepage      = "https://github.com/fernandolopez/xremotebot-clients"

  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  spec.bindir        = "exe"
  spec.licenses      = ["MIT"]
  spec.executables   = spec.files.grep(%r{^exe/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]

  spec.add_dependency "websocket", "~> 1.2"
  spec.add_development_dependency "bundler", "~> 1.9"
  spec.add_development_dependency "rake", "~> 10.0"
  spec.add_development_dependency "pry", "~> 0.10"
  spec.add_development_dependency "rb-readline", "~> 0.5"
end
