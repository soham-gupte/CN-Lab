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

seq_num = 0

while True :
    message = input("Enter your message ('bye' to exit): ")
    csum = rdt_utils.checksum(message)

    # Case - Sender to send the packet
    send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
    rdt_utils.send_message(sender_socket, send_msg, recv_addr)
    if message == 'bye' :
        print("Program exiting...")
        break
    print(f"Message sent: {message}\nChecksum: {csum}")

    while True :
        recv_msg, _ = receiver_socket.recvfrom(1024)
        _, ack, csum_ack = rdt_utils.extract_message_checksum(recv_msg)
        if (not rdt_utils.evaluate_checksum(ack, csum_ack)) :
            print("Corrupted ACK/NAK received! Retransmitting message...")
            time.sleep(1)
            send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
            rdt_utils.send_message(sender_socket, send_msg, recv_addr)  
        elif (ack != '1') :
            print("NAK received! Retransmitting message...")
            time.sleep(1)
            send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
            rdt_utils.send_message(sender_socket, send_msg, recv_addr)
        else :
            print("ACK received!")
            seq_num = 1 - seq_num
            break
        