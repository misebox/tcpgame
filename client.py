import socket
import yaml

import common
from message import AppMessageFactory


def main():
    with open('config.yml') as f:
        config = yaml.safe_load(f)
    remote_name = config['remote_name']
    server_port = config['server_port']
    user_name = config['user_name']

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender = (remote_name, server_port)
    soc.connect(sender)

    msg = common.recv_message(soc)

    my_addr = msg.params['client_address']
    print(my_addr)

    # register
    msg = AppMessageFactory.register(user_name)
    common.send_message(soc, msg)
    msg = common.recv_message(soc)

    while True:
        cmd = input('input command:').strip().split(' ')
        if cmd[0] == 'game':
            if cmd[1] == 'create':
                gamename = cmd[2]
                msg = AppMessageFactory.create_game(gamename)
                common.send_message(soc, msg)
                msg = common.recv_message(soc)
            elif cmd[1] == 'list':
                msg = AppMessageFactory.get_game_list()
                common.send_message(soc, msg)
                msg = common.recv_message(soc)                
                for g in msg.params['games']:
                    print(g)
            elif cmd[1] == 'join':
                game_name = cmd[2]
                msg = AppMessageFactory.join_game(game_name)
                common.send_message(soc, msg)
                msg = common.recv_message(soc)
                print(msg)

        elif cmd[0] == 'close':
            msg = AppMessageFactory.close()
            common.send_message(soc, msg)
            msg = common.recv_message(soc)
            break

    soc.close()

if __name__ == '__main__':
    main()
