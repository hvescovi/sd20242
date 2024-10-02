# https://pymotw.com/2/socket/multicast.html

import socket
import struct
import sys
import os
import json

SERVER_DIR = "./out/4/"
SERVER_DIR_2 = "./out/5/"
SERVER_DIR_3 = "./out/6/"

multicast_group = '224.3.29.71'
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

def search_server_cont(server, string_pesquisar):
    oldpwd = os.getcwd()
    os.chdir(server)
    dados = os.listdir()
    grep = os.system("grep -l -r "+string_pesquisar+" > ../cache.txt")
    openedFile = open(oldpwd + "/cache.txt", "r")
    conteudo = openedFile.read()
    # remove o \n
    conteudo = conteudo.replace("\n", " | ")
    # remove as " devido a incompatibilidade com json
    conteudo = conteudo.replace('"', '')
    openedFile.close()
    print(conteudo)
    resposta = '{"header": "OK", "detail": "' + conteudo + '"}'
    os.chdir(oldpwd)
    sock.sendto(resposta.encode() , address)
    # print(dados)

def search_server_dir(server):
    # abrir arquivo
    openedFile = open(server + parsed_data['fileName'], "r")
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
    print(f"{server} - Respondendo o cliente {address} - enviando: {resposta}")
    sock.sendto(resposta.encode() , address)

# Receive/respond loop
while True:
    # print(sys.stderr, '\nwaiting to receive message')
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    #print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    print('received %s bytes from %s: %s' % (len(data), address, data.decode('utf-8')))

    parsed_data = json.loads(data.decode('utf-8')) 
    if (parsed_data['fileName'].split()[0] == "search"):
        search_server_cont("./out/", parsed_data['fileName'].split()[1])
    # Verificar se o arquivo existe no diretório de arquivos do servidor
    elif(os.path.exists(SERVER_DIR + parsed_data['fileName'])):
        search_server_dir(SERVER_DIR)
    elif(os.path.exists(SERVER_DIR_2 + parsed_data['fileName'])):
        search_server_dir(SERVER_DIR_2)
    elif(os.path.exists(SERVER_DIR_3 + parsed_data['fileName'])):
        search_server_dir(SERVER_DIR_3)
    # se nao abrir
    else:
        # nada
        print('Não encontrou, fazendo nada...')
    
    #print(sys.stderr, 'sending acknowledgement to', address)
    #print('sending acknowledgement to', address)
    #sock.sendto('ack'.encode(), address)