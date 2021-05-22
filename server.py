import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 11111))  # IPとポート番号を指定します
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the server!", 'utf-8'))

    full_msg = b''
    while True:
        msg = clientsocket.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg
    print(full_msg)

    clientsocket.close()