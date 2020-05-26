
import socket

def get():
    #Pedido ao servidor tcp
    sok = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    IPv6 = sok.getsockname()[0]
    sok.connect((IPv6, 9988))

    sendString(sok, method + '/' + info + '/' + value)
    rec_msg = receiveString(sok)
    print(rec_msg)

    sok.close()
    return rec_msg