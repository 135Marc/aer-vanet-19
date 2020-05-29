import time
import sys

def rmAwaitPdu(rplyawait, elem, interval, answersr,answersm, ty):
    time.sleep(interval)
    if rplyawait.checkElem(elem):
        rplyawait.rmElem(elem)
        print('Response timeout for ', elem)
        if ty == 'ROUTE_REQUEST'
            answersr.put('not found')
        else:
            answersm.put(elem, 'not found.')
        sys.exit()