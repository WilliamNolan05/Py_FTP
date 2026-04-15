import socket 
import threading

port = 12399

addr = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((addr,port))
s.listen(5)

auth_user = 'tony'
auth_password = 'gabagool'

class Auth:
    def USER():
        print("User Command Was Selected")
        status_code = ("331").encode()
        client.send(status_code)

while True:
    client, addr = s.accept()
    msg = ("Thank you for connecting! ").encode()
    client.send(msg)
    if str(client.recv(1024).decode()) == "USER":
        Auth.USER()
        print("User Command Was Selected")
        status_code = ("331").encode()
        client.send(status_code)
        username = client.recv(1024).decode()
        if username == auth_user:
            client.send(('Username Correct').encode())
        else:
            client.send(('Incorrect Username').encode())