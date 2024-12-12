# https://pymotw.com/2/socket/multicast.html

import socket
import struct
from threading import Event
import os
import json

SERVER_DIR = "names/"

class Server:
    def __init__(self, addr_group, port, server_dir):
        self.multicast_group = addr_group
        self.server_address = ('', port)
        self.server_dir = server_dir

    def run(self) -> None:
        
        if not os.path.exists(self.server_dir):
            os.mkdir(self.server_dir)

        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        sock.bind(self.server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            # Receive/respond loop
        while True:
            # print(sys.stderr, '\nwaiting to receive message')
            print('\n<<< waiting to receive message')
            data, address = sock.recvfrom(1024)
            
            #print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
            print('<<< received %s bytes from %s: %s' % (len(data), address, data.decode('utf-8')))

            parsed_data = data.decode('utf-8')
            print(parsed_data)
            parsed_data = json.loads(parsed_data)

            if("index" in  list(parsed_data.keys())):
                parsed_data = parsed_data["index"]
                json_object = {}
                with open(f'{SERVER_DIR}index.json', 'r') as openfile:
                    # Reading from json file
                    json_object = json.load(openfile)
                
                # print(json.loads(parsed_data))
                print(list(parsed_data.keys()))
                json_object[list(parsed_data.keys())[0]] = parsed_data[list(parsed_data.keys())[0]]

                json_object = json.dumps(json_object, indent=4)

                with open(f'{SERVER_DIR}index.json', "w") as outfile:
                    outfile.write(json_object)


            # Verificar se o arquivo existe no diretório de arquivos do servidor
            if("fileName" in list(parsed_data.keys()) and os.path.exists(self.server_dir + parsed_data['fileName'])):
                # abrir arquivo
                openedFile = open(self.server_dir + parsed_data['fileName'], "r")
                # ler o conteudo
                conteudo = openedFile.read()
                # remove o \n
                conteudo = conteudo[:-1]
                # remove as " devido a incompatibilidade com json
                conteudo = conteudo.replace('"', '')
                openedFile.close()
                # Preparar resposta
                resposta = '{"header": "OK", "detail": "' + conteudo + '"}'
                # enviar o coteudo
                print(f"<<< Respondendo o cliente {address} - enviando: {resposta}")
                sock.sendto(resposta.encode() , address)
            
            # se nao abrir
            else:
                # nada
                print('<<< Não encontrou, fazendo nada...')
            
            #print(sys.stderr, 'sending acknowledgement to', address)
            #print('sending acknowledgement to', address)
            #sock.sendto('ack'.encode(), address)