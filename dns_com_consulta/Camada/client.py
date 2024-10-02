
import socket
import struct
import sys
import json

multicast_group = ('224.3.29.79', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.5)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

while True:
    try:
        message = input("File: ")

        # Separar o comando e o parâmetro
        command_parts = message.split(" ", 1)

        if len(command_parts) < 2:
            print("Comando ou parâmetro inválido.")
            exit()

        operation = command_parts[0]
        parameter = command_parts[1]    

        # Montar a mensagem baseada no comando
        if operation == "fileName":
            data = json.dumps({"fileName": parameter})
        elif operation == "search":
            data = json.dumps({"search": parameter})
        else:
            print("Comando inválido.")
            exit()
        
        #data = '{"fileName": "' +  message + '"}'
        sent = sock.sendto(data.encode('utf-8'), multicast_group)

        # Look for responses from all recipients
        while True:
            #print (sys.stderr, 'waiting to receive')
            print ('waiting to receive')
            try:
                data, server = sock.recvfrom(4096)

            except socket.timeout:
                #print (sys.stderr, 'timed out, no more responses')
                print ('timed out, no more responses :(')
                break
            else:
                parsed_data = json.loads(data.decode('utf-8')) 
                #print (sys.stderr, 'received "%s" from %s' % (data, server))
                print ('received "%s" from %s' % (parsed_data['detail'], server))
                break

    finally:
        pass
        #print (sys.stderr, 'closing socket')
        #print ('closing socket')
        #sock.close()