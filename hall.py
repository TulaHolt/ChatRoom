#hallway of rooms, handles the creation and destruction of rooms
from lounge import Room
from player import Player
class Hall:

    def __init__ (self):
        self.rooms = {}
        self.names = []
        self.usersRoom = {}
        self.disp = []
        self.commandList = b'Commands:\n'

    def get(self, user, message):
        #user.socket.sendall(message.encode(4096))
        if "/create" in message:
            self.createRoom(user, message)
        elif "/display all" in message:
            self.listrooms(user)
        elif "/join" in message:
            self.joinRoom(user, message)
        elif user in self.usersRoom:
            for user in self.usersRoom:
                self.rooms[self.usersRoom[user]].broadcast(message)
        else:
            print("user not in room")
            user.socket.sendall(b"error: not in a room")


    def createRoom(self, user, msg):
        rn = msg.split()
        rName = str(rn[2])
        print(rName)
        room = Room(rName)
        self.names.append(rName)
        self.rooms[rName] = room
        user.socket.sendall(b"created " + self.rooms[rName].name.encode())
        #user.socket.sendall(b"hey" + self.commandList)
        self.addtoRoom(user, room.name)

    def addtoRoom(self, user, rName):
        self.rooms[rName].nicks.append(user)
        self.usersRoom[user] = rName

    def listrooms(self, user):
        for name in self.names:
            user.socket.send(b"\n" + self.rooms[name].name.encode())
            self.rooms[name].displayNicks(user)

    def joinRoom(self, user, msg):
        rn = msg.split()
        rName = str(rn[2])
        self.addtoRoom(user, rName)

