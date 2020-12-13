import sqlite3
import re
DATABASE_NAME = "project_database.db"


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


class Database:
    connection = None
    cursor = None

    def __init__(self, debug=True):
        self.debug = debug
        self.connection = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.connection.create_function("REGEXP", 2, regexp)
        self.cursor = self.connection.cursor()
        if self.debug:
            print("Database was initialised")

    def _perform_query_(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            if self.debug:
                print("_perform_query_ was successfull")
            return True, None
        except sqlite3.DatabaseError as error:
            if self.debug:
                print("_perform_query_ was not successfull: {}".format(error))
            return False, str(error)

    def select(self, data, table):
        selectors = []
        for name in data:
            value = data[name]
            selectors.append("{} REGEXP '{}'".format(name, value))
        query = "SELECT * FROM {} WHERE {}".format(table, " AND ".join(selectors))
        if self.debug:
            print("Database created select query: {}".format(query))
        result = self._perform_query_(query)
        if result[0]:
            data = self.cursor.fetchall()
            if self.debug:
                print("Date returned: {}".format(data))
            return True, data
        return result

    def insert(self, data, table):
        field_names = []
        field_values = []
        for name in data:
            value = data[name]
            field_names.append("'{}'".format(name))
            field_values.append("'{}'".format(value))
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ", ".join(field_names),
                                                         ", ".join(field_values))
        if self.debug:
            print("Database created insert query: {}".format(query))
        return self._perform_query_(query)

    def __del__(self):
        self.connection.close()
        if self.debug:
            print("Database was destroyed")


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
    res = db.select({"name": '^$'}, 'movie')
    print(res)

