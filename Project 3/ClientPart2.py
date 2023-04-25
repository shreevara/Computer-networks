import time
import random
from socket import *

serverAddress = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(1)

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
