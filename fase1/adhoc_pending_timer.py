import time
import sys

def pendingTimeout(timeout, pendingTable, elem):
    time.sleep(timeout)
    if pendingTable.check(elem):
        pendingTable.rm(elem)
        print('[TIMEOUT]', elem[1], elem[0])
        sys.exit()