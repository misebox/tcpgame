import enum
import json


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


class AppMessage:

    def __init__(self, sender, kind, params):
        self.sender = sender
        self.kind = kind
        self.params = params

    def to_json(self):
        # TODO: validation
        json_str = json.dumps(self, cls=AppJSONEncoder)
        return json_str


class AppJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AppMessage):
            return dict(
                klass='Message',
                sender=o.sender,
                kind=o.kind,
                params=o.params,
            )
        elif isinstance(o, MessageKind):
            return o.name
        else:
            return super(AppJSONEncoder, self).default(o)
