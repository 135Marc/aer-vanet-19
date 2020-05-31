import time
import sys

def pendingTimeout(timeout, pendingTable, elem):
    time.sleep(timeout)
    if pendingTable.check(elem[0]):
        pendingTable.rm(elem[0])
        print('[TIMEOUT]', elem[1], elem[0])
        sys.exit()