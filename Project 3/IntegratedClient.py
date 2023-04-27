from socket import *
import threading
import os
import time

CACHE_DIR = "cache"
CACHE_EXPIRATION = 120

def pingClient(serverName, serverPort):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    serverAddress = (serverName, serverPort)
    minRTT = float('inf')
    maxRTT = 0
    totalRTT = 0
    numRTT = 0
    numPacketsSent = 0
    numPacketsLost = 0
    for i in range(1, 61):
        sequenceNumber = i
        timestamp = time.time()
        pingMessage = 'ping,' + str(sequenceNumber) + ',' + str(timestamp)
        print(pingMessage)
        clientSocket.sendto(pingMessage.encode(), serverAddress)
        numPacketsSent += 1

        try:
            responseMessage, serverAddress = clientSocket.recvfrom(1024)
            timestamp = time.time()
            responseParts = responseMessage.decode().split(',')
            responseSequenceNumber = int(responseParts[1])
            responseTimestamp = float(responseParts[2])
            responseM = "echo,"+str(responseSequenceNumber)+","+str(timestamp)

            if sequenceNumber == responseSequenceNumber:
                RTT = timestamp - responseTimestamp
                print(responseM, 'RTT:', RTT)
                minRTT = min(minRTT, RTT)
                maxRTT = max(maxRTT, RTT)
                totalRTT += RTT
                numRTT += 1
            else:
                print('Received response message with wrong sequence number.')

        except timeout:
            print('Client ping timed out.')
            numPacketsLost += 1
        time.sleep(3)

    print('Minimum RTT:', minRTT)
    print('Maximum RTT:', maxRTT)
    print('Total number of RTTs:', numRTT)
    print('Packet loss rate:', numPacketsLost / numPacketsSent * 100, '%')
    print('Average RTT:', totalRTT / numRTT if numRTT > 0 else 0)

    clientSocket.close()

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
        t = threading.Thread(target=pingClient, args=(host, 12000))
        t.start() 
        
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
                    print(f"proxy-cache,client,{threading.get_ident()},{time.time()}")
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
            print(f"proxy-forward,client,{threading.get_ident()},{time.time()}")
        serverSocket.close()
    except:
        pass
    finally:
        connectionSocket.close()

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('192.168.0.106', 8080))
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
