import socket
import rdt_utils

# Creating receiving socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_addr = ('localhost', 12345)
receiver_socket.bind(receiver_addr)

while True :
    recv_msg, _ = receiver_socket.recvfrom(1024)
    _, message, csum = rdt_utils.extract_message_checksum(recv_msg)
    if (message == 'bye') :
        print("Connection closing...")
        break
    print(f"Message received: {message}\n")

receiver_socket.close()