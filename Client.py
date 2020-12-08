import socket, sys, threading
#server info
PORT = 8000
bufferSize = 'ascii'
name = ''

#functions


def receive():
    while True:
        try:
            message = client.recv(1024).decode(bufferSize)
            if message == 'NICKNAME':
                client.send(name.encode(bufferSize))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            sys.exit(1)


def write():
    while True:
        msg = '{}: {}'.format(name,input('>'))
        if msg == "/quit":
            message = '{} logged out'.format(name)
            client.send(message.encode(bufferSize))
            client.close()
            sys.exit(1)
        client.send(msg.encode(bufferSize))

'''def run():

        message = client.recv(1024).decode(bufferSize)

        if(message):
            if message == 'NICKNAME':
                client.send(name.encode(bufferSize))
            else:
                print(message)
             
        else:

            msg = '{}: {}'.format(name,input('>'))
            print(message)
            if message == "/quit":
                 message = '{} logged out'.format(name)
                 client.send(message.encode(bufferSize))
                 client.close()
                 sys.exit(1)
            else:
                client.send(msg.encode(bufferSize))'''



#main body of client


if len(sys.argv) != 2 :
    print("try again")
    sys.exit(1)
else :
    address = (sys.argv[1],PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    print("connected to " , address)

    name = input("what's your name: ")

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()
    #receive_thread = threading.Thread(target=run)
    #receive_thread.start()