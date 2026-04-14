import socket 

port = 12399

addr = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((addr,port))
s.listen(5)

while True:
    client, addr = s.accept()
    msg = ("Thank you for connecting").encode()
    client.send(msg)
    if str(client.recv(1024).decode()) == "USER":
        print("User Command Was Selected")
        status_code =("200").encode()
        client.send(status_code)
