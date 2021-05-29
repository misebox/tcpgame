import socket


HEADER_SIZE = 4

def recv_bytes(soc: socket.socket, req_size):
    buf = bytearray()
    cnt = 0
    while len(buf) < req_size:
        print(req_size, len(buf))
        # received = soc.recv(req_size - len(buf))
        received = soc.recv(4096)
        if len(received) == 0 and cnt >= 10:
            raise Exception('received 0 for 10 times')
        print('len received', len(received))
        buf.extend(received)
        cnt += 1
    return buf

def recv_body_size(soc: socket.socket):
    header_bytes = recv_bytes(soc, HEADER_SIZE)
    print(header_bytes)
    return bytes_to_int(header_bytes)

def bytes_to_int(_bytes):
    return int.from_bytes(_bytes, byteorder='big')

def int_to_bytes(num, byte_count):
    return num.to_bytes(byte_count, byteorder='big')

def send_message(soc, body):
    body_size = len(body)
    print(f'sent {body_size} bytes: {body}')
    header_bytes = int_to_bytes(body_size, 4)
    message = header_bytes + body
    res = soc.send(bytearray(header_bytes))
    print(res)
    soc.send(body)
