from Database import Database
import faker
import random
import pandas as pd
from Tools.PasswordGenerator import generate_password


db = Database()
faker = faker.Faker()


def prefill_users(clean=True, amount=20):
    table_name = "user"
    if clean:
        print("Importing users with pre clean")
        result = db.delete({"name": "/*"}, table_name)  # all users
        print("Users cleaned with result: ({})".format(result))
    else:
        print("Importing users")
    for counter in range(1, amount+1):
        name = faker.name()
        email = faker.email()
        password = generate_password()
        result = db.insert({"email": email, "password": password, "name": name}, table_name)
        print("Inserting user {}/{} [{}]: ({})".format(counter, amount, result, email))

    # Inserting admin user for faster debug
    result = db.insert({"email": "admin", "password": "pass", "name": "Administrator"}, table_name)
    print("Inserting user [{}]: ({})".format( result, "admin"))


def prefill_movies(clean=True, amount=500):
    table_name = "movie"
    if clean:
        print("Importing movies with pre clean")
        result = db.delete({"name": "/*"}, table_name)
        print("Movies cleaned with result: ({})".format(result))
    else:
        print("Importing movies")
    data = pd.read_csv('../data/movies_metadata.csv')
    titles = data["original_title"][:amount]
    counter = 0
    for title in titles:
        counter += 1
        result = db.insert({"name": title}, table_name)
        print("Inserting movie {}/{} [{}]: ({})".format(counter, len(titles), result, title))


def prefill_likes(clean=True, max_amount=50):
    table_name = "rating"
    if clean:
        print("Importing likes with pre clean")
        result = db.delete_all(table_name)
        print("Likes cleaned with result: ({})".format(result))
    else:
        print("Importing likes")

    all_movies = db.select({"name": "/*"}, "movie")[1]
    movie_ids = [movie[0] for movie in all_movies]
    all_users = db.select({"name": "/*"}, "user")[1]
    user_ids = [user[0] for user in all_users]
    user_counter = 0
    for user_id in user_ids:
        user_counter += 1
        movie_counter = 0
        sampled_movie_ids = random.sample(movie_ids, random.randint(0, max_amount))
        for movie_id in sampled_movie_ids:
            movie_counter += 1
            rating = random.randint(1, 5)
            result = db.insert({"movie_id": movie_id, "user_id": user_id, "rating": rating}, table_name)
            print("Inserting like for user {}/{} and movie {} {}/{} [{}]".format(
                user_counter, len(user_ids), movie_id, movie_counter, len(movie_ids), result))


def main(movies=True, users=True, likes=True, recommendations_clean=True):
    if movies:
        prefill_movies()
    if users:
        prefill_users()
    if likes:
        prefill_likes()

    if recommendations_clean:
        db.delete_all("recommendations")


if __name__ == "__main__":
    main()
