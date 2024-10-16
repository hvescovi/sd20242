import socket
import struct
import json
import os
from threading import Event

def clear_buffer(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            else:
                print("liberando socket....")
        except:
            print("socket vazio!")
            break


class Client:

    def __init__(self, addr_group, port, client_dir):
        self.multicast_group = (addr_group, port)
        self.client_dir = client_dir
        self.sock = None

    def run(self) -> None:
        
        if not os.path.exists(self.client_dir):
            os.mkdir(self.client_dir)
        
        # Create the datagram socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        self.sock.settimeout(0.5)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        opcao = None
        while opcao != "0":
            opcao = input("Insira o que tu quer: \n 1 = get(name), 2 = put(GUID, dados), 3 = get(GUID) ou 0 para sair.")

            if opcao == "1":
                message = input("--> File: ")
                self.getByName(message)
            elif opcao == "2":
                guid = input("--> GUID: ")
                dados = input("--> Dados: ")
                self.putData(guid, dados)
            elif opcao == "3":
                guid = input("--> GUID: ")
                self.getByGuid(guid)

    def getByName(self, message):
        data = '{"fileName": "' +  message + '"}'
        sent = self.sock.sendto(data.encode(), self.multicast_group)
        self.printResult(message)
        

    def getByGuid(self, guid):
        data = '{"guid": "' +  guid + '"}'
        sent = self.sock.sendto(data.encode(), self.multicast_group)
        self.printResult(guid)

    def putData(self, guid, dados):
        data = {
            "guid" : guid,
            "dados": dados
        }
        
        data = json.dumps(data)
        
        sent = self.sock.sendto(data.encode(), self.multicast_group)
        
    def printResult(self, content):
        while True:
            print('--> waiting to receive')
            try:
                data, server = self.sock.recvfrom(1024)

            except socket.timeout:
                print('--> timed out, no more responses :(')
                break
            else:
                parsed_data = json.loads(data.decode()) 
                print(f'--> received from {server}: {parsed_data}')
                
                with open(os.path.join(self.client_dir, content), 'w') as file:
                    file.write(parsed_data['detail'])
                
                # Recebeu, mas tenta receber respostas de outros nós que possuem o arquivo
                while True:
                    print('*** jogando fora')
                    try:
                        data, server = self.sock.recvfrom(1024)

                    except socket.timeout:
                        print('*** timed out, no more responses')
                        break