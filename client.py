import os
import socket 
import threading 
import sys
import pickle
import hashlib

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 12345

class Client: 
    def __init__(self, addr,hashlist):
       print("Setting up client")
       # set up socket
       self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

       # make the connection
       self.s.connect((addr, PORT))
    
       #create to work on a different thread
       #this thread is used to send message to the server
       send_thread = threading.Thread(target=self.send_message)
       send_thread.daemon = True
       send_thread.start()

        # this the list of hashes that the current peer has
       self.hashlist = hashlist

       while True:
           receive_thread = threading.Thread(target=self.recieve_message)
           receive_thread.start()
           receive_thread.join()
            #receive message from the server
           data = self.recieve_message()

           if not data:
               #the server has failed
               print("--------------Server failed-------------")
               break
           elif data[0:1] == b'\x10':
               print("Got peers")
               self.update_peers(data[1:])


    """
    This thread will deal with writing the recieved message into different files in the received folder
    """
    def recieve_message(self):
        print("------------Receiving-----------")
        while True:
            message = self.s.recv(1024)
            if not message:
                break
            received = pickle.loads(message)
            num_files = len(received)
            received_folder = './Folder_to_send/'
            upload = False
            for i in range(num_files):
                if self.hash_text(received[i]) not in self.hashlist:
                    with open(received_folder + 'file_' + str(i), 'w') as f:
                        f.write(received[i].decode('utf-8'))
                        print('writing', received[i].decode('utf-8'))
                        print("because not in this list:")
                        print(self.hashlist)
                        upload = True
            return received
        

    def hash_text(self, text):
        m = hashlib.sha256()
        m.update(text)
        hash = m.hexdigest()
        #print(hash)
        return hash

    

    """
    This method updates the list of peers
    """
    def update_peers(self, peers):
        p2p.peers = str(peers, "utf-8").split(',')[:-1]
    

    """
    This method is used to send the message
    """
    def send_message(self):
        try:
            self.s.send('req'.encode('utf-8'))
        except KeyboardInterrupt as e:
            print(e)
            return
