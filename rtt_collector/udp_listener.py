import socket
import time
import random
# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to localhost and port 161
server_address = ('localhost', 161)
server_socket.bind(server_address)

# Receive and process incoming packets
while True:
    print('Waiting for incoming packets...')
    data, address = server_socket.recvfrom(1024)  # Adjust buffer size as per your requirements

    # Process the received packet
    print('Received packet from:', address)
    print('Data:', data.decode())
    
    time.sleep(random.uniform(0.3, 1))
    # Generate the response string
    response = 'Hello, client!'

    # Send the response back to the client
    server_socket.sendto(response.encode(), address)

# Close the socket
# server_socket.close()
