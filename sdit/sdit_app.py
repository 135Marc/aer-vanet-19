import sys
import threading

from sdit_sender import sender
from sdit_receiver import receiver

MYPORT = 9999
MYGROUP_6 = '::'

def main():
    r = threading.Thread(target=receiver, args=(MYPORT, MYGROUP_6, ))
    r.start()
    s = threading.Thread(target=sender, args=(MYPORT, MYGROUP_6,))
    s.start()

if __name__ == '__main__':
    main()
