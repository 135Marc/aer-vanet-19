import json

def newPDU(type, ttl):
    pdu = '{"type": ' + type + '", ttl":' + str(ttl) + '}'
    return json.loads(pdu)

print(newPDU('HELLO',2))