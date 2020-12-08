#how the rooms are defined for use by hall.py
ENC = 'ascii'
class Room:

    def __init__(self, roomName):
        self.history = ''
        self.nicks = []
        self.name = roomName
        self.msg = ''

    def displayNicks(self, user):
        for nick in self.nicks:
            if self.msg == '':
                self.msg = nick.name
            else:
                self.msg = self.msg + ", " + nick.name
            #print (self.msg)
        #self.msg = self.msg + "\n"
        print(self.msg)
        user.socket.sendall(self.msg.encode(ENC))
        user.socket.sendall("\n".encode(ENC))
        self.msg = ''

    def broadcast(self, msg):
        #self.msg = msg
        self.msg = self.name + " >> " + msg
        self.history = self.history + str(msg)
        for person in self.nicks:
            person.socket.sendall(self.msg.encode(ENC))
        self.msg = ''


    def userSetup(self, user):
        message = '{}! welcome to, {}'.format(user, self.name)
        self.history = self.history + message
        user.socket.sendall(self.history.encode(ENC))
        for present in self.nicks:
            if present.name != user.name:
                user.socket.sendall(self.history.encode(ENC))



    def userRemoval(self, user):
        self.nicks.remove(user)
        message = '{} has left, {}'.format(user.name, self.name)
        self.history = self.history + str(message)
        for present in self.nicks:
            if present.name != user.name:
                present.socket.sendall(message.encode(ENC))
