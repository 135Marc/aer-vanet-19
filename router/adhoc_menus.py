import queue
import socket
import time
import threading
from adhoc_pdu import PDU

def tcpserver(name, port, table, msgqueue, answers):
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
        print(method)
        if method.upper() != 'QIT':
            if method == 'PTR':  
                req_msg = table.getStr()
                sendString(clientsocket, table.getStr())
            elif method == 'GET':
                newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'C', method + '/' + info, [name])
                msgqueue.put(newpdu)

                pdu = answers.get()
                req_msg = pdu.getMsg()
                sendString(clientsocket, req_msg)
            elif method == 'PUT': 
                newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'C', method + '/' + info + '/' + value, [name])
                msgqueue.put(newpdu)

                pdu = answers.get()
                req_msg = pdu.getMsg()
                sendString(clientsocket, req_msg)
            elif method == 'LST': 
                newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'C', method + '/' + info, [name])
                msgqueue.put(newpdu)

                pdu = answers.get()
                req_msg = pdu.getMsg()
                sendString(clientsocket, req_msg)
            elif method == 'DEL':
                newpdu = PDU(name, 'METHOD_REQUEST', 5, None, 'C', method + '/' + info, [name])
                msgqueue.put(newpdu)

                pdu = answers.get()
                req_msg = pdu.getMsg()
                sendString(clientsocket, req_msg)
            else:
                print('[METHOD not found]')
        else:
            connected = False
            print("[CONNECTION closed] disconnected.")


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