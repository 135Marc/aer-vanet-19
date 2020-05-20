import socket
import sys

HEADERSIZE = 10

def receiveString(s):
    #Receber tamanho do datagrama
    byts = s.recv(HEADERSIZE)
    if byts:
        size = int(byts)
        msg = s.recv(size)
        return msg.decode("utf-8")
    else:
        return ''

def sendString(clientsocket, msg):
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    clientsocket.send(bytes(msg,"utf-8"))
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 9999))

msg = receiveString(s)
print(msg)

print(f'''
---------------------------------
Command: method/[name/][subname/]
Methods: GET PUT DEL
---------------------------------'''
)

while True:
    opt = input()
    cmd = opt.split('/')
    if cmd and len(cmd[0]) == 3:
        method = cmd[0]
        function = cmd[1:]

        if method == 'get' or method == 'GET' or method == 'Get':
            sendString(s, method.upper())
        elif method == 'put' or method == 'PUT' or method == 'Put':
            sendString(s, method.upper())
        elif method == 'del' or method == 'DEL' or method == 'Del':
            sendString(s, method.upper())
        else:
            print(f'''
---------------------------------
Method not found: {method}
Methods: GET PUT DEL
---------------------------------
            ''')
    elif opt == 'p':
        sendString(s, 'PTR')
        print(receiveString(s))
    elif opt == 'h' or opt == 'H':
        print(f'''
---------------------------------
Command: method/[name/][subname/]
Methods: GET PUT DEL
Name: information name 
---------------------------------
            ''')
    elif opt == 'q' or opt == 'Q':
        s.close()
        sys.exit()
    else:
        print(f'''
---------------------------------
Bad command: {opt}
Command: method/[name/][subname/]
---------------------------------
        ''')

