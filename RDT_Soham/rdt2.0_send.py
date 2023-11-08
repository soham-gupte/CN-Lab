import socket
import rdt_utils
import time

# Creating sending socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_addr = ('localhost', 12344)

# Creating receiving socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_addr = ('localhost', 12345)
receiver_socket.bind(receiver_addr)

while True :
    message = input("Enter your message ('bye' to exit): ")
    csum = rdt_utils.checksum(message)

    # Case - Sender to send the packet
    send_msg = rdt_utils.encode_message(message, csum)
    rdt_utils.send_message(sender_socket, send_msg, recv_addr)

    if message == 'bye' :
        print("Program exiting...")
        break
    print(f"Message sent: {message}\nChecksum: {csum}")

    recv_msg, _ = receiver_socket.recvfrom(1024)

    # Wait for ACK or NAK
    while True :
        _, ack, csum_ack = rdt_utils.extract_message_checksum(recv_msg)
        if (ack != '1') :
            print("NAK received! Retransmitting message...")
            time.sleep(1)
            send_msg = rdt_utils.encode_message(message, csum)
            rdt_utils.send_message(sender_socket, send_msg, recv_addr)
        else :
            print("ACK received!")
            break
        recv_msg, _ = receiver_socket.recvfrom(1024)

    
    