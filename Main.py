from Database import session, User, Movie, Rating, Recommendation
from flask import Flask, request, render_template, redirect, url_for
import PageValues
from Exceptions import AuthorisationException

IP_ADDRESS = "0.0.0.0"
PORT = 105
DEFAULT_PAGE = "search"
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        check_logged_in()
        return redirect(url_for(DEFAULT_PAGE))
    except AuthorisationException:
        data = PageValues.pages["login"]
        if "error" in request.values:
            data["error"] = request.values["error"]
        return render_template(data["url"], data=data)


@app.route('/set_login_cookies', methods=['GET', 'POST'])
def set_login_cookies():
    resp = redirect(url_for(DEFAULT_PAGE))
    if "reset" in request.values:
        email = ""
        password = ""
    else:
        email = request.form['email']
        password = request.form["password"]
    resp.set_cookie('email', email)
    resp.set_cookie('password', password)
    return resp


def check_logged_in():
    try:
        email = request.cookies.get('email')
        password = request.cookies.get("password")
        user = session.query(User).filter_by(email=email, password=password).first()
        if user is None:
            raise AuthorisationException("No such user")
    except TypeError:
        raise AuthorisationException("No cookies")


def go_to_page(url_name, additional_data):
    data = PageValues.pages[url_name]
    data.update(additional_data)
    return render_template(data["url"], data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        check_logged_in()
        return redirect(url_for(DEFAULT_PAGE))
    except AuthorisationException:
        data = PageValues.pages["register"]
        if "error" in request.values:
            data["error"] = request.values["error"]
        if "email" in request.form and "password" in request.form and "name" in request.form:
            user = User(name=request.form["name"], email=request.form["email"], password=request.form["password"])
            session.add(user)
            session.commit()
            # TODO: might throw exception if constrains are violated
            return redirect(url_for("set_login_cookies"))
        # TODO: check if it works with all the form fields
        return render_template(data["url"], data=data)


def get_current_user():
    return session.query(User).filter_by(email=request.cookies.get('email'),
                                         password=request.cookies.get("password")).first()


@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        check_logged_in()
        user = get_current_user()
        data = {"person_name": user.name}
        print(request.form)
        if "rank" in request.form and "movie_id" in request.form:  # Redirected here after adding like
            movie = session.query(Movie).filter_by(id=request.form["movie_id"]).first()
            session.add(Rating(user_id=user.id, movie_id=movie.id, mark=request.form["rank"]))
            session.commit()
            data["message"] = "Your like {} for movie '{}' was added".format(request.form["rank"], movie.name)

        return go_to_page("search", data)
    except AuthorisationException:
        return redirect(url_for('login'))


@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        check_logged_in()
        movies = []
        if "search_string" in request.form:
            movies = session.query(Movie).filter(Movie.name.contains(request.form["search_string"])).all()
        return go_to_page("results", {"movies": movies})
    except AuthorisationException:
        return redirect(url_for('login'))


@app.route('/like', methods=['GET', 'POST'])
def like():
    try:
        check_logged_in()
        movie = session.query(Movie).filter_by(id=request.form["movie_id"]).first()
        return go_to_page("like", {"movie": movie})
    except AuthorisationException:
        return redirect(url_for('login'))


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    try:
        check_logged_in()
        recs = session.query(Movie, Recommendation).filter(Recommendation.user_id == get_current_user().id
                                                           ).filter(Movie.id == Recommendation.movie_id).all()
        return go_to_page("recommendations", {"recommendations": recs})
    except AuthorisationException:
        return redirect(url_for('login'))


@app.route('/likes_history', methods=['GET', 'POST'])
def likes_history():
    try:
        check_logged_in()
        recs = session.query(Movie, Rating).filter(Rating.user_id == get_current_user().id
                                                           ).filter(Movie.id == Rating.movie_id).all()
        return go_to_page("likes_history", {"likes": recs})
    except AuthorisationException:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=IP_ADDRESS, port=PORT)
