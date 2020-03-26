import socket

servidor = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
servidor.bind(('',1919))

while True:
    mensagem_bytes, endereco_ip_origem = servidor.recvfrom(2048)
    mensagem = mensagem_bytes.decode() 
    print(mensagem)
    servidor.sendto('mensagem recebida'.encode(), endereco_ip_origem)
