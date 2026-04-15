import socket 
from prompt_toolkit import prompt
import threading 

s = socket.socket()

port = 12399

s.connect(('127.0.0.1', port))
print(str(s.recv(1024).decode()))


class Auth: 
    def PASS():
          s.send("PASS".encode())
          
          
          
    def USER():
            s.send("USER".encode())
            if str(s.recv(1024).decode()) == "331":
                  username = (prompt("Username: ")).encode()
                  s.send(username)
                  if str(s.recv(1024).decode()) == 'Username Correct':  
                    print("Username was correct")
                    Auth.PASS()
            return    

Auth.USER()