#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import time
import random

def validate_checksum(message):
    
    parts = message.split(':')
    received_checksum, received_message = int(parts[0]), parts[1]
    calculated_checksum = 0
    for char in received_message:
        calculated_checksum ^= ord(char)
    
    if calculated_checksum == received_checksum:
        return True
    else:
        print(f"Received corrupted message: {received_message}")
        return False

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_address = ('localhost', 9799)
    receiver_socket.bind(receiver_address)

    while True:
        data, sender_address = receiver_socket.recvfrom(1024)
        data = data.decode()
        if data.lower() == 'exit':
            break
        sleep_duration = random.random() * 4

# Sleep for the specified duration
        time.sleep(sleep_duration)


        if sleep_duration >= 2 :
            continue
        
        
        
        
        if validate_checksum(data):
            print(f"Received message: {data.split(':')[1]}")
            print(f"Received message from : {data.split(':')[2]}")
            q=data.split(':')[2]
            receiver_socket.sendto(q.encode(), sender_address)
        else:
            q=data.split(':')[2]
            print("Received corrupted message. Sending NAK.")
            if(q=='0'):
                q='1'
            else:
                q='0'
                
            receiver_socket.sendto(q.encode(), sender_address)

    receiver_socket.close()

if __name__ == "__main__":
    main()


# In[ ]:




