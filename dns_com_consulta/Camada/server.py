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
    pastas.append(sys.argv[3])
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

    print("PARSED_DATA: ", parsed_data)

    if 'fileName' in parsed_data:
        # Buscar o conteúdo do arquivo
        file_name = parsed_data['fileName']

        print("FILNE_NAME: ", file_name)

        #file_name = file_name.split()

        #file_Name = file_name[1]

        for i in pastas:
            file_path = f"./out/{i}/{file_name}"
            # Verificar se o arquivo existe no diretório de arquivos do servidor
            if os.path.exists(file_path):
                # abrir arquivo
                with open(file_path, "r") as openedFile:
                    conteudo = openedFile.read().replace('"', '').strip()
                # Preparar resposta
                resposta = json.dumps({"header": "OK", "detail": conteudo})
                # enviar o conteudo
                print(f"Respondendo o cliente {address} - enviando: {resposta}")
                sock.sendto(resposta.encode(), address)
                break
        else:
            print('Arquivo não encontrado.')

    elif 'search' in parsed_data:
        # Buscar o padrão nos arquivos
        search_term = parsed_data['search']
        found_files = []
        for i in pastas:
            for root, dirs, files in os.walk(f"./out/{i}"):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        if search_term in f.read() or search_term in file:
                            found_files.append(file)
                            
        resposta = json.dumps({"header": "OK", "detail": found_files})
        print(f"Respondendo o cliente {address} - enviando: {resposta}")
        sock.sendto(resposta.encode('utf-8'), address)