import socket
import threading

host = input("Enter your IP Address: ")
server_host = input("Enter the IP Address of the Server: ")
client_port = input("Enter the (3) ports you're using for this user (from 13000, 13500) separated by space: ")
client_port = client_port.split(" ")
tracker_port = int(client_port[0])
print(f"Tracker port: {tracker_port}")
receiving_port = int(client_port[1])
print(f"Receiving port: {receiving_port}")
sending_port = int(client_port[2])
print(f"Sending port: {sending_port}")

# Create a UDP client server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((host, tracker_port))

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
