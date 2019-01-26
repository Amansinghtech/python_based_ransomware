import socket
import threading
import socket
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def keygen(passwd, file_name):
    password = passwd
    salt = b'\x82k\x19r%j\xe6\xf6\xda\x94&h9\xfd\xba\x0c'
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000000,
            backend=default_backend()
            )
    
    key=base64.urlsafe_b64encode(kdf.derive(password))

    file = open(file_name+'.key','wb')
    file.write(key)
    file.close()
    return key

def ClientHandler(cl, ad):
    client_data = cl.recv(2048)
    if client_data.decode().replace('\n','') == 'Start':
        print('keygen started: ')
        otp = Fernet.generate_key()
        print('generated OTP: %s'%otp.decode())
        secret = keygen(otp, ad[0])
        print('secret key is: %s'%secret.decode())
        cl.send(secret)
        data = cl.recv(2048)
        print(data.decode())
        print('encryption started')
        cl.close()


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print('started Listening on %s:%d'%(host, port))
    while True:
        client, addr = server.accept()
        print('got connection from %s:%d'%(addr))
        th = threading.Thread(target=ClientHandler, args=(client, addr,), daemon=True)
        th.start()

start_server('0.0.0.0',4567)