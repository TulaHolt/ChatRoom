import socket, sys, threading
#server info
PORT = 8000
bufferSize = 4096
name = ''

#functions


def receive():
    while True:
        try:
            message = client.recv(bufferSize).decode()
            if message == 'NICKNAME':
                client.send(name.encode())
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        msg = input('')
        #message = '{}: {}'.format(name, msg)
        if msg == "/quit":
            message = '{} logged out'.format(name)
            client.send(message.encode())
            client.close()
            sys.exit(1)
        client.send(msg.encode())


#main body of client


if len(sys.argv) != 2 :
    print("try again")
    sys.exit(1)
else :
    address = (sys.argv[1],PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    print("connected to " , address)
    print(client)

    name = input("what's your name: ")
    print ("Welcome, " , name)

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()