import socket 

s = socket.socket()

port = 12399


s.connect(('127.0.0.1', port))
print(str(s.recv(1024).decode()))

def menu():
    choice = int(input("Please Choose FTP Command"))
    if choice == 1: 
        s.send()