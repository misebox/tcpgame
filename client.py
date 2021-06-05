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
    msg = AppMessage.create_register(my_addr, user_name)
    common.send_message(soc, msg)

    # expect ok
    msg = common.recv_message(soc)

    soc.close()

if __name__ == '__main__':
    main()
