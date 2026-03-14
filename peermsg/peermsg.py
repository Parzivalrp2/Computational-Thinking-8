import hashlib
import os
import secrets
import socket
import struct
import threading

from dotenv import load_dotenv
from pyserpent import Serpent, serpent_cbc_decrypt, serpent_cbc_encrypt

load_dotenv()

permakeyenv = os.getenv("KEY")
if permakeyenv is None:
    raise Exception(
        "create a .env file in the root directory and define a 'KEY' variable to a random value (can be created using head -c 256 /dev/urandom | base64 on linux), otherwise get one from your peer"
    )
else:
    permakey = permakeyenv
port = int(input("Select communication port:"))
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerip = None


def sender():
    global conn
    global peerip
    peerIpIn = input("Peer IP: ")
    if peerIpIn == "":
        peerIpIn = "0.0.0.0"
    if peerip is None:
        peerip = peerIpIn
    connect(peerip)
    while True:
        message = input(">>")
        send(message)


def connect(peerip):
    global conn
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


def unpack(blob):
    i = 0

    def read_len():
        nonlocal i
        if i + 4 > len(blob):
            raise ValueError("truncated")
        L = struct.unpack(">I", blob[i : i + 4])[0]
        i += 4
        return L

    def read_bytes(L):
        nonlocal i
        if i + L > len(blob):
            raise ValueError("truncated")
        v = blob[i : i + L]
        i += L
        return v

    salt = read_bytes(read_len())
    iv = read_bytes(read_len())
    encmessage = read_bytes(read_len())
    return salt, iv, encmessage


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


def reciever():
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


sendT = threading.Thread(target=sender)
recieveT = threading.Thread(target=reciever)


recieveT.start()
sendT.start()
