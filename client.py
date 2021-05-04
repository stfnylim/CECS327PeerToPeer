"""
This file takes care of the client side of the peer to peer network
"""
import os
import socket 
import threading 
import sys
import pickle


HOST = '192.168.1.203'
PORT = 1234

class Client: 
    def __init__(self, addr):
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
            received_folder = './Folder_received/'
            for i in range(num_files):
                with open(received_folder + 'file_' + str(i), 'w') as f:
                    f.write(received[i].decode('utf-8'))
            return received


    

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
