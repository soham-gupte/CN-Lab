import socket
import rdt_utils

# Creating sending socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_addr = ('localhost', 12345)

while True :
    message = input("Enter your message ('bye' to exit): ")
    csum = rdt_utils.checksum(message)
    # Send the message now
    # send_msg = rdt_utils.encode_message(message, csum)
    send_msg = ("|" + message + "|" + str(csum)).encode()
    rdt_utils.send_message(sender_socket, send_msg, recv_addr)
    if message == 'bye' :
        print("Program exiting...")
        break
    print(f"Message sent: {message}\n")

sender_socket.close()