import time
import sys

def rmAwaitPdu(rplyawait, elem, interval, answers):
    time.sleep(interval)
    if rplyawait.checkElem(elem):
        rplyawait.rmElem(elem)
        print('Response timeout for ', elem)
        answers.put('not found')
        sys.exit()