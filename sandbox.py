from flask import Flask, request
SERVER_NAME = "Server"
IP_ADDRESS = "0.0.0.0"
PORT = 105


app = Flask(SERVER_NAME)
app.config["DEBUG"] = True


@app.route('/login', methods=['GET', 'POST'])
def login():
    return str(dict(request.args))


app.run(host=IP_ADDRESS, port=PORT)
