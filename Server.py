import socket, sys, threading
from hall import Hall
from player import Player
#constants list

PORT = 8000                     #Can be any number really, just details what port to connect to within the given ip
bufferSize = 4096               #Gotta figure out this still
MAXUSERS = 5                    #How many users can connect to chat service
HOST = ''                       #Stores IP address for host

#variables

clients = []

#functions


def broadcast(message):
    for client in clients:
        client.send(message)


def sendM(user):
    while True:
        try:
            message = client.recv(bufferSize).decode()
            print(user.name + " Is talking:\n")
            hallway.get(user, message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break



#main body of server

if len(sys.argv) != 2 :
    print("Incorrect information supplied. Try again")
    sys.exit(1)
else:
    HOST = sys.argv[1]
    address = (HOST,PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #the line above creates a connection using the python library "socket"
    #the first argument defines the protocol family, here AF_INET is the IPv4 protocol, and is considered the default for this library
    #the second argument here defines the type of connection, here SOCK_STREAM is used to create a TCP connection.

server.bind(address)
    #binds the address given when running the program to the socket

server.listen(MAXUSERS)
    #socket is now listening for connections made to the binded address, as long as the max amount of users has not been met

print("Server has started with ip and port of", address)

hallway = Hall()

while True:
    client, address = server.accept()
    client.send('NICKNAME'.encode())
    nickname = client.recv(bufferSize).decode()
    user = Player(client, nickname)
    clients.append(client)

    print("Nickname is {}".format(user.name))
    broadcast("{} joined! The Server".format(user.name).encode())
    client.send('Connected to server!'.encode())
    thread = threading.Thread(target=sendM, args=(user,))
    thread.start()



