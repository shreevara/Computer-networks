import time
import random
from socket import *

serverAddress = ('localhost', 12000)

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(1, 61):
    sequenceNumber = i
    timestamp = time.time()
    pingMessage = 'ping,' + str(sequenceNumber) + ',' + str(timestamp)
    
    clientSocket.sendto(pingMessage.encode(), serverAddress)

    try:
        responseMessage, serverAddress = clientSocket.recvfrom(1024)
        timestamp = time.time()
        responseParts = responseMessage.decode().split(',')
        responseSequenceNumber = int(responseParts[1])
        responseTimestamp = float(responseParts[2])

        if sequenceNumber == responseSequenceNumber:
            RTT = timestamp - responseTimestamp
            print('Response from server:', responseMessage.decode(), 'RTT:', RTT)
        else:
            print('Received response message with wrong sequence number.')

    except timeout:
        print('Client ping timed out.')

    time.sleep(3)

clientSocket.close()
