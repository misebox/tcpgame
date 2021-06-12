import common
from db import db
from message import AppMessage, MessageKind
import uuid




def process_register(socw, msg):
    # register user
    user_name = msg.params['name']
    user = next(filter(lambda x: x['name'] == user_name, db.users), None)
    if not user:
        user = {}
        user['uuid'] = uuid.uuid4()
        user['address'] = socw.client_address
        user['name'] = user_name
        db.users.append(user)

    user

    # send OK
    msg = AppMessage.create_ok()
    socw.send_message(msg)

    # DEBUG
    for user in db.users:
        print(user)


def process_create_game(socw, msg):
    # create game
    name = msg.params['name']
    game = db.games.get(name)
    if not game:
        game = {}
        game['uuid'] = uuid.uuid4()
        game['name'] = name

    # send OK
    msg = AppMessage.create_ok()
    socw.send_message(msg)
