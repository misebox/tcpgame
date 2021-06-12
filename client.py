import socket
import yaml

import common
from message import AppMessage


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
    msg = AppMessage.create_register(user_name)
    common.send_message(soc, msg)
    msg = common.recv_message(soc)

    while True:
        cmd = input('input command:').strip().split(' ')
        if cmd[0] == 'game':
            if cmd[1] == 'create':
                gamename = cmd[2]
                msg = AppMessage.create_create_game(gamename)
                common.send_message(soc, msg)
            elif cmd[1] == 'list':
                print('game list')
        elif cmd[0] == 'close':
            msg = AppMessage.create_close()
            common.send_message(soc, msg)
            msg = common.recv_message(soc)
            break

    soc.close()

if __name__ == '__main__':
    main()
