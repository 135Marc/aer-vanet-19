import socket

client = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

while True:
    mensagem_envio = input("Mensagem para o servidor:")
    client.sendto(mensagem_envio.encode(), ("127.0.0.1",  1919))
    mensagem_bytes, adress = client.recvfrom(2048)
    print(mensagem_bytes.decode())