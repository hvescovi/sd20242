# https://pymotw.com/2/socket/multicast.html

import socket
import struct
import sys
import os
import json

SERVER_DIR1 = "./out/0/"
SERVER_DIR2 = "./out/1/"
SERVER_DIRS = [SERVER_DIR1, SERVER_DIR2]

multicast_group = '224.3.29.76'
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

def searchByFileName(sock, address, SERVER_DIR, responseContent):
    if(os.path.exists(SERVER_DIR + responseContent)):
        openedFile = open(SERVER_DIR + responseContent, "r")
        contentFileName = openedFile.read()
        contentFileName = contentFileName[:-1]
        contentFileName = contentFileName.replace('"', '')
        openedFile.close()
        response = '{"header": "OK", "detail": "' + contentFileName + '"}'
        print(f"Respondendo o cliente {address} - enviando: {response}")
        sock.sendto(response.encode() , address)
    else: 
        print('Não encontrou, fazendo nada...')

def searchByFileContent(SERVER_DIR, responseContent):
    resultados = []
    for root, dirs, files in os.walk(SERVER_DIR):
        for fileName in files:
            filePath = os.path.join(root, fileName)
            file = open(filePath, 'r', encoding='utf-8')
            fileContent = file.read()
            if responseContent in fileContent:
                resultados.append(filePath)
            file.close()
    
    return resultados

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    print('received %s bytes from %s: %s' % (len(data), address, data.decode('utf-8')))

    parsed_data = json.loads(data.decode('utf-8')) 

    for SERVER_DIR in SERVER_DIRS: 
        responseContent =  parsed_data['content']
        
        if not responseContent:
            continue 
        
        isFileName = parsed_data['isFileName'] == 's'
        
        if isFileName: 
            searchByFileName(sock, address, SERVER_DIR, responseContent)
        else: 
            print(searchByFileContent(SERVER_DIR, responseContent))
