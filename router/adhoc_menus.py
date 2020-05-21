import queue
import socket
import time
import threading
from adhoc_pdu import PDU

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

def tcpserver(port, table):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(('::1', port))
    s.listen(5)
    print("[LISTENING] Server (tcp) is listening on port: " + str(port))

    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()

        h = threading.Thread(target=handleClient, args=(clientsocket, table, ))
        h.start()
        # print("[ACTIVE CONNECTIONS] " + (threading.activeCount() - 1))


HEADERSIZE = 10

def handleClient(clientsocket, table):
    #Send wellcome message
    sendString(clientsocket, "Welcome to the server!")

    msg = '-'
    connected = True
    while connected:
        if len(msg) != 0:
            msg = receiveString(clientsocket)
            if msg == 'PTR':   
                sendString(clientsocket, table.getStr())
                print(msg)
            elif msg == 'GET':   
                print(msg)
            elif msg == 'PUT':   
                print(msg)
            elif msg == 'DEL':
                print(msg)
            else:
                print(msg)
        else:
            connected = False
            print("[CONNECTION closed] disconnected.")

def receiveString(clientsocket):
    #Receber tamanho do datagrama
    byts, address = clientsocket.recv(HEADERSIZE)
    if byts:
        size = int(byts)
        msg = clientsocket.recv(size)
        return msg.decode("utf-8")
    else:
        return ''

def sendString(clientsocket, msg):
    msg = len(msg) + " "*HEADERSIZE + msg
    clientsocket.send(bytes(msg,"utf-8"))