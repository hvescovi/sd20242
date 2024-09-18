# https://pymotw.com/2/socket/multicast.html

import socket
import struct
import sys
import os
import json

#SERVER_DIR = "./out/1/"
# #SERVER_DIR = 0

multicast_group = '224.3.29.79'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

pastas = []
if len(sys.argv) > 2:
    pastas.append(sys.argv[1])
    pastas.append(sys.argv[2])
else:
    print("Forneça dois nomes de pastas")
    sys.exit()

# Receive/respond loop
while True:

    # print(sys.stderr, '\nwaiting to receive message')
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    #print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    print('received %s bytes from %s: %s' % (len(data), address, data.decode('utf-8')))

    parsed_data = json.loads(data.decode('utf-8')) 

    for i in pastas:
    # Verificar se o arquivo existe no diretório de arquivos do servidor
        if(os.path.exists("./out/" + str(i) + "/" + parsed_data['fileName'])):
            # abrir arquivo
            openedFile = open("./out/" + str(i) + "/" + parsed_data['fileName'], "r")
            # ler o conteudo
            conteudo = openedFile.read()
            # remove o \n
            conteudo = conteudo[:-1]
            # remove as " devido a incompatibilidade com json
            conteudo = conteudo.replace('"', '')
            openedFile.close()
            # Preparar resposta
            resposta = '{"header": "OK", "detail": "' + conteudo + '"}'
            print("Pasta: ", i)
            # enviar o coteudo
            print(f"Respondendo o cliente {address} - enviando: {resposta}")
            sock.sendto(resposta.encode() , address)
    
        # se nao abrir
        else:
            # nada
            print('Não encontrou, fazendo nada...')
    
    #print(sys.stderr, 'sending acknowledgement to', address)
    #print('sending acknowledgement to', address)
    #sock.sendto('ack'.encode(), address)