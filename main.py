
from server import Server
from client import Client
import sys
import os

class p2p:
    #list of local ip addresses of laptops on our network
    peers = ['192.168.1.68', '192.168.1.203']
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
    print(len(message[0]))
    
    while True:
        try:
            print("---------------Connecting----------------")
            for peer in p2p.peers:
                try:
                    client = Client(peer)
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
    

if __name__ == "__main__":
    main()
