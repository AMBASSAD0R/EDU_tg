import sqlite3

class SQL:
    def __init__(self, path_db):
        self.connection = sqlite3.connect(path_db)
        self.cursor = self.connection.cursor()

    def create_task(self, id, subject, text_tasks, answer, file_id, photo_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'tasks' (id, subject, text_task, answer, file_id, photo_id)  VALUES  (?,?,?,?,?,?)", (int(id), subject, text_tasks, answer, file_id, photo_id))

    def check_tasks(self, id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM tasks WHERE id = {id};').fetchall()
            return bool(len(result))
