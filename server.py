"""
This file takes part of the server side of the peer to peer network
"""
import os
import socket 
import threading 
import tqdm
import sys
import pickle

HOST = '192.168.1.203'
PORT = 1234

class Server: 
    def __init__(self, msg):
        try:
            print("Setting up server")
            # the message to send in bytes
            self.msg = msg
            # define a socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.connections = []
            #list of peers 
            self.peers = []
            # bind the socket
            self.s.bind((HOST, PORT))

            # listen for connections
            self.s.listen(1)
            self.run()
        except Exception as e:
            print(e)
            sys.exit()



    """
    Sends list of messages to clients using pickle
    """
    def handler(self, connection, a):
        try:
            while True:
                # server recieves the message
                data = connection.recv(1024)
                for connection in self.connections:
                    if data and data.decode('utf-8') == "req":
                        print("----------------------Sending-------------------")
                        print("message ", self.msg)
                        data = pickle.dumps(self.msg)
                        connection.send(data)
                        #cwd = os.getcwd()
                        #filename = "./data_laptop_1.txt"

                        # if the connection is still active we send it back the data
                        # this part deals with uploading of the file
                        '''
                        connection.send(self.msg)
                        fileIO.create_file(data)
                        '''
                        #send file to client??
                        #convert_to_music(self.msg)
                        '''
                        connection.send(f"{filename}{SEPARATOR}{filesize}".encode())
                        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                        with open(filename, "rb") as f:
                            while True:
                                bytes_read = f.read(1024)
                                if not bytes_read:
                                    break
                                connection.sendall(bytes_read)
                                progress.update(len(bytes_read))
                        '''

        except Exception as e:
            print(e)
            sys.exit()




    """
    Run the server
    """
    def run(self):
        # constantly listen for connections
        print("---------------------Server Running----------------------")
        while True:
            #receive an upcoming connection
            connection, a = self.s.accept()
            #append to the list of peers 
            self.peers.append(a)
            print("Peers are: {}".format(self.peers) )
            self.send_peers() #send a list of peers to all the neighbor nodes
            # create a thread for a connection (handle multiple connections without blocking)
            c_thread = threading.Thread(target=self.handler, args=(connection, a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(connection)#add to the list of connections
            print("{}, connected".format(a))
            



    """
    send a list of peers to all the peers that are connected to the server
    """
    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list = peer_list + str(peer[0]) + ","
        for connection in self.connections:
            # We add a special character at the begining of the message
            #This way we can differentiate if we recieved a message or a a list of peers
            data = b'\x10' + bytes(peer_list, 'utf-8')
            connection.send(b'\x10' + bytes(peer_list, 'utf-8'))

