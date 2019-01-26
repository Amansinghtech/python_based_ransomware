import threading
import os
from cryptography.fernet import Fernet

print('Please Run it as Admin or Root for better decryption process')
print('\n')
key_path = input('enter the path for Decryption key: ')
file = open(key_path, 'rb')
secret_key = file.read()
file.close()

def decryptor(path):

    with open(path, 'rb') as f:
        data = f.read()
    
    tool = Fernet(secret_key)
    try:
        decrypted_data = tool.decrypt(data)
        new_name = path.replace('.crypt', '')

        with open(new_name, 'wb') as f:
            f.write(decrypted_data)
        f.close()
        os.remove(path)
    except:
        print("Error: Not Permitted")
    else:
        print('decryption sucessful')


def threader(path):
    th = threading.Thread(target=decryptor, args=(path,), daemon=True)
    th.start()


def dir_walker():
    extensions = ['.crypt']
    for root, dirs, files in os.walk("c:/"):
        for file in files:
            for ext in extensions:    
                if file.endswith(ext):
                    ally = os.path.join(root, file)
                    print(ally)
                    threader(ally)
    
    
dir_walker()
