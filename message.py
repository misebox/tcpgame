import enum
import json
import time
from datetime import datetime, timedelta, timezone

class MessageKind(enum.Enum):
    OK          = enum.auto()
    ERROR       = enum.auto()
    WELCOME     = enum.auto()
    REGISTER    = enum.auto()
    CREATE_GAME = enum.auto()
    LIST_GAME   = enum.auto()
    JOIN_GAME   = enum.auto()
    START_GAME  = enum.auto()
    ACTION      = enum.auto()
    RESULT      = enum.auto()
    SCORE       = enum.auto()
    CLOSE       = enum.auto()

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')


class AppMessage:
    def __init__(self):
        self.sender = None
        self.kind = None
        self.params = {}
        self.timestamp = None

    @classmethod
    def create_message(cls, kind, params=None, sender=None):
        msg = AppMessage()
        msg.sender = sender
        msg.kind = kind
        msg.params = params or {}
        msg.timestamp = datetime.now(JST)
        return msg

    @classmethod
    def create_ok(cls):
        return cls.create_message(MessageKind.OK)

    @classmethod
    def create_welcome(cls, body, client_address):
        params = dict(
            body=body,
            client_address=client_address
        )
        return cls.create_message(MessageKind.WELCOME, params)

    @classmethod
    def create_register(cls, name):
        params = dict(
            name=name,
        )
        return cls.create_message(MessageKind.REGISTER, params)

    @classmethod
    def create_create_game(cls, name):
        params = dict(
            name=name,
        )
        return cls.create_message(MessageKind.CREATE_GAME, params)

    @classmethod
    def create_close(cls):
        return cls.create_message(MessageKind.CLOSE)

    @classmethod
    def from_dict(cls, _dict):
        assert _dict.get('klass') == 'Message'
        kind = MessageKind[_dict['kind']]
        sender = tuple(_dict['sender']) if _dict['sender'] else None
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
    
    def __str__(self):
        timestamp = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else self.timestamp
        return f'MSG({timestamp} {self.sender} {self.kind} {self.params})'

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

