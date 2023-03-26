from socket import *
import threading
import os
import time

CACHE_DIR = "cache"
CACHE_EXPIRATION = 120

def handle_client(connectionSocket, addr):
    #todo
    try:
        message = connectionSocket.recv(4096).decode()
        htmlRes = message.split(" ")
        htmlRes[1] = "/"+ htmlRes[1].split("/")[3]
        message = " ".join(htmlRes)
        hostDets = message.split()[4].split(":")
        host = hostDets[0]
        port = int(hostDets[1])
        
        cache_key = host + ":" + str(port) + htmlRes[1]
        cache_file = CACHE_DIR + htmlRes[1]
        if os.path.exists(cache_file):
            # check if cached response is still valid
            if time.time() - os.path.getmtime(cache_file) < CACHE_EXPIRATION:
                # cache hit - read response from disk and send to client
                with open(cache_file, "rb") as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        connectionSocket.sendall(data)
                return

        # cache miss - forward request to server and cache response
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((host, port))
        serverSocket.sendall(message.encode())
        with open(cache_file, "wb") as f:
            while True:
                response = serverSocket.recv(4096)
                if not response:
                    break
                f.write(response)
                connectionSocket.sendall(response)
        serverSocket.close()
    except Exception as e:
        print(e)
    finally:
        connectionSocket.close()

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('localhost', 8080))
serverSocket.listen(1)
print("Proxy Server is up")
print('The server is ready to receive...')

# Create cache directory if it doesn't exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

while True:
    # Wait for a connection request
    connectionSocket, addr = serverSocket.accept()
    #print('Connected by', addr)

    # Start a new thread to handle the client request
    t = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    t.start()

# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()
