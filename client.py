import socket 
from prompt_toolkit import prompt
import os

s = socket.socket()

port = 12399

addr = prompt("FTP Server IP: ")

s.connect((addr, port))
print(str(s.recv(1024).decode()))

class Actions:
    def QUIT(args):
        s.send(("QUIT").encode())
        if (s.recv(1024).decode()) == "600":
            quit()

    def HELP(args):
        f = open('help.txt', 'r', encoding='utf-8')
        file_contents = f.read()
        return file_contents

    def PWD(args):
        s.send(("PWD").encode())
        return (s.recv(1024).decode())
    
    def TEST(args):
        s.send(("TEST").encode())
        return (s.recv(1024).decode())
    
    def CWD(path):
        tup = (("CWD", path))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())
        return(f'Path changed to {path}')
    
    def LPWD(args):
        cwd = os.getcwd()
        return(cwd)
    
    def LCD(path):
        os.chdir(path)
    
    def LLIST(args):
        return os.listdir()
    
    def LIST(args):
        s.send(("LIST").encode())
        return (s.recv(1024).decode())
    
    def PASV(args):
        s.send(("PASV").encode())
        d_info = (s.recv(1024).decode())
        ip, port = d_info.split(" ")
        port = int(port)

        d = socket.socket()
         
        d.connect((ip, port))
        d.send(('Connected').encode())
        return(port)
        

    
Commands = {'QUIT':Actions.QUIT,
            'HELP':Actions.HELP,
            'PWD':Actions.PWD,
            'TEST':Actions.TEST,
            'CWD':Actions.CWD,
            'LCD':Actions.LCD,
            'LLIST':Actions.LLIST,
            'LIST':Actions.LIST,
            'PASV':Actions.PASV
            }

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
             (command, args) = Menu.Command_Parser()
             
             if command in Commands:
                  print(Commands[command](args))
    
    def Command_Parser():
            U_input = (prompt("tony> ")).split(" ")
            command = U_input[0]
            args = ""
            if len(U_input) > 1:
                args = U_input[1]
            return (command, args)


Auth.USER()