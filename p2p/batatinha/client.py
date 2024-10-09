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

    def run(self) -> None:
        
        if not os.path.exists(self.client_dir):
            os.mkdir(self.client_dir)
        
        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        sock.settimeout(0.5)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        opcao = None
        while opcao != "0":
            opcao = input("Insira o que tu quer: \n 1 = get(name), 2 = put(GUID, dados), 3 = get(GUID) ou 0 para sair.")

            if opcao == 1:
                self.getByName()
            elif opcao == 2:
                pass
            elif opcao == 3:
                pass



    def getByName(self):
        message = input("--> File: ")
        
        data = '{"fileName": "' +  message + '"}'
        sent = sock.sendto(data.encode(), self.multicast_group)

        # Look for responses from all recipients
        while True:
            #print (sys.stderr, 'waiting to receive')
            print('--> waiting to receive')
            # limpa o socket
            #clear_buffer(sock)
            try:
                data, server = sock.recvfrom(1024)

            except socket.timeout:
                #print (sys.stderr, 'timed out, no more responses')
                print('--> timed out, no more responses :(')
                break
            else:
                parsed_data = json.loads(data.decode()) 
                #print (sys.stderr, 'received "%s" from %s' % (data, server))
                print(f'--> received from {server}: {parsed_data}')
                
                with open(os.path.join(self.client_dir, message), 'w') as file:
                    file.write(parsed_data['detail'])
                
                # Recebeu, mas tenta receber respostas de outros nós que possuem o arquivo
                while True:
                    #print (sys.stderr, 'waiting to receive')
                    print('*** jogando fora')
                    # limpa o socket
                    #clear_buffer(sock)
                    try:
                        data, server = sock.recvfrom(1024)

                    except socket.timeout:
                        #print (sys.stderr, 'timed out, no more responses')
                        print('*** timed out, no more responses')
                        break
