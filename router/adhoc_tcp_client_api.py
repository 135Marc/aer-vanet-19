import queue
import socket
import time
import threading
from adhoc_pdu import PDU

def get(name, port, table, msgqueue, answers):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind((s.getsockname()[0], port))
    s.listen(5)
    print("[LISTENING] Server (tcp) is listening on port: " + str(port))

    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()

        h = threading.Thread(target=handleClient, args=(name, clientsocket, table, msgqueue, answers ))
        h.start()
        print("[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 1))


HEADERSIZE = 10

def handleClient(name, clientsocket, table, msgqueue, answers):
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
            if method == 'PTR':  
                req_msg = table.getStr()
                sendString(clientsocket, table.getStr())
            else:
                if not table.exists('C'):
                    newpdu = PDU(name, 'ROUTE_REQUEST', 5, None, 'C', '', [name])
                    msgqueue.put(newpdu)

                    up = answers.get()
                    if up == 'not found':
                        req_msg = 'Server unavailable.'
                        sendString(clientsocket, req_msg)
                    else:
                        if method == 'GET' or method == 'LST' or method == 'DEL' or method == 'PUT':
                            print(method)
                            tmsg = method + '/' + info
                            if method == 'PUT':
                                tmsg += '/' + value

                            newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'C', tmsg, [name])
                            msgqueue.put(newpdu)
                            
                            pdu = answers.get()
                            req_msg = pdu.getMsg()
                            sendString(clientsocket, req_msg)
                            table.remove('C')
                        else:
                            print('[METHOD not found]')
                elif method == 'GET' or method == 'LST' or method == 'DEL' or method == 'PUT':
                    print(method)
                    tmsg = method + '/' + info
                    if method == 'PUT':
                        tmsg += '/' + value

                    newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'C', tmsg, [name])
                    msgqueue.put(newpdu)
                    
                    pdu = answers.get()
                    req_msg = pdu.getMsg()
                    sendString(clientsocket, req_msg)
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
