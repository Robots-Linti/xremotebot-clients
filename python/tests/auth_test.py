import unittest
from test_helper import WSMockBase
from remotebot_client import Remotebot, ApiKeyRequired, ApiKeyInvalid

def auth(msg):
    msg = json.loads(msg)
    if msg['method'] == 'hello':
        return '{"response": "authentication_required"}'
    elif msg['method'] == 'authenticate':
        valid = msg['values'][0] == 'asd'
        return '{"response": "values", "values": [' + valid + ']}'

class AuthTest(unittest.TestCase):
    def setUp(self):
        server = Remotebot('localhost', api_key='asd', WSMockBase)

    def test_api_key_required_by_server(self):
        WSMockBase.action = lambda x: '{"response": "authentication_required"}'
        with self.assertRaises(ApiKeyRequired):
            server = Remotebot('localhost', wsbase=WSMockBase)

    def test_api_key_not_required_by_server(self):
        WSMockBase.action = lambda x: '{"response": "authentication_not_required"}'
        server = Remotebot('localhost', wsbase=WSMockBase)
        self.assertIsInstance(server, Remotebot)

    def test_api_key_correct(self):
        WSMockBase.action = auth
        server = Remotebot('localhost', 'asd', wsbase=WSMockBase)
        self.assertIsInstance(server, Remotebot)

    def test_api_key_incorrect(self):
        WSMockBase.action = auth
        with self.assertRaises(ApiKeyIncorrect):
            server = Remotebot('localhost', 'zxc', wsbase=WSMockBase)





