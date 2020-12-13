from Database import Database
from flask import Flask, request, render_template, redirect, url_for
import PageValues

SERVER_NAME = "Server"
IP_ADDRESS = "0.0.0.0"
PORT = 105
DEFAULT_PAGE = "search"

app = Flask(SERVER_NAME)
app.config["DEBUG"] = True
db = Database()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    logged_in, error = logged_in_cookies()
    if logged_in:
        return redirect(url_for(DEFAULT_PAGE))
    page_data = PageValues.pages["login"]
    if "error" in request.values:
        page_data["error"] = request.values["error"]
    return render_template(page_data["url"], data=page_data)


@app.route('/set_login_cookies', methods=['GET', 'POST'])
def set_login_cookies():
    if request.method in ['POST','GET']:
        if "reset" in request.values:
            email = ""
            password = ""
        else:
            email = request.form['email']
            password = request.form["password"]
        resp = redirect(url_for(DEFAULT_PAGE))
        resp.set_cookie('email', email)
        resp.set_cookie('password', password)
        return resp


def logged_in_cookies():
    email = request.cookies.get('email')
    password = request.cookies.get("password")
    success, data = db.select({"email": "^" + email + "$", "password": "^" + password + "$"}, 'user')
    success = success & len(data) == 1  # query was successful and one entry was found with that email and password
    if not success and len(data) == 0:
        data = "No such email"
    if email == "":
        data = ""
    return success, data


@app.route('/register', methods=['GET', 'POST'])
def register():
    raise ValueError("Not implemented")


def check_and_go(page_name, additional_data=None):
    logged_in, error = logged_in_cookies()
    if logged_in:
        page_data = PageValues.pages[page_name]
        if additional_data is not None:
            page_data.update(additional_data)
        return render_template(page_data["url"], data=page_data)
    else:
        return redirect(url_for('login', error=error))


@app.route('/search', methods=['GET', 'POST'])
def search():
    email = request.cookies.get('email')
    password = request.cookies.get("password")
    _, data = db.select({"email": "^" + email + "$", "password": "^" + password + "$"}, 'user')
    try:
        top_up_data = {"person_name": data[0][3]}
    except IndexError:
        top_up_data = {}
    return check_and_go("search", top_up_data)


@app.route('/results', methods=['GET', 'POST'])
def results():

    return check_and_go("results")


app.run(host=IP_ADDRESS, port=PORT)
