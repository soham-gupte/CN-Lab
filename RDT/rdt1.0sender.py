import socket

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = ('localhost', 12345)

while True:
    message = input("Enter a message ('exit' to quit): ")
    if message.lower() == 'exit':
        break

    sender_socket.sendto(message.encode(), receiver_address)
    print(f"Sent message: {message}")

sender_socket.close()

