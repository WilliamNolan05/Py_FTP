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

class Client_Session():
    def __init__(self, client):
        self.client = client
        self.data_socket = None
        #Defines the List of commands that methods can use 
        self.Commands = {
            'TEST':self.TEST,
            'PWD':self.PWD,
            'QUIT':self.QUIT,
            'CWD':self.CWD,
            'LIST':self.LIST,
            'PASV':self.PASV
        }
    #Function to send status codes
    def Status_Code(self,status_code):
        self.client.send((status_code).encode())

    #Gets user to input Username
    def USER(self):
        print("USER Command: ")
        username = str("")
        while username != auth_user:
            username = self.client.recv(1024).decode()
            if username == auth_user:
                self.Status_Code("331")
            else:
                self.Status_Code("530")
                print('retry')
        return username
        
    #Gets user to input password
    def PASS(self):
        print("PASS Command: ")
        password = str("")
        while password != auth_password:
            password = self.client.recv(1024).decode()
            if password == auth_password:
                self.Status_Code("230")
                print("correct!")
            else:
                self.Status_Code("530")
                print('retry')
        return password 

    #Reads inputs and runs commands accordingly
    def Input_Loop(self):
        try:
            while True:
                (command, args) = self.Command_Parser()
                print(command)
                if command in self.Commands:
                    self.Commands[command](args)
        except:
            self.client.close()
    
    #Welcomes client in and runs the authentication functions
    def Client_Handler(self):
        msg = ("Thank you for connecting!").encode()
        self.client.send(msg)
        username = self.USER()
        password = self.PASS()
        if username == auth_user and password == auth_password:
            self.Input_Loop()


    #Parses Commands in               
    def Command_Parser(self):
        S_input = ((self.client.recv(1024).decode()).split(" "))
        command = S_input[0]
        args = ""
        if len(S_input) > 1:
            args = S_input[1]
        return (command, args)
    #Will Remove at end, just used to test sending/recieving commands from client
    def TEST(self, args):
        self.client.send(('TEST').encode())
    #PWD (Print Working Directory)
    def PWD(self, args):
        cwd = os.getcwd()
        self.client.send((cwd).encode())

    def CWD(self, path):
        os.chdir(path)

    def QUIT(self, args):
        print("closing connection with client")
        self.Status_Code("600")
        self.client.close()
    
    def LIST(self, args):
        contents = str(os.listdir())
        self.client.send((contents).encode())

    def PASV(self, args):
        data_ip = '127.0.0.1'
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket = d
        self.data_socket.bind((data_ip,0))
        (ip, port) = d.getsockname()
        d.listen(5) 
        print(ip, port)
        tup = (ip, port)
        d_info = ' '.join(str(item) for item in tup)
        self.client.send((d_info).encode())
        
        
#Main loop that accepts clients, creates a new session object for them and runs it on a seperate thread. 
while True:
    client, addr = s.accept()
    new_session = Client_Session(client)
    thread = threading.Thread(target=new_session.Client_Handler)
    thread.start()