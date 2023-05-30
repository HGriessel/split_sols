import socket
import time
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('0.0.0.0', 161)
server_socket.bind(server_address)

while True:
    print('Waiting for incoming packets...')
    data, address = server_socket.recvfrom(1024)  # Adjust buffer size as per your requirements

    print('Received packet from:', address)
    print('Data:', data.decode())
    
    time.sleep(random.uniform(0.5, 1))
    response = 'Hello, client!'

    server_socket.sendto(response.encode(), address)

