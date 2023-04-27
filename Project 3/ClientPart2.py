# Import required modules
import time
import random
from socket import *

# Set the server address and port number
serverAddress = ('localhost', 12000)

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set timeout value for the socket
clientSocket.settimeout(1)

# Initialize variables to calculate statistics
minRTT = float('inf')
maxRTT = 0
totalRTT = 0
numRTT = 0
numPacketsSent = 0
numPacketsLost = 0

# Send ping messages to the server every 3 seconds for 3 minutes
for i in range(1, 61):
    # Generate the ping message in the required format
    sequenceNumber = i
    timestamp = time.time()
    pingMessage = 'ping,' + str(sequenceNumber) + ',' + str(timestamp)

    # Send the ping message to the server
    print(pingMessage)
    clientSocket.sendto(pingMessage.encode(), serverAddress)
    numPacketsSent += 1

    try:
        # Receive the server response message
        responseMessage, serverAddress = clientSocket.recvfrom(1024)
        timestamp = time.time()

        # Parse the response message to extract sequence number and timestamp
        responseParts = responseMessage.decode().split(',')
        responseSequenceNumber = int(responseParts[1])
        responseTimestamp = float(responseParts[2])
        responseM = "echo,"+str(responseSequenceNumber)+","+str(timestamp)
        # Calculate the RTT and update statistics
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
        # Handle the case when no response is received within one second
        print('Client ping timed out.')
        numPacketsLost += 1

    # Wait for 3 seconds before sending the next ping message
    time.sleep(3)

# Print the statistics after all pings are sent
print('Minimum RTT:', minRTT)
print('Maximum RTT:', maxRTT)
print('Total number of RTTs:', numRTT)
print('Packet loss rate:', numPacketsLost / numPacketsSent * 100, '%')
print('Average RTT:', totalRTT / numRTT if numRTT > 0 else 0)
 
# Close the socket
clientSocket.close()
