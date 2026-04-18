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


class Actions:
    def TEST():
        s.send('TEST').encode()

class Auth:
    def USER():
        print("USER Command: ")
        username = str("")
        while username != auth_user:
            username = client.recv(1024).decode()
            if username == auth_user:
                Status_Code("331")
            else:
                Status_Code("530")
                print('retry')
        return username
        
    
    def PASS():
        print("PASS Command: ")
        password = str("")
        while password != auth_password:
            password = client.recv(1024).decode()
            if password == auth_password:
                Status_Code("230")
                print("correct!")
            else:
                Status_Code("530")
                print('retry')
        return password 
    

def Menu():
    while True:
        if client.recv(1024).decode() == "TEST":
            print("TEST was selected")
            client.send(("TEST").encode())
            print("Jobs Done!")
    



while True:
    client, addr = s.accept()
    msg = ("Thank you for connecting!").encode()
    client.send(msg)
    username = Auth.USER()
    password = Auth.PASS()
    if username == auth_user and password == auth_password:
        thread = threading.Thread(target=Menu)
        thread.start()