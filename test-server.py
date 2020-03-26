import socket

print("(SERVER) -> Welcome to the Server-Side. Please type your IP address below:")
HOST = input()  # Standard loopback interface address (localhost -> 127.0.0.1)
print("(SERVER) -> Please specify the server port you want to use:")
PORT = input()  # Port to listen on (non-privileged ports are > 1023)
PORT = int(PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Bind the socket;
    s.listen()  # Put the socket listening for connections;
    conn, addr = s.accept()  # Accept incoming connection(s);
    with conn:
        print('Connected by -> ', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                s.close()
                break  # If there is no data received, close current connection and end the script.
            conn.sendall(data)  # All bytes sent back to client, if there are any.
            print("(SERVER) Data received: ", data)
        s.close()   # Close socket in the end.
