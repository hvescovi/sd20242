# https://pymotw.com/2/socket/multicast.html

import socket
import struct
import os
import datetime
import json
from hashTable import HashTable
from operator import itemgetter

SERVER_DIR = "names/"


class Server:
    def __init__(self, addr_group, port, server_dir):
        self.multicast_group = addr_group
        self.server_address = ('', port)
        self.server_dir = server_dir
        self.address = None
        self.sock = None

    def run(self) -> None:

        if not os.path.exists(self.server_dir):
            os.mkdir(self.server_dir)

        # Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        self.sock.bind(self.server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Receive/respond loop
        while True:
            # print(sys.stderr, '\nwaiting to receive message')
            print('\n<<< waiting to receive message')
            data, self.address = self.sock.recvfrom(1024)

            # print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
            print('<<< received %s bytes from %s: %s' %
                  (len(data), self.address, data.decode('utf-8')))

            parsed_data = json.loads(data.decode('utf-8'))

            if 'fileName' in parsed_data:
                fileName = parsed_data['fileName']
                hash = HashTable.get(HashTable.name == fileName)
                self.returnContent(hash.id)

            elif 'guid' in parsed_data and 'dados' in parsed_data:
                guid = parsed_data['guid']
                dados = parsed_data['dados']
                self.putContent(guid, dados)

            elif 'guid' in parsed_data:
                guid = parsed_data['guid']
                hash = HashTable.get(HashTable.id == guid)
                self.returnContent(hash.id)

            elif 'sync' in parsed_data:
                self.syncDatabase()

    def returnContent(self, id):
        path = self.server_dir + str(id)

        # Verificar se o arquivo existe no diretório de arquivos do servidor
        if (os.path.exists(path)):
            # abrir arquivo
            openedFile = open(path, "r")
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
            print(f"<<< Respondendo o cliente {
                  self.address} - enviando: {resposta}")
            self.sock.sendto(resposta.encode(), self.address)

        # se nao abrir
        else:
            # nada
            print('<<< Não encontrou, fazendo nada...')

    def putContent(self, guid, dados):
        file = HashTable.create(id=guid, name=dados)
        file.save()

        print("Novo arquivo criado, GUID: ", guid)

    def serialize_datetime(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def syncDatabase(self):
        data = HashTable.select()
        allContent = [content.__data__ for content in data]

        allContent = {
            "header": "OK",
            "detail": allContent
        }

        allContent = json.dumps(allContent, default=self.serialize_datetime)

        print(f"Syncing...")
        self.sock.sendto(allContent.encode(), self.address)
