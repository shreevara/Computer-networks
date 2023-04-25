from socket import *
import threading
import time
import random

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

        clientSocket.sendto(pingMessage.encode(), serverAddress)
        numPacketsSent += 1

        try:
            responseMessage, serverAddress = clientSocket.recvfrom(1024)
            timestamp = time.time()
            responseParts = responseMessage.decode().split(',')
            responseSequenceNumber = int(responseParts[1])
            responseTimestamp = float(responseParts[2])

            if sequenceNumber == responseSequenceNumber:
                RTT = timestamp - responseTimestamp
                print('Response from server:', responseMessage.decode(), 'RTT:', RTT)
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
        
    except Exception as e:
        print(e)
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
    print('Connected by', addr)
    print(f"proxy-forward,server,{threading.get_ident()},{time.time()}")

    # Start a new thread to handle the client request
    t = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    t.start()
# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()