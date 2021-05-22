import socket
import yaml

s = open('config.yml').read()
config = yaml.load(s)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config['server_name'], config['server_port']))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

msg = s.recv(1024)
print(msg.decode("utf-8"))