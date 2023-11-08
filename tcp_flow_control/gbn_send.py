import socket
import time
import random

def is_lost(p) :
    return random.random() < p

server_host = "127.0.0.1"  # Replace with the server's IP
server_port = 12345  # Use the same port as the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

cwnd = 5    # Constant sending window
iter = 1
expected_ack = 2

num_packets = int(input("Enter number of packets to send: "))

while (iter <= num_packets) :

    isdropped = False
    if (iter + cwnd > num_packets) :
        send_pkts = list(range(iter, num_packets+1))
    else :
        send_pkts = list(range(iter, iter + cwnd))

    print(f"Sending window: {send_pkts}")

    for pkt in send_pkts :

        print(f"Packet {pkt} was sent!")
        time.sleep(1.5)
        if (is_lost(0.25) and not isdropped) :
            # Store dropped packet in separate iterator
            new_iter = pkt
            isdropped = True
            client_socket.send("-1".encode('utf-8'))
            time.sleep(1)
            ack = client_socket.recv(1024).decode('utf-8')
            continue

        message = str(pkt)
        client_socket.send(message.encode('utf-8'))
        time.sleep(1)
        ack = client_socket.recv(1024).decode('utf-8')
        print(f"Received ACK {ack}")
        if (int(ack) == expected_ack) :
            expected_ack += 1
            if (send_pkts[-1]+1 <= num_packets) :
                print(f"Window shifted to add {send_pkts[-1]+1}")
                send_pkts.append(send_pkts[-1]+1)
    
    if (isdropped) :
        print(f"PACKET {new_iter} TIMEOUT!\n")
        iter = new_iter
        continue

    iter = send_pkts[-1] + 1