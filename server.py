import socket
import yaml
import common
import time

with open('config.yml') as f:
    config = yaml.safe_load(f)

try:
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_soc.bind((config['server_name'], int(config['server_port'])))
    # TIME_WAIT状態にあるローカルソケットをタイムアウトを待たずに再利用する

    server_soc.listen(5)

    while True:
        client_socket, address = server_soc.accept()
        print(f"Connection from {address} has been established!")
        body = bytes("Welcome to the server!", 'utf-8')
        common.send_message(client_socket, body)

        client_socket.close()

finally:
    server_soc.close()