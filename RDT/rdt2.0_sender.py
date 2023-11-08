import socket
import random

def corrupt_message(message):
    if random.random() < 0.15:  
        message = 'new123'.encode() + message
    
    return message

def calculate_checksum(data):
    checksum = 0

    for byte in data:
        checksum ^= byte
        print(checksum, byte)

    return checksum

def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(("localhost", 2000))  # Replace with actual receiver IP and port

#    i = 0
    while True:
        message = input("Enter a message('exit' to quit): ")

        checksum = calculate_checksum(message.encode())

        message_corrupted = corrupt_message(message.encode())

        packet = message_corrupted + b"|" + str(checksum).encode()
        sender_socket.send(packet)

        ack = sender_socket.recv(1024).decode()

        while (ack != "ACK"):
            print("Message corrupted. Resending packet...")

            message_corrupted = corrupt_message(message.encode())

            packet = message_corrupted + b"|" + str(checksum).encode()

            sender_socket.send(packet)
            ack = sender_socket.recv(1024).decode()

        if ack == "ACK":
            print("Message sent successfully.")

        if(message.lower() == 'exit'):
            print("PROGRAM ENDING...\n")
            break

    sender_socket.close()

if __name__ == "__main__":
    main()

