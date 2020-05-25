import queue
import socket
import time
import threading
from adhoc_pdu import PDU

def tcpserver(name, port, table, msgqueue):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind((s.getsockname()[0], port))
    s.listen(5)
    print("[LISTENING] Server (tcp) is listening on port: " + str(port))

    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()

        h = threading.Thread(target=handleClient, args=(name, clientsocket, table, msgqueue, ))
        h.start()
        print("[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 1))


HEADERSIZE = 10

def handleClient(name, clientsocket, table, msgqueue):
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
        print(method)
        if len(method) != 0:
            if method == 'PTR':  
                req_msg = table.getStr()
                sendString(clientsocket, table.getStr())
            elif method == 'GET':
                newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'B', method + '/' + info, [name])
                msgqueue.put(newpdu)

                time.sleep(1) ## mudar isto
                pdu = msgqueue.get()
                req_msg = pdu.getMsg()
                if req_msg != '400 File not found.':
                    sendString(clientsocket, req_msg)
                else:
                    sendString(clientsocket, '400 File not found.')
            elif msg == 'PUT': 
                newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'B', method + '/' + info, [name])
                msgqueue.put(newpdu)
                continue
            elif msg == 'DEL':
                continue
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


def menus(source, msgqueue, table):
    while True:
        print('Nodo: ' + source)
        # print('---------Opções:-----------')
        # print('Encontrar nodo: f')
        # print('Imprimir tabela: p')
        # print('---------------------------')

        opt = input()
        # Imprimir tabela
        if opt == 'p':
            table.printTable()
        
        # Encontrar novo nodo
        elif opt == 'f':
            print('Nome do nodo:')
            nodo = input()
            newpdu = PDU(source, 'ROUTE_REQUEST', 5, None, nodo, '', [source])
            msgqueue.put(newpdu)
        
        # Operação padrão
        else:
            print('Opção inválida.')