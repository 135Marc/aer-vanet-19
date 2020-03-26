import socket

print("(CLIENT) -> Welcome to the Client Side. Please type your IP address below:")
HOST = input()  # The server's hostname or IP address (127.0.0.1);
print("(CLIENT) -> Please specify the client port you want to use:")
PORT = input()  # The port used by the client to connect to the server;
PORT = int(PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # Connect the client socket to the desired address and port;
    while True:
        inp = input("Mensagem -> ")  # Input written in the terminal;
        s.sendall(inp.encode())     # Send all text written, in bytes , back to server;
        #data = s.recv(1024)  # Data received allows us to "see" what was effectively sent;
        #print("Received (After Sent) : ", data)  # Show the data sent to the server.
