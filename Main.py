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
    try:
        email = request.cookies.get('email')
        password = request.cookies.get("password")
        success, data = db.select({"email": "^" + email + "$", "password": "^" + password + "$"}, 'user')
        success = success & len(data) == 1  # query was successful and one entry was found with that email and password
    except TypeError:
        return False, "No cookies"
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


def get_current_user():
    email = request.cookies.get('email')
    password = request.cookies.get("password")
    _, data = db.select({"email": "^" + email + "$", "password": "^" + password + "$"}, 'user')
    try:
        return data[0]
    except IndexError:
        return None


@app.route('/search', methods=['GET', 'POST'])
def search():
    user = get_current_user()
    top_up_data = {}
    if user is not None:
        top_up_data = {"person_name": user[3]}
    if "rank" in request.form:
        _, data = db.select({"name": request.form["movie"]}, "movie")
        movie_id = data[0][0]
        user_id = get_current_user()[0]
        db.insert({"movie_id": movie_id, "user_id": user_id, "rating": request.form["rank"]}, "rating")
        top_up_data.update({"message": "Your like {} for movie {} was added".format(request.form["rank"],
                                                                                    request.form["movie"])})
    return check_and_go("search", top_up_data)


@app.route('/results', methods=['GET', 'POST'])
def results():
    top_up_data = {}
    _, data = db.select({"name": '^{}$'.format(request.form["search_string"])}, 'movie')
    print(data)
    top_up_data.update({"movies": data})
    return check_and_go("results", top_up_data)


@app.route('/like', methods=['GET', 'POST'])
def like():
    top_up_data = {"movie": request.form["movie"]}
    return check_and_go("like", top_up_data)


app.run(host=IP_ADDRESS, port=PORT)
