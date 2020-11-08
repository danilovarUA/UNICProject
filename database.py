import sqlite3
DATABASE_NAME = "project_database.db"

class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def perform_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def add_user(self):
        pass

    def check_user(self):
        pass

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
