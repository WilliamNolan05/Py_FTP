import socket 
from prompt_toolkit import prompt
import threading 

s = socket.socket()

port = 12399

s.connect(('127.0.0.1', port))
print(str(s.recv(1024).decode()))

class Auth: 
    def PASS():
            status_code = "1"
            while status_code != "230":
                username = (prompt("Password: ")).encode()
                s.send(username)
                if str(s.recv(1024).decode()) == "230":  
                    print("Password was Correct")
                    status_code = "230"
                    Menu.Welcome_Page()
                else:
                    print("Password was incorrect")

    def USER():
            s.send("USER".encode())
            status_code = "1"
            while status_code != "331":
                username = (prompt("Username: ")).encode()
                s.send(username)
                if str(s.recv(1024).decode()) == "331":  
                    print("Username was correct")
                    status_code = "331"
                    Auth.PASS()
                else:
                    print("Username was incorrect")

class Menu:
    def Welcome_Page():
          f = open('banner.txt', 'r', encoding='utf-8')
          file_contents = f.read()
          print(file_contents)
          Menu.Input_Loop()
        
    def Input_Loop():
         while True:
             command = (prompt("tony> ")).encode()




Auth.USER()
