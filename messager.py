import socket
reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
reciever.bind((socket.gethostname(), 7443))
reciever.listen()
while True:
    (peersocket, address) = reciever.accept()
