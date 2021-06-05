import unittest
import json

from message import AppMessage, MessageKind
from message import AppJSONEncoder
from message import decodeAppMessage



class TestAppMessage(unittest.TestCase):

    def test_greeting_to_json(self):
        greet = AppMessage(sender=None, kind=MessageKind.GREETING, params={})
        expected = '{"klass": "Message", "sender": null, "kind": "GREETING", "params": {}}'
        self.assertEqual(greet.to_json(), expected, "シリアライズ結果がおかしい")

    def test_welcome_to_json(self):
        welcome = AppMessage(sender=("127.0.0.1", 40000), kind=MessageKind.WELCOME, params=dict(body="HELLO"))
        expected = '{"klass": "Message", "sender": ["127.0.0.1", 40000], "kind": "WELCOME", "params": {"body": "HELLO"}}'
        self.assertEqual(welcome.to_json(), expected, "シリアライズ結果がおかしい")

    def test_decode_welcome(self):
        welcome_json = '{"klass": "Message", "sender": ["127.0.0.1", 40000], "kind": "WELCOME", "params": {"body": "HELLO"}}'
        msg = json.loads(welcome_json, object_hook=decodeAppMessage)
        expected = AppMessage(sender=("127.0.0.1", 40000), kind=MessageKind.WELCOME, params=dict(body="HELLO"))

        self.assertEqual(msg.kind, expected.kind, "デシリアライズ結果のkindがおかしい")
        self.assertEqual(msg.sender, expected.sender, "デシリアライズ結果のsenderがおかしい")
        self.assertEqual(msg.params, expected.params, "デシリアライズ結果のparamsがおかしい")



if __name__ == "__main__":
    unittest.main()