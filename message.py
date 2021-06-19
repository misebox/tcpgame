from db import Game
import enum
import json
import time
import uuid
from datetime import datetime, timedelta, timezone

class MessageKind(enum.Enum):
    OK            = enum.auto()
    ERROR         = enum.auto()
    WELCOME       = enum.auto()
    REGISTER      = enum.auto()
    CREATE_GAME   = enum.auto()
    GET_GAME_LIST = enum.auto()
    GAME_LIST     = enum.auto()
    JOIN_GAME     = enum.auto()
    START_GAME    = enum.auto()
    ACTION        = enum.auto()
    RESULT        = enum.auto()
    SCORE         = enum.auto()
    CLOSE         = enum.auto()

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')


class AppMessage:
    def __init__(self):
        self.sender = None
        self.kind = None
        self.params = {}
        self.timestamp = None

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


class AppMessageFactory:
    @classmethod
    def create_message(cls, kind, params=None, sender=None):
        msg = AppMessage()
        msg.sender = sender
        msg.kind = kind
        msg.params = params or {}
        msg.timestamp = datetime.now(JST)
        return msg

    @classmethod
    def ok(cls):
        return cls.create_message(MessageKind.OK)

    @classmethod
    def welcome(cls, body, client_address):
        params = dict(
            body=body,
            client_address=client_address
        )
        return cls.create_message(MessageKind.WELCOME, params)

    @classmethod
    def register(cls, name):
        params = dict(
            name=name,
        )
        return cls.create_message(MessageKind.REGISTER, params)

    @classmethod
    def create_game(cls, name):
        params = dict(
            name=name,
        )
        return cls.create_message(MessageKind.CREATE_GAME, params)

    @classmethod
    def get_game_list(cls):
        return cls.create_message(MessageKind.GET_GAME_LIST)

    @classmethod
    def send_game_list(cls, games):
        params = dict(
            games=games,
        )
        return cls.create_message(MessageKind.GAME_LIST, params)

    @classmethod
    def join_game(cls, name):
        params = dict(
            name=name,
        )
        return cls.create_message(MessageKind.JOIN_GAME, params)

    @classmethod
    def start_game(cls, game):
        params = dict(
            game=game,
        )
        return cls.create_message(MessageKind.START_GAME, params)

    @classmethod
    def close(cls):
        return cls.create_message(MessageKind.CLOSE)


class AppJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AppMessage):
            return o.to_dict()
        elif isinstance(o, MessageKind):
            return o.name
        elif isinstance(o, Game):
            return o.to_dict()
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, uuid.UUID):
            return {'klass': 'UUID', 'uuid': str(o)}
        else:
            return super(AppJSONEncoder, self).default(o)

def decodeAppMessage(obj):
    if obj.get('klass') == 'Message':
        return AppMessage.from_dict(obj)
    if obj.get('klass') == 'Game':
        return Game.from_dict(obj)
    if obj.get('klass') == 'UUID':
        return uuid.UUID(obj['uuid'])
    else:
        return obj

