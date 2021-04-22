"""
    Main will be in charge of converting from client to server or server to client
"""
import socket
import threading
import sys
import time
import fileio

class main:
    # we also include ourselves as a default peer to the network
    peers = ['192.168.0.7', '192.168.0.15','192.168.0.12']

def main():
    # if the server ever breaks, we will make the client a new server
    msg = fileIO.convert_to_bytes()

    while True:
        try:
            print("-" * 10 + 'Connecting...' + '-' *10)

            # sleeping any time between 1 to 5 secs
            time.sleep(randint(1,2))
            # for all the peers in the peers list
            for peer in main.peers:
                # Try to instantiate a client to set up a connection
                try:
                    # The client will be made to connect to the network
                    # its responsibility will be to upload the file to the machine
                    client = client(peer)
                    print('Have made a client with HOST: '+ peer + '\n')
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                # Try to also set up the server for the same IP address
                try:
                    # The server will be made to connect to the network
                    # its responsibility will be to upload files to the other peers
                    server = server(msg)
                    print('Have made a server with HOST: ' + peer + '\n')
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass
        except KeyboardInterrupt as e:
            sys.exit(0)

if __name__ == "__main__":
    main()


