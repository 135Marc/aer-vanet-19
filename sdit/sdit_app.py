import sys
import threading

from sdit_sender import sender
from sdit_receiver import receiver

PORT = 9997
IPV6 = '::1'

def main():
    r = threading.Thread(target=receiver, args=(PORT, IPV6, ))
    r.start()
    while True:
        sender(PORT, IPV6)

if __name__ == '__main__':
    main()
