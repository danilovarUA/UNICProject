import random

import faker
import pandas as pd
from sqlalchemy.exc import IntegrityError

from Database import session, User, Movie, Rating, Recommendation
from Tools.PasswordGenerator import generate_password

faker = faker.Faker()


def prefill_users(clean=True, amount=1000):
    if clean:
        session.query(User).delete()
    for counter in range(amount):
        user = User(email=faker.email(), password=generate_password(), name=faker.name())
        session.add(user)
    user = User(email="admin", password="pass", name="Administrator")
    session.add(user)
    session.commit()


def prefill_movies(clean=True):
    if clean:
        session.query(Movie).delete()
    data = pd.read_csv('../data/movies_metadata.csv')
    titles = data["original_title"]
    for title in titles:
        movie = Movie(name=title)
        session.add(movie)
    session.commit()


def prefill_ratings_from_csv(clean=True):
    if clean:
        session.query(Rating).delete()
    data = pd.read_csv('../data/ratings_small.csv')
    user_ids = data["userId"]
    movie_ids = data["movieId"]
    ratings = data["rating"]
    ratings_sql = []
    for index in range(len(user_ids)):
        ratings_sql.append(Rating(user_id=user_ids[index].item(),
                                  movie_id=movie_ids[index].item(),
                                  mark=ratings[index].item()))
    counter = 0
    for rating_sql in ratings_sql:
        counter += 1
        if counter % 1000 == 0:
            print("{}/{}".format(counter, len(ratings_sql)))
        try:
            session.add(rating_sql)
            if counter % 100 == 0:
                session.commit()
        except IntegrityError:
            session.rollback()
            print("Skipping, violates constraints")


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
        # prefill_ratings()
        prefill_ratings_from_csv(clean=True)

    if recommendations_clean:
        clean_recommendations()


if __name__ == "__main__":
    main()
