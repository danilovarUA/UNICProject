from Database import session, User, Movie, Rating, Recommendation
import faker
import random
import pandas as pd
from Tools.PasswordGenerator import generate_password


faker = faker.Faker()


def prefill_users(clean=True, amount=50):
    if clean:
        session.query(User).delete()
    for counter in range(amount):
        user = User(email=faker.email(), password=generate_password(), name=faker.name())
        session.add(user)
    user = User(email="admin", password="pass", name="Administrator")
    session.add(user)
    session.commit()


def prefill_movies(clean=True, amount=50):
    if clean:
        session.query(Movie).delete()
    data = pd.read_csv('../data/movies_metadata.csv')
    titles = data["original_title"][:amount]
    for title in titles:
        movie = Movie(name=title)
        session.add(movie)
    session.commit()


def clean_recommendations():
    session.query(Recommendation).delete()
    session.commit()


def prefill_ratings(clean=True, max_amount=30):
    if clean:
        session.query(Rating).delete()

    movies = session.query(Movie).all()
    users = session.query(User).all()
    for user in users:
        sampled_movies = random.sample(movies, random.randint(0, max_amount))
        for movie in sampled_movies:
            rating = Rating(user_id=user.id, movie_id=movie.id, mark=random.randint(1, 5))
            session.add(rating)
    session.commit()


def main(movies=True, users=True, ratings=True, recommendations_clean=True):
    if movies:
        prefill_movies()
    if users:
        prefill_users()
    if ratings:
        prefill_ratings()

    if recommendations_clean:
        clean_recommendations()


if __name__ == "__main__":
    main()
