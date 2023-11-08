import socket
import random

def corrupt_message(message):
    if random.random() < 0.15:  # 15% probability of corruption
        message = 'new123abc'.encode() + message
    return message

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(("localhost", 2000))  

    seq_num = 0 

    while True:
        message = input("Enter a message to send: ")
        checksum = calculate_checksum(message.encode())

        message_corrupted = corrupt_message(message.encode())
        packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
        sender_socket.send(packet)

        ack = sender_socket.recv(1024).decode()

        while True:
            if ack == "ACK":
                print(f"Message {seq_num} sent successfully.")
                seq_num = 1 - seq_num  
                break
            elif ack == "NAK":
                print(f"Message {seq_num} corrupted. Resending...")
            else:
                print("Unknown acknowledgment. Resending...")
            
            message_corrupted = corrupt_message(message.encode())

            packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
            sender_socket.send(packet)
            ack = sender_socket.recv(1024).decode()

        if message.lower() == 'exit':
            print("Ending program...\n")
            break

    sender_socket.close()

if __name__ == "__main__":
    main()

