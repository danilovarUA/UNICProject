import sqlite3
DATABASE_NAME = "project_database.db"


class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def _perform_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True, None
        except sqlite3.OperationalError as error:
            return False, str(error)

    def add_user(self, email, password):
        query = "INSERT INTO user (email,password) VALUES( '{}',	'{}')".format(email, password)
        try:
            return self._perform_query(query)
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: user.email" == str(error):
                return False, "This email is already registered"
            else:
                return False, error

    def check_user(self, email, password):
        query = "SELECT * FROM user WHERE email='{}' AND password='{}'".format(email, password)
        result = self._perform_query(query)
        if not result[0]:
            return result
        else:
            rows = self.cursor.fetchall()
            if len(rows) == 1:
                return True, None
            else:
                return False, "User not found"

    def add_rating(self, user_id, movie_id, rating):
        query = "INSERT INTO rating (user_id,movie_id, rating) VALUES( '{}', '{}', '{}')".format(
            user_id, movie_id, rating)
        return self._perform_query(query)

    def search_movies(self, search_string):
        query = "SELECT * FROM movie WHERE name LIKE '{}'".format(search_string)
        result = self._perform_query(query)
        if result[0]:
            return True, self.cursor.fetchall()
        return result

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    # populate movies
    # movies = ["Titanic", "The Wizard of Oz", "Star Wars: Episode IV - A New Hope",
    #           "The Lord of the Rings: The Return of the King", "Snow White and the Seven Dwarfs ",
    #           "Terminator 2: Judgment Day", "The Lion King", "The Godfather", "The Jesus Film", "Jurassic Park",
    #           "Raiders of the Lost Ark", "The Shawshank Redemption", "The Dark Knight",
    #           "Pirates of the Caribbean: The Curse of the Black Pearl", "Jaws", "Fight Club", "Pulp Fiction",
    #           "Forrest Gump", "Shrek", "Transformers", "The Matrix"]
    # db = Database()
    # for mov in movies:
    #     query = "INSERT INTO movie (name) VALUES( '{}')".format(mov)
    #     print (db._perform_query(query))

    # movie search test
    db = Database()
    res = db.search_movies('the dark knight')
    print(res)
