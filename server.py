"""

server class will be able to set up a connection by listening
for further connections. It is a temporary mode of the peer.
"""

# import modules
import socket
import threading
import sys
import time

# constants
HOST = '192.168.0.20'
PORT = 12345
BYTE_SIZE = 1024
PEER_BYTE_DIFFERENTIATOR = b'\x11'

class Server:
    """
    constructor
    """

    def __init(self, msg):
        try:
            # message that will be uploaded in bytes
            self.msg = msg
            # This is defining the endpoint socket for the server side
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # This is the list of connections that are connected to this server
            self.connections = []
            # The list of peers that are connected to this server
            self.peers = []
            # Connects to the socket with the IP address and port number
            self.s.bind((HOST, PORT))
            # Now listening for further connections
            self.s.listen(1)
            # outputs that the server is running and listening for connections
            print("-"*10+ HOST + ' is now up and running'+'-'*10)

            self.run()
        # if an exception occurs, the program will exit
        except Exception as e:
            sys.exit()
    """
    sending messages to the client and closing the connection if they
    have left
    """
    def handler(self, connection, a):

        try:
            while True:
                # server receives the message
                data = connection.recv(BYTE_SIZE)
                # for all the connections within the connection list
                for connection in self.connections:
                    # If the peer wants to disconnect from the server
                    if data and data.decode('utf-')[0].lower() == 'q':
                        # disconnects the peer from the network
                        self.disconnect(connection, a)
                        return
                    # If the peer wants to connect to the server
                    elif data and data.decode('utf-8') == "req":
                        # outputs that the peer is uploading the data to this server
                        print("-"*10 + connection + " uploading " + "-"*10)
                        connection.send(self.msg)

        except Exception as e:
            sys.exit()


    """
        When the user disconnects, this method will remove itself from the peers list.
    """
    def disconnect(self, connection, a):
        # removes itself from
        self.connections.remove(connection)
        self.peers.remove(a)
        connection.close()
        self.send_peers()
        print('{}, disconnected'.format(a))
        print()
    """
        This is used to run the actual server
        This creates the threads for each of the clients
    """
    def run(self):
        # constantly listen
        while True:
            connection, a = self.s.accept()
            # append to the list of peers
            self.peers.append(a)

            print('Peers are: {}'.format(self.peers))
            self.send_peers()

            c_thread = threading.Thread(target=self.handler, args=(connection,a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(connection)
            print("{}, connected".format(a))
            print("-"*50)


    """
        This method sends this list of peers to the other peers that are 
        connected to the network
    """
    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list= peer_list + str(peer[0])+","
        for connection in self.connections:
            # to differentiate between messages or list of peers,
            # we can add the \x11 to the peers list
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8')
            connection.send(PEER_BYTE_DIFFERENTIATOR + bytes(peer_list))
