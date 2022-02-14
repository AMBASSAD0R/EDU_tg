import sqlite3


class SQL:
    def __init__(self, path_db):
        self.connection = sqlite3.connect(path_db)
        self.cursor = self.connection.cursor()

    def create_task(self, id, subject, number_task, text_tasks, answer, file_id, photo_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT OR IGNORE INTO 'tasks' (id, subject, number_task, text_task, answer, file_id, photo_id, num_attempts, rights_solves, rating)  VALUES  (?,?,?,?,?,?,?,?,?,?)",
                (id, subject, number_task, text_tasks, answer, file_id, photo_id,0,0,0))

    def check_tasks(self, id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `tasks` WHERE `id` = ?', (id,)).fetchall()
            return bool(len(result))
    
    def update_task_num_attempts(self, id):
        pass

    def update_task_rating(self, id):
        pass

    def update_task_rights_solves(self, id):
        pass