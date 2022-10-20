import socket
import threading
import random

# Create a UDP client server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Random port nums for different clients from 13,000 to 13,499 (+1 because last port is excluded)
host = input("Enter your IP Address: ")
server_host = input("Enter the IP Address of the Server: ")
client.bind((host, random.randint(13000, 13500)))

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()


while True:
    message = input("")
    if message == "exit":
        print("EXIT: SUCCESS!")
        client.sendto("ONE HOST HAS EXITED THE PROGRAM!".encode(), (server_host, 9999))
        exit()
    else:
        client.sendto(f"{message}".encode(), (server_host, 9999))
