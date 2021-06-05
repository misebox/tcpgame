import enum
import json
import time
from datetime import datetime, timedelta, timezone

class MessageKind(enum.Enum):
    GREETING    = enum.auto()
    WELCOME     = enum.auto()
    REGISTER    = enum.auto()
    CREATE_GAME = enum.auto()
    LIST_GAME   = enum.auto()
    JOIN_GAME   = enum.auto()
    START_GAME  = enum.auto()
    ACTION      = enum.auto()
    RESULT      = enum.auto()
    SCORE       = enum.auto()

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')


class AppMessage:
    def __init__(self):
        self.sender = None
        self.kind = None
        self.params = {}
        self.timestamp = None

    @classmethod
    def create_welcome(cls, sender, body, client_address):
        params = dict(
            body=body,
            client_address=client_address
        )
        return cls.create_message(sender, MessageKind.WELCOME, params)

    @classmethod
    def create_message(cls, sender, kind, params):
        msg = AppMessage()
        msg.sender = sender
        msg.kind = kind
        msg.params = params
        msg.timestamp = datetime.now(JST)
        return msg

    @classmethod
    def from_dict(cls, _dict):
        assert _dict.get('klass') == 'Message'
        kind = MessageKind[_dict['kind']]
        sender = tuple(_dict['sender'])
        params = _dict['params']
        timestamp = datetime.fromisoformat(_dict['timestamp'])
        msg = cls()
        msg.kind = kind
        msg.sender = sender
        msg.params = params
        msg.timestamp = timestamp
        return msg

    def to_json(self):
        # TODO: validation
        json_str = json.dumps(self, cls=AppJSONEncoder)
        return json_str

    def to_bytes(self):
        return bytes(self.to_json(), encoding='ascii')

    def to_dict(self):
        return dict(
            klass='Message',
            sender=self.sender,
            kind=self.kind,
            params=self.params,
            timestamp=self.timestamp,
        )

    @staticmethod
    def restore_message(message_bytes):
        msg = json.loads(message_bytes, object_hook=decodeAppMessage)
        return msg
    

class AppJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AppMessage):
            return o.to_dict()
        elif isinstance(o, MessageKind):
            return o.name
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return super(AppJSONEncoder, self).default(o)

def decodeAppMessage(obj):
    if obj.get('klass') == 'Message':
        return AppMessage.from_dict(obj)
    else:
        return obj

