import socket 
from prompt_toolkit import prompt
import os

s = socket.socket()
data_stream = None

port = 12399

addr = prompt("FTP Server IP: ")

s.connect((addr, port))
print(str(s.recv(1024).decode()))

class Actions:
    def QUIT(args):
        s.send(("QUIT").encode())
        if (s.recv(1024).decode()) == "221":
            quit()

    def HELP(args):
        f = open('help.txt', 'r', encoding='utf-8')
        file_contents = f.read()
        return file_contents

    def PWD(args):
        s.send(("PWD").encode())
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
    
    def DELE(filename):
        tup = (("DELE", filename))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())
        return(f'{filename} deleted ')
    
    def CDUP(args):
        s.send(("CDUP").encode())
        return("moved up a directory")
    
    def MKD(dirname):
        tup = (("MKD", dirname))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())
        return(f'directory {dirname} created ')
    
    def RMD(dirname):
        tup = (("RMD", dirname))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())
        return(f'directory {dirname} removed')   
    
    def PASV(args):
        s.send(("PASV").encode())
        d_info = (s.recv(1024).decode())
        ip, port = d_info.split(" ")
        port = int(port)

        data_socket = socket.socket()
         
        data_socket.connect((ip, port))
        data_socket.send(('Connected').encode())

        global data_stream
        data_stream = Data_Stream(data_socket)
        return('Data Connection Established')
    

class Data_Stream:

    def __init__(self, data_socket):
         self.data_socket = data_socket
        
    def RETR(self, filename):

        tup = (("RETR", filename))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())
        if (s.recv(1024).decode()) == "150":
            with open (filename, "wb") as file:
                while True:
                    chunk = self.data_socket.recv(8192)

                    if not chunk:
                        break 
                    file.write(chunk)
        if (s.recv(1024).decode()) == "226":
            return(f"{filename} has been copied from ftp server")
        
    def STOR(self, filename):
        tup = (("STOR", filename))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())

        if (s.recv(1024).decode()) == "150":
            with open(filename, "rb") as file:
                while True: 
                    chunk = file.read(8192)
                    if not chunk:
                        break   
                    self.data_socket.sendall(chunk)
                self.data_socket.close()
                self.data_socket = None
        else: 
            return("something went wrong in file transfer")
        if (s.recv(1024).decode()) == "226":
            return(f"{filename} has been copied to the server")
        else: return("something went wrong in file transfer")
    
    def CWD(path):
        tup = (("CWD", path))
        msg = ' '.join(str(val) for val in tup)
        s.send((msg).encode())
        return(f'Path changed to {path}')   
    
    
Commands = {'QUIT':Actions.QUIT,
            'HELP':Actions.HELP,
            'PWD':Actions.PWD,
            'LPWD':Actions.LPWD,
            'CWD':Actions.CWD,
            'LCD':Actions.LCD,
            'LLIST':Actions.LLIST,
            'LIST':Actions.LIST,
            'PASV':Actions.PASV,
            'RMD':Actions.RMD,
            'MKD':Actions.MKD,
            'CDUP':Actions.CDUP,
            'DELE':Actions.DELE,
            'RETR': lambda args: data_stream.RETR(args) if data_stream is not None else print("Please run PASV first"),
            'STOR': lambda args: data_stream.STOR(args) if data_stream is not None else print("Please run PASV first")
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