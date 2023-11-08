import threading
import socket

def broadcast(message) :
    for client in clients:
        client.send(message)

def handle(client) :
    while True :
        try :
            message = client.recv(1024)
            broadcast(message)
        except :
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = users[index]
            broadcast(f"{user} has left the chat.".encode("ascii"))
            users.remove(user)
            break
    
def receive() :
    while True :
        client, address = server.accept()
        print(f"Connected to {str(address)}")
        client.send("Root".encode("ascii"))
        user = client.recv(1024).decode("ascii")
        users.append(user)
        clients.append(client)
        print(f"Name of the client: {user}")
        broadcast(f"{user} joined the chat!".encode("ascii"))
        client.send("Connecting to the server!".encode("ascii"))
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

host = "10.100.109.50"
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
users = []


print("Server is listening...")
receive()