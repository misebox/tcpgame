import socket
import yaml
import common

from message import AppMessage, MessageKind
import conversation

with open('config.yml') as f:
    config = yaml.safe_load(f)


class SocketWrapper:
    def __init__(self, sender, client_socket, address_port):
        self.sender = sender
        self.server_address, self.server_port = sender
        self.client_socket = client_socket
        self.client_address, self.client_port = address_port

    def send_message(self, msg):
        common.send_message(self.client_socket, msg)

    def recv_message(self):
        return common.recv_message(self.client_socket)

try:
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender = (config['server_name'], int(config['server_port']))
    server_soc.bind(sender)
    # TIME_WAIT状態にあるローカルソケットをタイムアウトを待たずに再利用する

    server_soc.listen(5)

    while True:
        client_socket, address_port = server_soc.accept()
        print(f"Connection from {address_port} has been established!")

        socw = SocketWrapper(sender, client_socket, address_port)
        # Welcome
        body = "Welcome to the server!"
        msg = AppMessage.create_welcome(sender, body, address_port)
        socw.send_message(msg)

        # recv FIRST MESSAGE
        msg = socw.recv_message()
        if msg.kind == MessageKind.REGISTER:
            conversation.process_register(socw, msg)
        elif msg.kind == MessageKind.CREATE_GAME:
            conversation.process_create_game(socw, msg)

        client_socket.close()

finally:
    server_soc.close()