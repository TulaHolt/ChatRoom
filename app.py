'''
Chat room application. Users can sign up or login and join/create chat rooms and talk to eachother in
real time
'''
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import boto3

# Create instance of the class
app = Flask(__name__)
# Encapsulate flask app. A new server will be running
socketio = SocketIO(app)


dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

from boto3.dynamodb.conditions import Key, Attr


# Render first page which is the signup page
@app.route('/')
def index():
    return render_template('index.html')


# Sign up methods allowing user to create username and password
@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        table = dynamodb.Table('users')

        table.put_item(
            Item={
                'username': username,
                'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account!"

        return render_template('login.html', msg=msg)
    return render_template('index.html')


# User can choose that they are returning and just want to login
@app.route('/login')
def login():
    return render_template('login.html')


# User on login in page types in username and password and is checked against the table
@app.route('/check', methods=['post'])
def check():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        table = dynamodb.Table('users')
        response = table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        items = response['Items']
        username = items[0]['username']
        print(items[0]['password'])
        tab = dynamodb.Table('room')
        gbentries = tab.scan()
        r = ([ [f['roomname']] for f in gbentries['Items']])
        room = [dict(roomname=row[0]) for row in r]
        if password == items[0]['password']:
            return render_template("home.html", username=username, room=room)
    return render_template("login.html")


@app.route('/home')
def home():
    table = dynamodb.Table('room')
    gbentries = table.scan()
    r = ([[f['roomname']] for f in gbentries['Items']])
    room = [dict(roomname=row[0]) for row in r]
    return render_template('home.html', room=room)


# Create new room template
@app.route('/createroom')
def createroom():
    return render_template('createroom.html')


# User enters a new room to be stored
@app.route('/newroom', methods=['post'])
def newroom():
    if request.method == 'POST':
        roomname = request.form['roomname']

        table = dynamodb.Table('room')
        ''' 
        response = table.query(
            KeyConditionExpression=Key('roomname').eq(roomname)
        )
        items = response['Items']
        if roomname == items[0]['roomname']:
            msg = "Room name already exists"
            return render_template("createroom.html", msg=msg)
        '''

        table.put_item(
            Item={
                'roomname': roomname
            }
        )
        msg = "New room added!"
        tab = dynamodb.Table('room')
        gbentries = tab.scan()
        r = ([[f['roomname']] for f in gbentries['Items']])
        room = [dict(roomname=row[0]) for row in r]

        return render_template('home.html', msg=msg, room=room)
    return render_template('createroom.html')


# Sends user to appropriate chatroom depending on which they choose to join
@app.route('/chat/<chatroom>/<username>')
def chat(chatroom, username):
    return render_template('chat.html', username=username, chatroom=chatroom)


# Display all users in a room
# @socketio.on('')

# Allows user to join room and notifies room that someone has joined
@socketio.on('join_room')
def handle_join_room_event(data):
    # Will print the time the user joined
    app.logger.info("{} has joined the chat room {}".format(data['username'], data['chatroom']))
    # Makes the client join the room
    join_room(data['chatroom'])
    # Will inform other relevant clients that someone joined the room
    socketio.emit('join_room_announcement', data, chatroom=data['chatroom'])


# Allows user to leave room and notifies room that someone has left
@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the chat room {}".format(data['username'], data['chatroom']))
    # Makes the client leave the room
    leave_room(data['chatroom'])
    # Will inform other relevant clients that someone left the room
    socketio.emit('leave_room_announcement', data, chatroom=data['chatroom'])


# Allows user to send a message
@socketio.on('send_message')
def handle_send_message_event(data):
    # inform that someone has sent a message
    app.logger.info("{} has sent a message to the chat room {}: {}".format(data['username'], data['chatroom'], data['message']))
    # emit the message out to all other people in the room
    socketio.emit('recieve_message', data, chatroom=data['chatroom'])


''' 
def chat():
    # Get username and room name to join correct chat
    username = request.args.get('username')
    chatroom = request.args.get('chatroom')

    room = request.args.get('room')
    # make sure we have these two values before rendering chat
    if username and chatroom:
        return render_template('chat.html', username=username, chatroom=chatroom, room=room)

    msg = "Enter valid Room Name"
    return render_template('home.html', username=username, msg=msg, room=room)
    '''



if __name__ == "__main__":
    socketio.run(app, debug=True)
    # app.run(debug=True)
