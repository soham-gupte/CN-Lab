import socket

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = ('localhost', 12345)
receiver_socket.bind(receiver_address)

while True:
    data, sender_address = receiver_socket.recvfrom(1024)
    message = data.decode()
    print(f"Received message: {message}")

    if message.lower() == 'exit':
        print("Exiting receiver.")
        break

receiver_socket.close()
