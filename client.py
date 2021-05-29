import socket
import yaml
import time

import common

def main():
    with open('config.yml') as f:
        config = yaml.safe_load(f)

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.connect((config['remote_name'], config['server_port']))

    body_size = common.recv_body_size(soc)
    print(body_size)
    body = common.recv_bytes(soc, body_size)
    print(body)
    soc.close()

if __name__ == '__main__':
    main()
