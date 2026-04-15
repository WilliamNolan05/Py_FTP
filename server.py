import socket 
import threading
import logging

port = 12399

addr = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((addr,port))
s.listen(5)

auth_user = 'tony'
auth_password = 'gabagool'


def Status_Code(status_code):
    client.send((status_code).encode())

class Auth:
    def USER():
        print("USER Command: ")
        Status_Code("200")
        username = client.recv(1024).decode()
        if username == auth_user:
            Status_Code("331")
            Auth.PASS()
        else:
            client.send(("Incorrect Username").encode())
            Auth.USER()
    
    
    def PASS():
        print("PASS Command: ")
        Status_Code("200")
        password = client.recv(1024).decode()
        if password == auth_password:
            Status_Code("230")
        else:
            client.send(("Incorrect Password").encode())
            Auth.PASS()
        

while True:
    client, addr = s.accept()
    msg = ("Thank you for connecting! ").encode()
    client.send(msg)
    if str(client.recv(1024).decode()) == "USER":
        Auth.USER()
