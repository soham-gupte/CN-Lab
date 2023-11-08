import socket
import time

server_host = "127.0.0.1"  # Replace with the server's IP
server_port = 12345  # Use the same port as the server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)

pkt_num = 1
buffer = []

while True:

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    while True:
        temp = pkt_num
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        if (pkt_num == int(data)) :
            print(f"Received from client: {data}")
            pkt_num += 1
            temp = pkt_num
            print(f"pkt_num : {temp}")
            while (len(buffer)) :
                x = buffer.pop(0)
                print(f"Received buffered packet {x}!")
                time.sleep(0.5)
                pkt_num = x + 1
            temp = pkt_num
        elif (data == "-1") :
            print("Packet must have been dropped!")
        else :
            print(f"Out of order packet {data} arrived, sending ACK and buffering packet...")
            pkt_num = int(data) + 1
            buffer.append(int(data))

        print(f"Sent ACK {pkt_num}\n")
        client_socket.send(str(pkt_num).encode('utf-8'))
        pkt_num = temp

    client_socket.close()