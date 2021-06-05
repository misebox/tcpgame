import socket
import yaml
import common

from message import AppMessage, MessageKind

with open('config.yml') as f:
    config = yaml.safe_load(f)

try:
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender = (config['server_name'], int(config['server_port']))
    server_soc.bind(sender)
    # TIME_WAIT状態にあるローカルソケットをタイムアウトを待たずに再利用する

    server_soc.listen(5)

    while True:
        client_socket, address = server_soc.accept()
        print(f"Connection from {address} has been established!")
        # Welcome
        body = "Welcome to the server!"
        msg = AppMessage(kind=MessageKind.WELCOME, sender=sender, params=dict(body=body, client_address=address))
        common.send_message(client_socket, msg)

        client_socket.close()

finally:
    server_soc.close()