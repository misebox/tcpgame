
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

class DB:
    def __init__(self):
        self.users= []
        self.games = []


db = DB()
