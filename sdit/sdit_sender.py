import pickle

def sender(socket, port, groupipv6):
    socket.connect((groupipv6, port))

    while True:
        msg = input('-----msg------')
        socket.sendto(msg.encode('utf-8'), (groupipv6, port))

    