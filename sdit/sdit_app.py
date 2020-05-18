import sys
import threading
import socket
from sdit_sender import sender
from sdit_receiver import receiver

MYPORT = 9999
MYGROUP_6 = '::'

def main():
    SOCKET = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    r = threading.Thread(target=receiver, args=(SOCKET, MYPORT, MYGROUP_6, ))
    r.start()
    s = threading.Thread(target=sender, args=(SOCKET, MYPORT, MYGROUP_6,))
    s.start()

if __name__ == '__main__':
    main()
