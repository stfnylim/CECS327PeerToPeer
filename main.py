import socket
from server import Server
from client import Client
import sys
import os
import hashlib

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)

cwd = os.getcwd()
uploadedfilesdir = os.path.join(cwd,'Folder_to_send')
#filelistdir = os.path.join(uploadedfilesdir,'.filelist')

class p2p:
    # list of local ip addresses of devices on our network
    peers = ['192.168.0.21','192.168.56.1',HOST]
    
#Helper function to convert a file to bytes
path_to_file = './default_file'


def read_folder(folder_path):

    files = os.listdir(folder_path)
    files = [folder_path + file for file in files]
    all_read_data = []
    for file in files:
        with open(file, 'r') as f:
            read_data = f.read()
            all_read_data.append(read_data.encode('utf-8'))

    return all_read_data


def main():
    folder_path = './Folder_to_send/'
    message = read_folder(folder_path)
    print(HOST)
    create_folder()
    hashlist = update_uploaded_files(folder_path)

    #print(len(message[0]))
    
    while True:
        try:
            print("---------------Connecting----------------")
            for peer in p2p.peers:
                try:
                    client = Client(peer,hashlist)
                except KeyboardInterrupt:
                    sys.exit(0)
                
                except:
                    pass

                # become the server
                try:
                    server = Server(message)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass
        except KeyboardInterrupt as e:
            print(e)
            sys.exit(0)
        
    
def create_folder():

    if (os.path.isdir(uploadedfilesdir)):
        print("shared folder is already made")
    else:
        os.mkdir(uploadedfilesdir)
        print("have just made the shared folder")
    print("You may now start uploading files or downloading files in your peer to peer network.")

"""
    this method will be responsible for hashing all the files within the
    shared folder and return a list of all the hashes
"""
def update_uploaded_files(folder_path):       
    files = os.listdir(folder_path)
    files = [folder_path + file for file in files]
    all_read_data = []
    print('These are the hashes for locally stored files:')
    for file in files:
        with open(file, 'r') as f:
            read_data = f.read()
            hash = hash_text(read_data.encode('utf-8'))
            all_read_data.append(hash)
    return all_read_data


def hash_text(text):
        m = hashlib.sha256()
        m.update(text)
        hash = m.hexdigest()
        print(hash)
        return hash

if __name__ == "__main__":
    main()
