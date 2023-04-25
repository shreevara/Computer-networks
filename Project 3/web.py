# import socket module and threading module
from socket import *
import threading
import os
import time
import random

# In order to terminate the program
import sys
serverSocketPing = socket(AF_INET, SOCK_DGRAM)
serverSocketPing.bind(('192.168.0.105', 12000))
print("Ready to receive pings from client")

def pingServer():
    

    while True:
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)

        # Receive the client packet along with the address it is coming from
        message, address = serverSocketPing.recvfrom(1024)

        # If rand is less is than 4, we consider the packet lost and do not respond
        if rand < 4:
            continue

        # Otherwise, prepare the server response

        # The server responds
        serverSocketPing.sendto(message, address)


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

pingThread = threading.Thread(target=pingServer)
pingThread.start()

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('192.168.0.105', 28000))
serverSocket.listen(1)
print("Server is up at http://192.168.0.105:28000")
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
