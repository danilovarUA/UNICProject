import sqlite3
import re
import os

DATABASE_NAME = "{}/data/project_database.db".format(os.path.dirname(os.path.abspath(__file__)))


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


class Database:
    connection = None
    cursor = None

    def __init__(self, debug=False):
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
                print("Data returned: {}".format(data))
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

    def delete(self, data, table):
        selectors = []
        for name in data:
            value = data[name]
            selectors.append("{} REGEXP '{}'".format(name, value))
        query = "DELETE FROM {} WHERE {}".format(table, " AND ".join(selectors))
        if self.debug:
            print("Database created delete query: {}".format(query))
        result = self._perform_query_(query)
        if result[0]:
            data = self.cursor.fetchall()
            if self.debug:
                print("Data returned: {}".format(data))
            return True, data
        return result

    def delete_all(self, table):
        # TODO reimplement using only delete and FUCKING DEPRECATE IT
        query = "DELETE FROM {}".format(table)
        result = self._perform_query_(query)
        return result

    def __del__(self):
        self.connection.close()
        if self.debug:
            print("Database was destroyed")
