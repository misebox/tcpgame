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

    clients = {}
    while True:
        client_socket, address_port = server_soc.accept()
        print(f"Connection from {address_port} has been established!")

        # Welcome
        body = "Welcome to the server!"
        msg = AppMessage.create_welcome(sender, body, address_port)
        common.send_message(client_socket, msg)

        # recv REGISTER
        msg = common.recv_message(client_socket)
        assert msg.kind == MessageKind.REGISTER
        user_name = msg.params['name']
        address, port = address_port
        clients[address] = clients.get(address) or {}
        client = clients[address]
        client['name'] = user_name
        for addr, d in clients.items():
            print(addr, d)

        # send OK
        msg = AppMessage.create_ok(sender)
        common.send_message(client_socket, msg)

        client_socket.close()

finally:
    server_soc.close()