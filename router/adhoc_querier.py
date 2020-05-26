
import socket

def get(msg):
    #Pedido ao servidor tcp
    sok = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    IPv6 = sok.getsockname()[0]
    sok.connect((IPv6, 9988))

    sendString(sok, msg)
    rec_msg = receiveString(sok)
    print(rec_msg)

    sok.close()
    return rec_msg

def receiveString(s):
    #Receber tamanho do datagrama
    byts = s.recv(HEADERSIZE)
    if byts and representsInt(byts):
        size = int(byts)
        msg = s.recv(size)
        return msg.decode("utf-8")
    else:
        return ''

def sendString(clientsocket, msg):
    msg = '{:<10}'.format(len(msg)) + msg
    clientsocket.send(bytes(msg,"utf-8"))