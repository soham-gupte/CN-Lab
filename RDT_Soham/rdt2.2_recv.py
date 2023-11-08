import socket
import rdt_utils

# Creating receiving socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_addr = ('localhost', 12344)
receiver_socket.bind(receiver_addr)

# Creating sending socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_addr = ('localhost', 12345)
expected_seq_num = 0

while True :
    recv_msg, _ = receiver_socket.recvfrom(1024)
    seq_num, message, csum = rdt_utils.extract_message_checksum(recv_msg)
    if (message == 'bye') :
        print("Connection closing...")
        break
    # print(f"Message received: {message}\nChecksum: {csum}\nActual csum: {rdt_utils.checksum(message)}")

    # Check pakcet sequence number:
    if (rdt_utils.evaluate_seq_num(seq_num, str(expected_seq_num)) and rdt_utils.evaluate_checksum(message, csum)) :
        print(f"Message received: {message}\nChecksum: {csum}\nActual csum: {rdt_utils.checksum(message)}")
        expected_seq_num = 1 - expected_seq_num
        # Packet received, send ACK for that packet
        # send_ack = '1'
    elif (rdt_utils.evaluate_seq_num(seq_num, str(expected_seq_num)) and not rdt_utils.evaluate_checksum(message, csum)) :
        print("Corrupted message! Resend packet!")
        # send_ack = '0'
    else :
        print("Duplicate packet arrived - Send next packet!")
        # expected_seq_num = 1 - expected_seq_num
        # send_ack = '1'

    send_ack = str(expected_seq_num)

    # send_ack = str(rdt_utils.evaluate_checksum(message, csum))
    # print(f"Send ack: {send_ack}")
    csum1 = rdt_utils.checksum(send_ack)

    send_msg = rdt_utils.encode_ack(send_ack, csum1, str(expected_seq_num))
    rdt_utils.send_message(sender_socket, send_msg, recv_addr)