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
        print(query)
        result = self._perform_query(query)
        if not result[0]:
            return result
        else:
            rows = self.cursor.fetchall()
            return True, len(rows) == 1

    def add_rating(self):
        pass

    def add_movie(self):
        pass

    def add_recommendation(self):
        pass

    def remove_recommendation(self):
        pass

    def __del__(self):
        self.connection.close()
