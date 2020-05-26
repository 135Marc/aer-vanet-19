import queue
import socket
import time
import threading

HEADERSIZE = 10
INFNAMES = {}
port = 9984

def infNamesList():
    lst = ''
    for k in INFNAMES:
        lst += k
        lst += '\n'
    return lst

def handleClient(clientsocket):
    #Send wellcome message
    #sendString(clientsocket, "Welcome to the server!")

    msg = '-'
    connected = True
    while connected:
        try:
            msg = receiveString(clientsocket)
            cmd = msg.split('/')
            method = cmd[0]
            value = ''
            if method == 'PUT':
                value = cmd[-1]
                cmd.pop()
            cmd.pop(0)
            info = '/'.join(cmd)
        except:
            method = ''
        if len(method) != 0:
            if method == 'GET':
                try:
                    info = INFNAMES[info]
                    sendString(clientsocket, info)
                except:
                    sendString(clientsocket, '400 File not found.')
            elif method == 'PUT': 
                try:
                    f = INFNAMES[info]
                    sendString(clientsocket, 'File already attached.')
                except:
                    INFNAMES[info] = value #alterar para a informação fornecida
                    sendString(clientsocket, 'File attached.')
            elif method == 'DEL':
                try:
                    del INFNAMES[info]
                    sendString(clientsocket, 'File deleted.')
                except:
                    sendString(clientsocket, '400 File not found.')
            elif method == 'LST':
                sendString(clientsocket, infNamesList())
            else:
                print('[METHOD not found]')
        else:
            connected = False
            print("[CONNECTION closed] disconnected.")

def receiveString(clientsocket):
    #Receber tamanho do datagrama
    byts = clientsocket.recv(HEADERSIZE)
    if representsInt(byts):
        size = int(byts)
        msg = clientsocket.recv(size)
        return msg.decode("utf-8")
    else:
        return ''

def sendString(clientsocket, msg):
    msg = '{:<10}'.format(len(msg)) + msg
    clientsocket.send(bytes(msg,"utf-8"))

def representsInt(s):
    try: 
        n = int(s)
        if n >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.bind((s.getsockname()[0], port))
s.listen(5)
print("[LISTENING] Server (tcp) is listening on port: " + str(port))

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()

    h = threading.Thread(target=handleClient, args=(clientsocket,))
    h.start()
    print("[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 1))
