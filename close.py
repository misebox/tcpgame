
import socket
import yaml

with open('config.yml') as f:
    config = yaml.safe_load(f)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    soc.bind((config['server_name'], int(config['server_port'])))  # IPとポート番号を指定します

finally:
    soc.close()
