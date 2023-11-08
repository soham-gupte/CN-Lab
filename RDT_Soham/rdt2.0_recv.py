import socket
import rdt_utils

# Creating receiving socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_addr = ('localhost', 12344)
receiver_socket.bind(receiver_addr)

# Creating sending socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_addr = ('localhost', 12345)

while True :
    recv_msg, _ = receiver_socket.recvfrom(1024)
    _, message, csum = rdt_utils.extract_message_checksum(recv_msg)
    if (message == 'bye') :
        print("Connection closing...")
        break
    print(f"Message received: {message}\nChecksum: {csum}\nActual csum: {rdt_utils.checksum(message)}")

    # Now evaluating the checksum -> 1 - ACK; 0 - NAK
    send_ack = str(rdt_utils.evaluate_checksum(message, csum))
    print(f"Send ack: {send_ack}")
    csum1 = rdt_utils.checksum(send_ack)
    
    # Send ACK or NAK
    send_msg = rdt_utils.encode_ack(send_ack, csum1)
    rdt_utils.send_message(sender_socket, send_msg, recv_addr)

