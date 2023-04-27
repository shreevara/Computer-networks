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

# Send ping messages to the server every 3 seconds for 3 minutes
for i in range(1, 61):
    # Generate the ping message in the required format
    sequenceNumber = i
    timestamp = time.time()
    pingMessage = 'ping,' + str(sequenceNumber) + ',' + str(timestamp)
    print(pingMessage)
    # Send the ping message to the server
    clientSocket.sendto(pingMessage.encode(), serverAddress)

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
        else:
            print('Received response message with wrong sequence number.')

    except timeout:
        # Handle the case when no response is received within one second
        print('Client ping timed out.')

    # Wait for 3 seconds before sending the next ping message
    time.sleep(3)
 
# Close the socket
clientSocket.close()
