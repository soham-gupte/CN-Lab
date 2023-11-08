import socket

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(("localhost", 2000)) 
    receiver_socket.listen(1)

    print("Receiver is ready to receive messages...")

    conn, addr = receiver_socket.accept()

    expected_seq_num = 0  
    ack = "ACK"
    nak = "NAK"

    while True:
        packet = conn.recv(1024).decode()
        seq_num, message, received_checksum = packet.split('|')
        seq_num = int(seq_num)
        received_checksum = int(received_checksum)

        checksum = calculate_checksum(message.encode())

        if seq_num == expected_seq_num and checksum == received_checksum:

            conn.send('ACK'.encode())
            print(f"Received and delivered: {message}\nSending ACK")
            expected_seq_num = 1 - expected_seq_num  
        else:
            conn.send("NAK".encode())
            print("Message corrupted or out of sequence. Requesting sender to resend...")

        if message.lower() == 'exit':
            break

    receiver_socket.close()

if __name__ == "__main__":
    main()

