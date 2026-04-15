import socket 
from prompt_toolkit import prompt
import threading 

s = socket.socket()

port = 12399

s.connect(('127.0.0.1', port))
print(str(s.recv(1024).decode()))


class Auth: 
    def PASS():
        if str(s.recv(1024).decode()) == "200":
            password = (prompt("Password: ")).encode()
            s.send(password)
            if str(s.recv(1024).decode()) == "230":
                print("Password Was Correct")
            else:
                print(("Password Incorrect"))

    def USER():
            s.send("USER".encode())
            if str(s.recv(1024).decode()) == "200":
                  username = (prompt("Username: ")).encode()
                  s.send(username)
                  if str(s.recv(1024).decode()) == "331":  
                    print("Username was correct")
                    Auth.PASS()
                  else:
                       print("Username was incorrect")
                       Auth.USER()

Auth.USER()