# import socket module and threading module
from socket import *
import threading
import os
import time

# In order to terminate the program
import sys

def clientThread(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]

        # Get the file extension
        file_extension = os.path.splitext(filename)[1]

        # Open the file and read its contents in binary mode
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()

        # Set content type header based on file extension
        if file_extension == ".pdf":
            content_type = b"Content-Type: application/pdf\r\n"
        elif file_extension == ".html":
            content_type = b"Content-Type: text/html\r\n"
        else:
            content_type = b"Content-Type: application/octet-stream\r\n"

        # Send HTTP headers and content to client
        connectionSocket.sendall(b"HTTP/1.1 200 OK\r\n")
        connectionSocket.sendall(content_type)
        connectionSocket.sendall(b"\r\n")
        connectionSocket.sendall(outputdata)

        # Print server response information
        print(f"server-response,200,{threading.current_thread().name},{time.time()}")

    except IOError:
        # Send response message for file not found
        connectionSocket.sendall(b"HTTP/1.1 404 Not Found\r\n")
        connectionSocket.sendall(b"\r\n")

        # Print server response information
        print(f"server-response,404,{threading.current_thread().name},{time.time()}")

    finally:
        # Close client socket
        connectionSocket.close()

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('192.168.0.102', 28000))
serverSocket.listen(1)
print("Server is up at http://192.168.0.102:28000")
print('The server is ready to receive...')

while True:
    # Wait for a connection request
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr)

    # Start a new thread to handle the client request
    t = threading.Thread(target=clientThread, args=(connectionSocket, addr))
    t.start()

# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()
