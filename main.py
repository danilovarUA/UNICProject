from database import Database
from flask import Flask, request
SERVER_NAME = "Server"
IP_ADDRESS = "0.0.0.0"
PORT = 105


app = Flask(SERVER_NAME)
app.config["DEBUG"] = True
db = Database()


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = db.check_user(request.args["email"], request.args["password"])
    if response[0]:
        if response[1]:
            return "User in DB"
        else:
            return "User not in DB"


@app.route('/register', methods=['GET', 'POST'])
def register():
    response = db.add_user(request.args["email"], request.args["password"])
    return str(response)


app.run(host=IP_ADDRESS, port=PORT)