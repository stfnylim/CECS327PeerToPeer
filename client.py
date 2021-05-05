<<<<<<< Updated upstream
"""
    This class is responsible for the client part of the peer.
    It will be responsible for uploading the files unto the machine
"""

import socket
import threading
import sys
import time
import fileIO

# constants
PORT = 12345
BYTE_SIZE = 1024

class Client:
    def __init(self,addr):
        # define the socket on the client side
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # This will allow the program to use a socket that was just closed
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSADDR,1)

        # make the connection to the socket using IP address and port number
        self.s.connect((addr, PORT))
        self.previous_data = None

        # creates a thread to start interacting with peers
        i_thread = threading.Thread(target = self.send_message)
        i_thread.daemon = True
        i_thread.start()

        while True:
            r_thread = threading.Thread(target= self.receive_message)


    """
        This is outputting the message that was received
    """
    def receive_message(self):
        try:

            print("-"*10 + ' Receiving message ' + "-"*10)

            data = self.s.recv(BYTE_SIZE)

            print(data.decode('utf-8'))

            print("\n Received message: \n")

            if self.previous_data != data:
                fileIO.create_file(data)
                self.previous_data = data

            # TODO download file to the actual computer

            return data
        except KeyboardInterrupt:
            self.send_disconnect_signal()


    """
        This will update the peers list
    """
    def update_peers(self, peers):
        # The actual format of the list would be 12.0.0.1, 13.0.0.1
        # -1 is necessary to remove the null value
        p2p.peers = str(pee)

=======
"""
This file takes care of the client side of the peer to peer network
"""
import os
import socket 
import threading 
import sys
import pickle
import hashlib

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 1234

class Client: 
    def __init__(self, addr,hashlist):
       print("Setting up client")
       # set up socket
       self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

       # make the connection
       self.s.connect((addr, PORT))
    
       #create to work on a different thread
       #this thread is used to send message to the server
       i_thread = threading.Thread(target=self.send_message)
       i_thread.daemon = True
       i_thread.start()

        # this the list of hashes that the current peer has
       self.hashlist = hashlist

       while True:
           r_thread = threading.Thread(target=self.recieve_message)
           r_thread.start()
           r_thread.join()
            #receive message from the server
           data = self.recieve_message()

           if not data:
               #the server has failed
               print("--------------Server failed-------------")
               break

           elif data[0:1] == b'\x10':
               print("Got peers")
               # first byte is the byte '\x11 we added to make sure that we have peers
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
            received_folder = './Folder_to_receive/'
            upload = False
            for i in range(num_files):
                if self.hash_text(received[i]) not in self.hashlist:
                    with open(received_folder + 'file_' + str(i), 'w') as f:
                        f.write(received[i].decode('utf-8'))
                        print('writing', received[i].decode('utf-8'))
                        print("because not in this list:")
                        print(self.hashlist)
                        upload = True
            
        if upload:
            print("The files within the folder is now updated with new files")
        else:
            print("The files were the same, so no files were updated")
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
        # our peers list would lool like 127.0.0.1, 192.168.1.1, 
        # we do -1 to remove the last value which would be None
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
>>>>>>> Stashed changes
