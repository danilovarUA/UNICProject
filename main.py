from database import Database
from flask import Flask, request, render_template
import constants


app = Flask(constants.flask_server_name)
app.config["DEBUG"] = True
db = Database()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template(constants.login_page_path, name=constants.name, header=constants.login_page_header, error="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template(constants.register_page_path, name=constants.name, header=constants.register_page_header)


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.args.get("type") == "login":
        success, data = db.check_user(request.form["email"], request.form["password"])
    else:
        success, data = db.add_user(request.form["email"], request.form["password"])
    if success:
        return render_template(constants.search_page_path, name=constants.name,
                               header=constants.search_page_page_header, person_name=request.form["email"])
    else:
        if request.args.get("type") == "login":
            return render_template(constants.login_page_path, name=constants.name, header=constants.login_page_header,
                                   error=data)
        else:
            return render_template(constants.register_page_path, name=constants.name,
                                   header=constants.login_page_header, error=data)


@app.route('/results', methods=['GET', 'POST'])
def results_page():
    success, data = db.check_user(request.form["email"], request.form["password"])
    if success:
        success, data = db.search_movies(request.form["search_string"])
        print(data)
        return render_template(constants.results_page_path, name=constants.name,
                               header=constants.results_page_page_header, person_name=request.form["email"],
                               password=request.form["password"])
    else:
        return render_template(constants.login_page_path, name=constants.name, header=constants.login_page_header,
                               error=data)


app.run(host=constants.flask_ip_address, port=constants.flask_port)
