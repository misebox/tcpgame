import socket
import yaml

import common


def main():
    with open('config.yml') as f:
        config = yaml.safe_load(f)

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender = (config['remote_name'], config['server_port'])
    soc.connect(sender)

    msg = common.recv_message(soc)
    soc.close()

if __name__ == '__main__':
    main()
