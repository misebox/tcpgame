import unittest

from message import AppMessage, MessageKind
from message import AppJSONEncoder



class TestAppMessage(unittest.TestCase):

    def test_greeting_to_json(self):
        greet = AppMessage(sender=None, kind=MessageKind.GREETING, params={})
        expected = '{"klass": "Message", "sender": null, "kind": "GREETING", "params": {}}'
        self.assertEqual(greet.to_json(), expected, "シリアライズ結果がおかしい")

    def test_welcome_to_json(self):
        welcome = AppMessage(sender=("127.0.0.1", 40000), kind=MessageKind.WELCOME, params=dict(body="HELLO"))
        expected = '{"klass": "Message", "sender": ["127.0.0.1", 40000], "kind": "WELCOME", "params": {"body": "HELLO"}}'
        self.assertEqual(welcome.to_json(), expected, "シリアライズ結果がおかしい")




if __name__ == "__main__":
    unittest.main()