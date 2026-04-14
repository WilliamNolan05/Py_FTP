import socket 

s = socket.socket()

port = 12399

s.connect(('127.0.0.1', port))
print(str(s.recv(1024).decode()))


class Auth: 
    def login():
            s.send("USER".encode())

Auth.login()