import socket

addr = '0.0.0.0'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((addr,0))
s.listen(5)

ip, port = s.getsockname()
print(port)