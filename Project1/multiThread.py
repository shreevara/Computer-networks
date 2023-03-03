# import socket module and threading module
from socket import *
import threading

# In order to terminate the program
import sys

def handle_client(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        
        # Open the file and read its contents in binary mode
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()
        
        # Send HTTP headers and content to client
        connectionSocket.sendall(b"HTTP/1.1 200 OK\r\n")
        connectionSocket.sendall(b"Content-Type: application/pdf\r\n")
        connectionSocket.sendall(b"\r\n")
        connectionSocket.sendall(outputdata)
    except IOError:
        # Send response message for file not found
        connectionSocket.sendall(b"HTTP/1.1 404 Not Found\r\n")
        connectionSocket.sendall(b"\r\n")
        connectionSocket.sendall(b"<html><head></head><body><h1>404 Not Found</h1></body></html>")
    finally:
        # Close client socket
        connectionSocket.close()

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('192.168.0.104', 28000))
serverSocket.listen(1)
print("Server is up at http://192.168.0.104:28000/Project1-WebServer.pdf")
print('The server is ready to receive...')

while True:
    # Wait for a connection request
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr)

    # Start a new thread to handle the client request
    t = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    t.start()

# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()
