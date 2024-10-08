import socket
import struct
import sys
import time

message = 'very important data'
multicast_group = ('224.3.29.71', 10001)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

def progress_bar(duration=5):
    for i in range(100):
        time.sleep(duration / 100)
        sys.stdout.write('\r[' + '=' * (i // 2) + '>' + ' ' * (50 - i // 2) + ']')
        sys.stdout.flush()
    print()

while True:
    progress_bar()
    
    print("waiting for a command (q = quit): ")
    message = input("Command: ")
    if message == 'q':
            break
    # Send data to the multicast group
    #print (sys.stderr, 'sending "%s"' % message)
    print ('sending "%s"' % message)
    sent = sock.sendto(message.encode(), multicast_group)

    # Look for responses from all recipients
    while True:
        #print (sys.stderr, 'waiting to receive')
        print ('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            #print (sys.stderr, 'timed out, no more responses')
            print ('timed out, no more responses')
            break
        else:
            #print (sys.stderr, 'received "%s" from %s' % (data, server))
            print ('received "%s" from %s' % (data, server))

#print (sys.stderr, 'closing socket')
print ('closing socket')
sock.close()
