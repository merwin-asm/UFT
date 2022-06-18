"""
pyE2EE 1.0.2
A module for end-2-end-encryption.
Author : Merwin Mathews
"""


import rsa
import base64
import string
import socket
import random
import threading
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



class Server:
    def __init__(self,port=5432,client_loop=None):
        try:
            self.PublicKey , self.PrivateKey = Utils().load_keys()
        except:
            Utils().generate_keys_save()
            self.PublicKey , self.PrivateKey = Utils().load_keys()

        # if client_loop != None:
        self.client_loop = client_loop

        # VARS
        self.TotalCons = 0
        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', port))
        self.server.listen()
        self.connection_loop()


    def connection_loop(self):
        while True:
            c, addr = self.server.accept()
            c.send(self.PublicKey.save_pkcs1("PEM"))
            key = self.recv_rsa(c)
            f = Fernet(Utils().password_to_key(key))
            self.clients.append([c,f])
            t = threading.Thread(target=self.client_loop,args=[self,c])
            t.daemon = True
            t.start()
            self.TotalCons += 1
            print(f"Total Connections : {self.TotalCons}")

    def sendall(self,data):
        for e in self.clients:
            self.send(e,data)

    def send(self,client,data):
        data = self.get_publickey(client).encrypt(data.encode())
        client.send(data)

    def recv(self,client):
        data = self.get_publickey(client).decrypt(client.recv(3000)).decode()
        return data

    def recv_rsa(self,client):
        data = Utils().decrypt_rsa(client.recv(3000), self.PrivateKey)
        return data

    def close(self,c):
        self.clients.remove([c,self.get_publickey(c)])
        c.close()
        self.TotalCons -= 1
        print(f"Total Connections : {self.TotalCons}")

    def get_publickey(self,client):
        for e in self.clients:
            if e[0] == client:
                return e[1]

class Client:
    def __init__(self,host_ip,port=5432):
        self.key = Utils().make_random_pass()
        self.f = Fernet(Utils().password_to_key(self.key))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host_ip, port))
        self.init_connection()


    def init_connection(self):
        self.Server_PublicKey = rsa.PublicKey.load_pkcs1(self.client.recv(3000))
        self.send_rsa(self.key)


    def send_rsa(self,data):
        self.client.send(Utils().encrypt_rsa(data,self.Server_PublicKey))

    def send(self,data):
        self.client.send(self.f.encrypt(data.encode()))

    def recv(self):
        return self.f.decrypt(self.client.recv(3000)).decode()

    def close(self):
        self.client.close()

class Utils:


    def generate_keys_save(self):
        pubkey,privkey = rsa.newkeys(1024)
        with open("pubkey.pem","wb") as f:
            f.write(pubkey.save_pkcs1("PEM"))
            f.close()
        with open("privkey.pem", "wb") as f:
            f.write(privkey.save_pkcs1("PEM"))
            f.close()


    def generate_keys(self):
        pubkey,privkey = rsa.newkeys(1024)
        return pubkey,privkey



    def load_keys(self):
        with open("pubkey.pem", "rb") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
            f.close()
        with open("privkey.pem", "rb") as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())
            f.close()
        return pubkey , privkey



    def encrypt_rsa(self,data,pubkey):
        return rsa.encrypt(data.encode("ascii"),pubkey)


    def decrypt_rsa(self,data,privkey):
        try:
            return rsa.decrypt(data,privkey).decode("ascii")
        except:
            return False

    def password_to_key(self,password):
        salt = b'.-Kh)ura/)\xcef\xc8\x88u\xc2'
        password = password.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def make_random_pass(self):
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=35))
        return res
