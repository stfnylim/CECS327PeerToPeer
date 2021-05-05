
from server import Server
from client import Client
import sys
import os
import socket
import hashlib

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)

cwd = os.getcwd()
uploadedfilesdir = os.path.join(cwd,'Folder_to_send')
filelistdir = os.path.join(uploadedfilesdir,'.filelist')

class p2p:
    #list of local ip addresses of laptops on our network
    peers = [HOST, '192.168.0.21']
    #peers = ['192.168.1.203', '192.168.1.68']



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

    create_folder()
    hashlist = update_uploaded_files(folder_path)
    print(len(message[0]))
    
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
    for file in files:
        with open(file, 'r') as f:
            read_data = f.read()
            hash = hash_text(read_data.encode('utf-8'))
            all_read_data.append(hash)
    return all_read_data

"""
    uploadedfiles = os.listdir(os.path.join(cwd, 'Folder_to_send'))
    print('These are the uploaded files in the following shared folder:')
    hashlist = []
    for i in uploadedfiles:
        # this is to hash the file at the specified location
        print(i)
       
        path_to_file = os.path.join(uploadedfilesdir, i)
        file_hash = hashlib.md5()
        with open(path_to_file, 'rb') as afile:
            buf = afile.read()
            file_hash.update(buf)
        hex = file_hash.hexdigest()
        print("file hash for", i,":\n",hex)
        hashlist.append(hex) # adds the hash to the list
    # after finishing adding the list of hashes return the list
    print("The final list of hashes is:")
    print(*hashlist, sep = "\n")
    return hashlist
"""
def hash_text(text):
        m = hashlib.sha256()
        m.update(text)
        hash = m.hexdigest()
        print(hash)
        return hash

if __name__ == "__main__":
    main()
