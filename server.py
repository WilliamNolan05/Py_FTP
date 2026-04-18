import socket 
import threading
import logging
import os 

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
        client.send(('TEST').encode())
        
    def PWD():
        cwd = os.getcwd()
        client.send((cwd).encode())

Commands = {
            'TEST':Actions.TEST,
            'PWD':Actions.PWD
            }

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
    

class Menu:
    def Input_Loop():
         while True:
             command = Menu.Command_Parser()
             print(command)
             if command in Commands:
                  Commands[command]()
                  
    def Command_Parser():
        S_input = ((client.recv(1024).decode()).split(" "))
        command = S_input[0]
        return command


while True:
    client, addr = s.accept()
    msg = ("Thank you for connecting!").encode()
    client.send(msg)
    username = Auth.USER()
    password = Auth.PASS()
    if username == auth_user and password == auth_password:
        thread = threading.Thread(target=Menu.Input_Loop)
        thread.start()