import sqlite3

class Work_DB:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('sqlite_python.db')
        self.cursor = self.sqlite_connection.cursor()

     def create_user(self):
         sqlite_insert_query = """INSERT INTO unknown_table_1
                                   (id, text)  VALUES  (1, 'Демо текст')"""

         count = self.cursor.execute(sqlite_insert_query)
         self.sqlite_connection.commit()

    def close_connection(self):
        self.sqlite_connection.close()
        return True



