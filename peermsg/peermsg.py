import getpass
import hashlib
import secrets
import socket
import struct
import threading
import time
import keyring

from pyserpent import Serpent, serpent_cbc_decrypt, serpent_cbc_encrypt

peerip: str | None = None
permakey: str | None = None
port: int | None = None
newmessage = False
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
messages = []

def sender():
    global conn
    global peerip
    peerIpIn = input("Peer IP: ")
    if peerIpIn == "":
        peerIpIn = "0.0.0.0"
    if peerip is None:
        peerip = peerIpIn
    connect()
    while True:
        message = input(">>")
        send(message)


def connect():
    global conn
    global peerip
    conn.connect((peerip, port))
    print(f"Connected to: {peerip}")


def pack(salt, iv, encmessage):
    parts = [
        struct.pack(">I", len(salt)),
        salt,
        struct.pack(">I", len(iv)),
        iv,
        struct.pack(">I", len(encmessage)),
        encmessage,
    ]
    return b"".join(parts)


def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError
        data += chunk
    return data


def encrypt(data):
    global permakey
    salt = secrets.token_bytes(128)
    tempkey_input = permakey.encode() + salt
    tempkey = hashlib.sha256(tempkey_input).digest()
    iv = Serpent.generateIV()
    encdata = serpent_cbc_encrypt(tempkey, data, iv)
    return salt, iv, encdata


def decrypt(salt, iv, encdata):
    tempkey_input = permakey.encode() + salt
    tempkey = hashlib.sha256(tempkey_input).digest()
    data = serpent_cbc_decrypt(tempkey, encdata, iv)
    return data


def send(unencmessage):
    global conn
    unencmessage = unencmessage.encode()
    (salt, iv, encmessage) = encrypt(unencmessage)
    blob = pack(salt, iv, encmessage)
    conn.sendall(blob)


def recievercli():
    global peerip
    global permakey
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen()
    peersocket, peeraddr = s.accept()
    with peersocket:
        print(f"\n Connected from {peeraddr}")
        peerip = peeraddr[0]
        while True:
            salt_len = struct.unpack(">I", recv_exact(peersocket, 4))[0]
            salt = recv_exact(peersocket, salt_len)
            iv_len = struct.unpack(">I", recv_exact(peersocket, 4))[0]
            iv = recv_exact(peersocket, iv_len)
            encmessage_len = struct.unpack(">I", recv_exact(peersocket, 4))[0]
            encmessage = recv_exact(peersocket, encmessage_len)
            unencmessage = decrypt(salt, iv, encmessage).decode()
            print(f"\n{peerip}~> {unencmessage}")

def recievergui():
    global peerip
    global permakey
    global port
    global newmessage
    while True:
        time.sleep(5)
        if port is not None and peerip is not None and permakey is not None:
            print("starting reciever")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", port))
            s.listen()
            peersocket, peeraddr = s.accept()
            with peersocket:
                peerip = peeraddr[0]
                while True:
                    salt_len = struct.unpack(">I", recv_exact(peersocket, 4))[0]
                    salt = recv_exact(peersocket, salt_len)
                    iv_len = struct.unpack(">I", recv_exact(peersocket, 4))[0]
                    iv = recv_exact(peersocket, iv_len)
                    encmessage_len = struct.unpack(">I", recv_exact(peersocket, 4))[0]
                    encmessage = recv_exact(peersocket, encmessage_len)
                    unencmessage = decrypt(salt, iv, encmessage).decode()
                    messages.append(unencmessage)
                    newmessage = True
                    print(messages)

def main():
    global permakey
    global port
    global conn
    global peerip
    service = "peermsg"
    username = getpass.getuser()
    if input("Input Random Key y/n:") == "y":
        permakey = input("Input Key:")
        keyring.set_password(service, username, permakey)
        print("Stored encryption key in keyring.")
    else:
        print("Attempting to retrieve key from keyring...")
        permakey = keyring.get_password(service, username)
        if permakey is not None:
            print("Successfully retrieved key.")
        else:
            raise Exception("Failed to retrieve key.")
    port = int(input("Select communication port:"))
    if port == "":
        port = 7080
    else:
        port = port

    sendT = threading.Thread(target=sender)
    recieveT = threading.Thread(target=recievercli)

    recieveT.start()
    sendT.start()


if __name__ == "__main__":
    main()
