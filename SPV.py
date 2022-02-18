"""
SPV 1.0.0 (Secure Password Verification)
This can be used to Verify a password without
sharing the real password. Instead, ask for hidden
proof like make the client do something that can
be done only using the correct password.
"""


from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import random


class SPV:
    def __init__(self,socket):
        self.sock = socket
    def GetVerified(self,password):
        """
        This function can be used to get verified
        by the server , it uses the socket set
        while initialising of the SPV class.
        """
        try:
            eq_1 = self.sock.recv(1260)
            self.sock.send(".".encode())
            eq_2 = self.sock.recv(1260)
            self.sock.send(self.make_sum(eq_1,eq_2,password))
            ret = self.sock.recv(1260)
            f = Fernet(self.password_to_key(password))
            ret = f.decrypt(ret).decode()
            if ret == "ok":
                return True
            else:
                return False
        except:
            return False
    def Verify(self,real_password,sock):
        """
        This function can be used to verify
        a client who is trying to get verified
        using the GetVerified function of the SPV
        module. It uses the socket set
        while calling this function.
        """
        try:
            f = Fernet(self.password_to_key(real_password))
            num_1 = random.randint(1,1000000000000000000000000)
            num_2 = random.randint(1,1000000000000000000000000)
            sum = num_1+num_2
            sock.send(f.encrypt(str(num_1).encode()))
            sock.recv(1260)
            sock.send(f.encrypt(str(num_2).encode()))
            ret = sock.recv(1260)
            ret = f.decrypt(ret)
            ret = int(ret.decode())
            if ret == sum:
                ret_code = f.encrypt("ok".encode())
                sock.send(ret_code)
                return True
            else:
                ret_code = f.encrypt("no".encode())
                sock.send(ret_code)
                return False
        except:
            return False
    def make_sum(self,en_1,en_2,password):
        f = Fernet(self.password_to_key(password))
        num_1 =  int(f.decrypt(en_1).decode())
        num_2 = int(f.decrypt(en_2).decode())
        return f.encrypt(str(num_1+num_2).encode())
    def password_to_key(self,password):
        salt = b'.-Kh)ura/)\xcef\xc8\x88u\xc2'
        password = password.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

if __name__ == '__main__':
    pass
