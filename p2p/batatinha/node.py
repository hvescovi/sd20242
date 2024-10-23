# https://www.pythontutorial.net/python-concurrency/python-threading/

from client import *
from server import *
from config import *
from threading import Thread, Event
from hashTable import *
import time

SERVER_PIPE_PATH = "client_pipe"
CLINET_PIPE_PATH = "server_pipe"


class Node:

    def __init__(self):
        pass

    def run(self):
        HashTable.create_table()

        server = Server("224.3.29.50", 1234, 'bla/')
        client = Client("224.3.29.50", 1234, 'bla/')

        event = Event()

        server_thread = Thread(target=server.run)
        client_thread = Thread(target=client.run)

        server_thread.start()

        time.sleep(0.5)
        client_thread.start()


if __name__ == "__main__":
    node = Node()
    node.run()
