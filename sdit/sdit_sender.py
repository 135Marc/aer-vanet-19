import socket
import sys

HEADERSIZE = 10
IPv6 = '::1'
s = len(sys.argv)
    if s > 1:
        IPv6 = sys.argv[1]
        

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
print('Command: method/[name/][subname/]')
print('Methods: GET PUT DEL')
print('---------------------------------')

while True:
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((IPv6, 9996))
    opt = input()
    cmd = opt.split('/')
    if cmd and len(cmd[0]) == 3:
        method = cmd[0]
        function = cmd[1:]

        if method == 'get' or method == 'GET' or method == 'Get':
            sendString(s, method.upper())
            rec_msg = receiveString(s)
            print('msg get: ' + rec_msg)
        elif method == 'put' or method == 'PUT' or method == 'Put':
            sendString(s, method.upper())
        elif method == 'del' or method == 'DEL' or method == 'Del':
            sendString(s, method.upper())
        else:
            print('---------------------------------')
            print('Method not found: {method}')
            print('Methods: GET PUT DEL')
            print('---------------------------------')
    elif opt == 'p':
        sendString(s, 'PTR')
        rec_msg = receiveString(s)
        print('msg p: ' + rec_msg)
    elif opt == 'h' or opt == 'H':
        print('---------------------------------')
        print('Command: method/[name/][subname/]')
        print('Methods: GET PUT DEL')
        print('Name: information name')
        print('---------------------------------')
    elif opt == 'q' or opt == 'Q':
        sys.exit()
    else:
        print('---------------------------------')
        print('Bad command: {opt}')
        print('Command: method/[name/][subname/]')
        print('---------------------------------')
    s.close()

