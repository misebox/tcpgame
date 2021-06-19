
# user
# [
#     {
#         'uuid': '',
#         'name': '',
#         'address': '',
#     },...
# ]

# games
# [
#     {
#         'uuid': '',
#         'name': '',
#         'players' = [uuid, uuid]
#     },...
# ]

from typing import List


class DB:
    def __init__(self):
        self.users = []
        self.games = []



class Game:
    name: str
    players: List[str]

    def __init__(self):
        self.name = ''
        self.players = []

    def to_dict(self):
        return dict(
            klass='Game',
            name=self.name,
            players=self.players,
        )

    @classmethod
    def from_dict(cls, _dict):
        assert _dict.get('klass') == 'Game'
        game = Game()
        game.name = _dict['name']
        game.players = _dict['players']
        return game

    def __str__(self):
        return f'Game({self.name} {self.players})'


db = DB()
