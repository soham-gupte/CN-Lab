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

    if message == 'bye' :
        print("Program exiting...")
        send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
        rdt_utils.send_message(sender_socket, send_msg, recv_addr)
        break

    print("Timer started...\n")
    print(f"Message sent: {message}\nChecksum: {csum}\n")

    while (rdt_utils.bool_drop_packet()) :
    # Start timer
        time.sleep(4)
        print("Timer stopped. Packet was dropped! Resending packet...\n")
        print("Timer started...\n")

    # Case - Sender to send the packet
    send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
    rdt_utils.send_message(sender_socket, send_msg, recv_addr)

    # Receive ACK0 or ACK1
    # What if timeout?
    while True :
        recv_msg, _ = receiver_socket.recvfrom(1024)
        _, ack, csum_ack = rdt_utils.extract_message_checksum(recv_msg)
        # print("Timer stopped!\n")
        if (ack == '2') :
            time.sleep(4)
            print("Timer timed out! Resending packet...\n")
            rdt_utils.send_message(sender_socket, send_msg, recv_addr)
            print("Timer started...\n")
            continue
        elif (not rdt_utils.evaluate_checksum(ack, csum_ack)) :
            print("Corrupted ACK/NAK received! Retransmitting message...")
            print("Timer stopped!\n")
            time.sleep(1)
            send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
            rdt_utils.send_message(sender_socket, send_msg, recv_addr)
            print("Timer started...\n")
            continue
            # break
        if (rdt_utils.evaluate_seq_num(1 - seq_num, ack)) :
            seq_num = 1 - seq_num
            print(f"ACK{ack} received!")
            print("Timer stopped!\n")
            break
        else :
            print(f"ACK{ack} received! Retransmitting message!")
            print("Timer stopped!\n")
            time.sleep(3)
            send_msg = rdt_utils.encode_message(message, csum, str(seq_num))
            rdt_utils.send_message(sender_socket, send_msg, recv_addr)
            print("Timer started...\n")

    # print("Timer stopped!")
    # print(f"Message sent: {message}\nChecksum: {csum}")