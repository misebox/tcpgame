import common
from db import db
from db import Game
from message import AppMessageFactory, MessageKind



def find_user_by_name(name):
    return next(filter(lambda x: x['name'] == name, db.users), None)


def find_game_by_name(name):
    return next(filter(lambda x: x.name == name, db.games), None)


def process_register(socw, msg):
    # register user
    user_name = msg.params['name']
    user = next(filter(lambda x: x['name'] == user_name, db.users), None)
    if not user:
        user = {}
        user['address'] = socw.client_address[0]
        user['name'] = user_name
        db.users.append(user)
    socw.set_user(user)
    # send OK
    msg = AppMessageFactory.ok()
    socw.send_message(msg)
    # DEBUG
    for user in db.users:
        print(user)


def process_create_game(socw, msg):
    # create game
    name = msg.params['name']
    game = find_game_by_name(name)
    if not game:
        game = Game()
        game.name = name
        game.players.append(socw.get_user())
        db.games.append(game)

    # send OK
    msg = AppMessageFactory.ok()
    socw.send_message(msg)


def process_join_game(socw, msg):
    # join game
    name = msg.params['name']
    game = find_game_by_name(name)
    if not game:
        msg = AppMessageFactory.ok()
        socw.send_message(msg)
        return
    game.players.append(socw.get_user())
    # send OK
    msg = AppMessageFactory.start_game(game)
    socw.send_message(msg)


def process_get_game_list(socw, msg):
    msg = AppMessageFactory.send_game_list(db.games)
    socw.send_message(msg)


def process_close(socw, msg):
    msg = AppMessageFactory.ok()
    socw.send_message(msg)