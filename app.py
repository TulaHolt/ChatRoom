

from flask import Flask, render_template, request
import key_config as keys
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=keys.ACCESS_KEY_ID,
                          aws_secret_access_key=keys.ACCESS_SECRET_KEY, region_name="us-east-1")


from boto3.dynamodb.conditions import Key, Attr


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
        msg = "Registration Complete. Please Login to your account !"

        return render_template('login.html', msg=msg)
    return render_template('index.html')


# Create template for login
@app.route('/login')
def login():
    return render_template('login.html')


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
        if password == items[0]['password']:
            return render_template("home.html", username=username)
    return render_template("login.html")


@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)