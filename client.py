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

