import socket
import threading
import queue

notes = ''' 
    1) Remember that all messages are in str, so you might have to convert stuff like port nums to int
    2) Check for duplicate @handle when registering; 
        return SUCCESS if we can register & no duplicated @handle
        return FAIL if we can't register because there's a duplicate @handle
    3) Data from "register" command is used to create the user table
    4) Data from "follow" command is used to create the follower table
     '''

messages = queue.Queue()
clients = []

# Create a UDP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_host = input("Enter the IP Address of the server: ")

# bind to IP/ hostname:"localhost" port:9999 (tuple)
# hostname will be likely "general.asu.edu" (change it later)
server.bind((server_host, 9999))

# User table
user_table = []
# Follower table
follower_table = {}

# This function will run in a thread
# This function is constantly accepting (receiving) the messages and storing them into messages queue data structure
def receive():
    user_handle = []
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
            token = message.decode().lower().split(" ")
            if token[0] == "register":
                user_info = []
                for i in range(1, len(token)):
                    user_info.append(token[i])

                current_handle = user_info[0]
                # Check if character's length > 15 and the format is correct (3 ports)
                if len(current_handle) <= 15 and (user_info[2].isdigit() and user_info[3].isdigit() and (user_info[4].isdigit() and len(user_info) == 5)):
                    # TODO: CHECK FOR DUPLICATES, DON'T JUST INSERT @HANDLE DIRECTLY (DONE)
                    if current_handle not in user_handle:
                        user_handle.append(current_handle)
                        add_user(current_handle)
                        # TODO: PUT THE @HANDLE IN SORTED ALPHABETICAL-ORDER (DONE)
                        # DESIGN CONSIDERATION: We tried using dict, but it's difficult to sort the keys in dict
                        # Append user_info list to user_table
                        user_table.append(user_info)
                        # Sort the lists inside the user_table list by their Alphabetical-orders
                        user_table.sort()
                        # Return SUCCESS if registration is success (no dupe)
                        server.sendto(f"{current_handle} has been registered SUCCESSFULLY!".encode(), addr)
                        print("\n---USER INFORMATION---")
                        print(f"User Details: {user_info}")
                        print(f"Current Handle: {current_handle}")
                        print(f"USERS Table: \n{user_table}")
                        print(f"--- END OF LINE --- \n")
                    else:
                        #DUPLICATE
                        server.sendto(f"FAILURE!! Can't add {current_handle} -- User already exists!".encode(), addr)
                else:
                    if len(current_handle) > 15:
                        server.sendto("FAILURE: @handle must be at most 15 characters!".encode(), addr)
                    # Check if we're not entering 3 ports
                    if not (user_info[2].isdigit() and user_info[3].isdigit() and user_info[4].isdigit() and len(
                            user_info) == 5):
                        server.sendto(
                            "FAILURE: You must enter exactly 3 ports in the order: \"register @<handle> IP P1 P2 P3\"".encode(),
                            addr)
                        server.sendto("Be careful not to enter additional blank character (\" \") after the command, it's counting for the number of words!".encode(), addr)
                    else:
                        server.sendto(
                            "FAILURE: You must enter exactly 3 ports in the order: \"register @<handle> IP P1 P2 P3\"".encode(),
                            addr)
                        server.sendto(
                            "Be careful not to enter additional black character (\" \") after the command, it's counting for the number of words!".encode(),
                            addr)

            elif token[0] == "query" and token[1] == "handles":
                no_of_handles = f"There are {len(user_table)} registered handles!"
                handles = []
                for user in user_table:
                    handle = user[0]
                    handles.append(handle)
                server.sendto(no_of_handles.encode(), addr)
                server.sendto(str(handles).encode(), addr)

            elif token[0] == "follow":
                user_name = token[1]
                user_toFollow = token[2]
                userToFollow(user_name, user_toFollow, addr)

            elif token[0] == "drop":
                user_name = token[1]
                user_toUnfollow = token[2]
                userToUnfollow(user_name, user_toUnfollow, addr)

        except:
            print("\nerror")


def userToFollow(user_name, user_to_follow, addr):
    if user_name == user_to_follow:
        server.sendto('FAILURE'.encode(), addr)
        print(f"\n{user_name} tried to follow him/herself!")
    elif user_name in follower_table.keys():
        if user_to_follow in follower_table.keys():
            follower_table[user_to_follow].append(user_name)
            server.sendto("SUCCESS".encode(), addr)
        else:
            server.sendto("FAILURE".encode(), addr)
    else:
        server.sendto("FAILURE".encode(), addr)

    # Sort the follower list
    for follower in follower_table.values():
        follower.sort()

    print(f"\n---FOLLOWER TABLE---")
    print(follower_table)
    print('---END OF LINE---\n')


def userToUnfollow(user_name, user_to_unfollow, addr):
    # if user_name not in follower_table[user_to_unfollow]:
    #     server.sendto('FAILURE'.encode(), addr)

    if user_name == user_to_unfollow:
        server.sendto('FAILURE'.encode(), addr)
        print(f"\n{user_name} tried to follow him/herself!")
    elif user_name in follower_table.keys():
        if user_to_unfollow in follower_table.keys():
            follower_table[user_to_unfollow].remove(user_name)
            server.sendto("SUCCESS".encode(), addr)
        else:
            server.sendto("FAILURE".encode(), addr)

    else:
        server.sendto("FAILURE".encode(), addr)

    print(f"\n---FOLLOWER TABLE---")
    print(follower_table)
    print('---END OF LINE---\n')


def add_user(handle):
    # Used for sorting the followers
    global follower_table
    follower_table[handle] = []
    sorted_follower = sorted(follower_table.items(), key=lambda item: item[0])
    sorted_follower_table = {}
    for key, value in sorted_follower:
        sorted_follower_table[key] = value
    follower_table = sorted_follower_table


# This function will take all these messages and distribute them to the clients
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            # print(message.decode())
            # Might have to change this part!
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    server.sendto("", client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

