import random
import socket

def checksum(message) :
    return sum(message.encode())

def extract_message_checksum(recv_msg) :
    recv_msg = recv_msg.decode()
    temp = recv_msg
    temp = temp.split("|")
    return temp[0], temp[1], temp[2]

def encode_message(message, csum, seq_num = '') :
    # If message is to exit:
    if (message == 'bye') :
        return (seq_num + "|" + message + "|" + str(csum)).encode()
    
    # Add probable corruption
    p = 0.3     # Probability of message getting corrupted
    if random.random() < p :
        # Make the message corrupt
        temp = list(message)
        rand_ind = random.randint(0,len(temp)-1)
        temp.insert(rand_ind, chr(random.randint(0, 255)))
        # temp[rand_ind] = chr(random.randint(0, 255))
        message = "".join(temp)
    send_msg = seq_num + '|' + message + "|" + str(csum)
    send_msg = send_msg.encode()
    return send_msg

def send_message(sender_socket, send_msg, receiver_address) :
    sender_socket.sendto(send_msg, receiver_address)

def evaluate_checksum(message, csum) :
    if int(checksum(message)) == int(csum) :
        return 1
    return 0

def encode_ack(message, csum, seq_num = '') :
    # If message is to exit:
    if (message == 'bye') :
        return (seq_num + "|" + message + "|" + str(csum)).encode()
    
    # Add probable corruption
    p = 0.1     # Probability of message getting corrupted
    if random.random() < p :
        # Make the message corrupt
        temp = list(message)
        rand_ind = random.randint(0,len(temp)-1)
        temp.insert(rand_ind, chr(random.randint(0, 255)))
        # temp[rand_ind] = chr(random.randint(0, 255))
        message = "".join(temp)
    send_msg = seq_num + '|' + message + "|" + str(csum)
    send_msg = send_msg.encode()
    return send_msg

# For RDT 2.1

# def encode_message_with_seq(message, csum, ) :
def evaluate_seq_num(seq_num, expected_seq_num: str) :
    return str(seq_num) == expected_seq_num

def bool_drop_packet() :
    return random.random() <= 0.1


