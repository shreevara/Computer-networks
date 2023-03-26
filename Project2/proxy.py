from socket import *
import threading
import time

def handle_client(connectionSocket, addr):
    try:
        message = connectionSocket.recv(4096).decode()
        htmlRes = message.split(" ")
        htmlRes[1] = "/"+ htmlRes[1].split("/")[3]
        message = " ".join(htmlRes)
        hostDets = message.split()[4].split(":")
        host = hostDets[0]
        port = int(hostDets[1])
        
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((host, port))
        serverSocket.sendall(message.encode())
        while True:
            response = serverSocket.recv(4096)
            if not response:
                break
            connectionSocket.sendall(response)
        print(f"proxy-forward,client,{threading.get_ident()},{time.time()}")
        serverSocket.close()
        
    except:
        #print(e)
        pass
    finally:
        connectionSocket.close()

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('localhost', 8080))
serverSocket.listen(1)
print("Proxy Server is up")
print('The server is ready to receive...')


while True:
    # Wait for a connection request
    connectionSocket, addr = serverSocket.accept()
    #print('Connected by', addr)
    print(f"proxy-forward,server,{threading.get_ident()},{time.time()}")

    # Start a new thread to handle the client request
    t = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    t.start()
# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()