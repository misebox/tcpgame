import socket
import yaml

with open('config.yml') as f:
    config = yaml.safe_load(f)

print(config)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config['server_name'], config['server_port']))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

full_msg = b''
while True:
    msg = s.recv(2)
    if len(msg) == 0:
        break
    full_msg += msg

print(full_msg.decode("utf-8"))

s.send(bytes(f"{config['greeting']} My name is {config['user_name']}", 'utf-8'))

full_msg = b''
while True:
    msg = s.recv(2)
    if len(msg) == 0:
        break
    full_msg += msg
print(full_msg.decode("utf-8"))