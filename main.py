from database import Database
from flask import Flask, request, render_template
import constants
SERVER_NAME = "Server"
IP_ADDRESS = "0.0.0.0"
PORT = 105


app = Flask(SERVER_NAME)
app.config["DEBUG"] = True
db = Database()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", name=constants.name, header=constants.login_page_header, error="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html", name=constants.name, header=constants.register_page_header)


@app.route('/personalPage', methods=['GET', 'POST'])
def personal_page():
    if request.args.get("type") == "login":
        success, data = db.check_user(request.form["email"], request.form["password"])
    else:
        success, data = db.add_user(request.form["email"], request.form["password"])
    if success:
        return render_template("personalPage.html", name=constants.name, header=constants.personal_page_page_header,
                               person_name=request.form["email"])
    else:
        if request.args.get("type") == "login":
            return render_template("login.html", name=constants.name, header=constants.login_page_header,
                                   error=data)
        else:
            return render_template("register.html", name=constants.name, header=constants.login_page_header,
                                   error=data)


app.run(host=IP_ADDRESS, port=PORT)
