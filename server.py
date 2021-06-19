import socket
import yaml
import common
import asyncio

from message import AppMessageFactory, MessageKind
import conversation


import socketserver
import threading



class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        # , sender, client_socket, address_port
        # self.sender = sender
        # self.server_address, self.server_port = sender
        # self.client_socket = client_socket
        # self.client_address, self.client_port = address_port
        self.user = None
        # def handle_socket(sender, client_socket, address_port):

    def handle(self):

        print(dir(self.request))
        print(self.client_address)
        self.user = None
        cur_thread = threading.current_thread()
        print(f"thread name: {cur_thread}, request {self.request} ")

        # Welcome
        body = "Welcome to the server!"
        msg = AppMessageFactory.welcome(body, self.client_address)
        self.send_message(msg)

        while True:
            # recv FIRST MESSAGE
            msg = self.recv_message()
            if msg.kind == MessageKind.REGISTER:
                conversation.process_register(self, msg)
            elif msg.kind == MessageKind.CREATE_GAME:
                conversation.process_create_game(self, msg)
            elif msg.kind == MessageKind.GET_GAME_LIST:
                conversation.process_get_game_list(self, msg)
            elif msg.kind == MessageKind.JOIN_GAME:
                conversation.process_join_game(self, msg)
            elif msg.kind == MessageKind.CLOSE:
                conversation.process_close(self, msg)
                break
            else:
                break

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def send_message(self, msg):
        common.send_message(self.request, msg)

    def recv_message(self):
        return common.recv_message(self.request)


def main():
    with open('config.yml') as f:
        config = yaml.safe_load(f)

    server = socketserver.ThreadingTCPServer((config['server_name'], int(config['server_port'])), ThreadedTCPRequestHandler)
    try:
        with server:
            server.allow_reuse_address = True
            ip, port = server.server_address
            server.serve_forever()

        # server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sender = (config['server_name'], int(config['server_port']))
        # server_soc.bind(sender)
        # # TIME_WAIT状態にあるローカルソケットをタイムアウトを待たずに再利用する

        # server_soc.listen(5)
        # while True:
        #     # TODO: 複数の接続を処理する
        #     client_socket, address_port = server_soc.accept()

        #     handle_socket(sender, client_socket, address_port)


    finally:
        server.shutdown()

main()
