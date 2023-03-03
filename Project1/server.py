# import socket module
from socket import *

# In order to terminate the program
import sys

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 28000
serverSocket.bind(('192.168.0.104', serverPort))
serverSocket.listen(1)
print("Server is up at http://192.168.0.104:"+str(serverPort)+"/index.html")

while True:
    # Establish the connection
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        print("message", message)

        filename = message.split()[1]

        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket

        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n'.encode())
        connectionSocket.send('Connection: close\r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        # Send the content of the requested file into socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Close client socket
        connectionSocket.close()
        
    except IOError:
        
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n'.encode())
        connectionSocket.send('Connection: close\r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send('<html><body><h1>404 Not Found</h1></body></html>'.encode())

        # Close client socket
        connectionSocket.close()

# Close server socket
serverSocket.close()
# Terminate the program after sending the corresponding data
sys.exit()
