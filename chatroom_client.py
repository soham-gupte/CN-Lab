import threading
import socket

user = input("Enter your display username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.100.109.50", 12345))

def receive() :
    while True :
        try :
            message = client.recv(1024).decode("ascii")
            if (message == "Root") :
                client.send(user.encode("ascii"))
            else :
                print(message)
        except :
            print("Aborting, error occurred!")
            client.close()
            break

def write() :
    while True :
        message = f"{user} : {input('')}"
        client.send(message.encode("ascii"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()