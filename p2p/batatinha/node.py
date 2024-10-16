## https://www.pythontutorial.net/python-concurrency/python-threading/

from client import *
from server import *
from config import *
from threading import Thread, Event
from hashTable import *

SERVER_PIPE_PATH = "client_pipe"
CLINET_PIPE_PATH =  "server_pipe"

class Node:

    def __init__(self):
        pass

    def run(self):
        HashTable.create_table()
        
        client = Client("224.3.29.50", 1234, 'bla1/')
        server = Server("224.3.29.50", 1234, 'bla2/')

        event = Event()
        
        client_thread = Thread(target=client.run)
        server_thread = Thread(target=server.run)

        client_thread.start()
        server_thread.start()

        
if __name__ == "__main__":
    node = Node()
    node.run()
        