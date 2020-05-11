import time

def rmAwaitPdu(rplyawait, elem, interval):
    time.sleep(interval)
    if rplyawait.checkElem(elem):
        rplyawait.rmElem(elem)
        print('Response timeout for ', elem)
        sys.exit()