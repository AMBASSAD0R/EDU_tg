import sqlite3


class WorkDB:
    def __init__(self, path_db):
        self.connection = sqlite3.connect(path_db)
        self.cursor = self.connection.cursor()

    def create_user(self, user_id, data_reg, date_last_use):
        with self.connection:
            return self.cursor.execute('''INSERT INTO 'users' (user_id, date_reg, date_last_use)  VALUES  (?,?,?)''',
                                       (user_id, data_reg, date_last_use))

    def check_user(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('''SELECT * FROM `users` WHERE `user_id` = ?''', (user_id,)).fetchall()
            return bool(len(result))

    def update_date_use(self, user_id, date_use):
        with self.connection:
            return self.cursor.execute('''UPDATE `users` SET `date_last_use` = ? WHERE `user_id` = ?''',
                                       (date_use, user_id))

    def close_connection(self):
        self.sqlite_connection.close()
        return True

    def get_quetions(self, user_id):
        get_q = f'SELECT col_quetions FROM user_info WHERE user_id = {user_id};'
        with self.connection:
            result = self.cursor.execute(get_q).fetchall()
            return int(str(result[0])[1:-2])

    def get_task(self, id):
        get_q = f'SELECT * FROM tasks WHERE id = {id};'
        with self.connection:
            result = self.cursor.execute(get_q).fetchall()
            return result

    def update_col_quetions(self, user_id, count_quetions):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute('''UPDATE `user_info` SET `count_quetions` = ? WHERE `user_id` = ?''',
                                       (count_quetions, user_id))

    def update_date_use(self, user_id, date_use):
        with self.connection:
            return self.cursor.execute('''UPDATE `users` SET `date_last_use` = ? WHERE `user_id` = ?''',
                                       (date_use, user_id))
