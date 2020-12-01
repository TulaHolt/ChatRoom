#hallway of rooms, handles the creation and destruction of rooms
from lounge import Room
from player import Player
class Hall:

    def __init__ (self):
        self.rooms = {}
        self.names = []
        self.numUsers = 0
        self.usersRoom = {}
        self.disp = []
        self.commandList = b'Commands:\n'

    def get(self, user, message):
        print("{}: {}".format(user.name, message))
        #user.socket.sendall(message.encode(4096))
        if "/create" in message:
            self.createRoom(user, str(message))
        elif "/display all" in message:
            self.listrooms(user)
        elif "/join" in message:
            self.joinRoom(user, message)
        else:
            if user.name in self.usersRoom:
                self.rooms[self.usersRoom[user.name]].broadcast(user, message)
            else:
                print("user not in room")
                user.socket.sendall(b"error: not in a room")


    def createRoom(self, user, msg):
        rn = msg.split()
        rName = str(rn[1])
        room = Room(rName)
        self.names.append(rName)
        self.rooms[rName] = room
        user.socket.sendall(b"created " + self.rooms[rName].name.encode())
        #user.socket.sendall(b"hey" + self.commandList)
        self.addtoRoom(user, room.name)

    def addtoRoom(self, user, rName):
        self.rooms[rName].nicks.append(user.name)
        self.usersRoom[user.name] = rName

    def listrooms(self, user):
        for name in self.names:
            user.socket.sendall(b"" + self.rooms[name].name.encode() + b'\n')
            user.socket.sendall(str(self.rooms[name].nicks).encode() + b'\n')
            #self.rooms[name].displayNicks(user)

    def joinRoom(self, user, msg):
        rn = msg.split()
        rName = str(rn[1])
        self.addtoRoom(user, rName)

