import socket
import sys

HEADERSIZE = 10
IPv6 = '::1'
PORT = 9919
        
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
    
def representsInt(s):
    try: 
        n = int(s)
        if n >= 0:
            return True
        else:
            return False
    except ValueError:
        return False

print('---------------------------------')
print('Command: method [name/] [value/] servidor')
print('Methods: GET PUT DEL LST')
print('Tools: p - print')
print('       q - quit')
print('       h - help')
print('---------------------------------')

while True:
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    IPv6 = s.getsockname()[0]
    s.connect((IPv6, PORT))
    opt = input()

    fields = opt.split(' ')
    size = len(fields)
    if fields and len(fields[0]) == 3:
        method = fields[0]
        if method.upper() == 'GET' or method.upper() == 'PUT' or method.upper() == 'DEL' or method.upper() == 'LST':
            sendString(s, opt)
            rec_msg = receiveString(s)
            print(rec_msg)
        else:
            print('---------------------------------')
            print('Method not found: {}'.format(method))
            print('Methods: GET PUT DEL')
            print('---------------------------------')

    elif opt == 'p':
        sendString(s, 'PTR')
        rec_msg = receiveString(s)
        print(rec_msg)
    elif opt == 'q' or opt == 'Q':
        sys.exit()
    elif opt == 'h' or opt == 'H':
        print('---------------------------------')
        print('Command: method [name/] [value/] server')
        print('Methods: GET PUT DEL LST')
        print('Tools: p - print')
        print('       q - quit')
        print('       h - help')
        print('Name: information name')
        print('---------------------------------')
    else:
        print('---------------------------------')
        print('Bad format: {}'.format(opt))
        print('Command: method [name/] [subname/] server')
        print('---------------------------------')
    s.close()

