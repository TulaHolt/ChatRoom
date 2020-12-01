#how the rooms are defined for use by hall.py

class Room:

    def __init__(self, roomName):
        self.history = ''
        self.nicks = []
        self.name = roomName


    def broadcast(self, user, msg):
        self.msg = user.name + ": " + msg
        self.history = self.history + str(msg)
        for nick in self.nicks:
            print("loop")
            nick.socket.sendall(self.msg.encode())
            #nick.socket.sendall(b"")#msg.encode())


    def userSetup(self, user):
        message = '{}! welcome to, {}'.format(user, self.name)
        self.history = self.history + message
        user.socket.sendall(self.history.encode())
        for present in self.nicks:
            if present.name != user.name:
                user.socket.sendall(self.history.encode())



    def userRemoval(self, user):
        self.nicks.remove(user)
        message = '{} has left, {}'.format(user, self.name)
        self.history = self.history + str(message)
        for present in self.nicks:
            if present.name != user.name:
                present.socket.sendall(message.encode())
