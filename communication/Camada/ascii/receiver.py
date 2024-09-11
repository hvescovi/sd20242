# https://pymotw.com/2/socket/multicast.html

import socket
import struct
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
import os

multicast_group = '224.3.29.71'
server_address = ('', 10001)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    # print(sys.stderr, '\nwaiting to receive message')
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    #print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    print('received %s bytes from %s' % (len(data), address))

    # Decode data from bytes to string
    decoded_data = data.decode('utf-8')

    #print(sys.stderr, data)
    print("executing: ", decoded_data)

    # Format the decoded message using pyfiglet
    try:
        ascii_art = figlet_format(decoded_data, font='starwars')
        x = cprint(ascii_art, 'yellow', 'on_red', attrs=['bold'])
        print(x)
    except Exception as e:
        print(f"Error formatting text with figlet: {e}")
    
    #print(sys.stderr, 'sending acknowledgement to', address)
    print('sending acknowledgement to', address)
    sock.sendto('ack'.encode(), address)