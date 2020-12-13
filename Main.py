from Database import Database
from flask import Flask, request, render_template
import PageValues

SERVER_NAME = "Server"
IP_ADDRESS = "0.0.0.0"
PORT = 105

app = Flask(SERVER_NAME)
app.config["DEBUG"] = True
db = Database()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template(PageValues.login_page_path, name=PageValues.name, header=PageValues.login_page_header, error="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template(PageValues.register_page_path, name=PageValues.name, header=PageValues.register_page_header)


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.args.get("type") == "login":
        success, data = db.check_user(request.form["email"], request.form["password"])
    else:
        success, data = db.add_user(request.form["email"], request.form["password"])
    if success:
        return render_template(PageValues.search_page_path, name=PageValues.name,
                               header=PageValues.search_page_page_header, person_name=request.form["email"])
    else:
        if request.args.get("type") == "login":
            return render_template(PageValues.login_page_path, name=PageValues.name, header=PageValues.login_page_header,
                                   error=data)
        else:
            return render_template(PageValues.register_page_path, name=PageValues.name,
                                   header=PageValues.login_page_header, error=data)


@app.route('/results', methods=['GET', 'POST'])
def results_page():
    success, data = db.check_user(request.form["email"], request.form["password"])
    if success:
        success, data = db.search_movies(request.form["search_string"])
        print(data)
        return render_template(PageValues.results_page_path, name=PageValues.name,
                               header=PageValues.results_page_page_header, person_name=request.form["email"],
                               password=request.form["password"])
    else:
        return render_template(PageValues.login_page_path, name=PageValues.name, header=PageValues.login_page_header,
                               error=data)


app.run(host=IP_ADDRESS, port=PORT)
