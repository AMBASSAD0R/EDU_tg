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

    def update_task_id(self, user_id, task_id):
        with self.connection:
            return self.cursor.execute('''UPDATE `user_task` SET `task_id` = ? WHERE `user_id` = ?''',
                                       (task_id, user_id))

    def add_user_in_user_task(self, user_id, task_id):
        with self.connection:
            return self.cursor.execute('''INSERT INTO 'user_task' (user_id, task_id)  VALUES  (?,?)''',
                                       (user_id, task_id))

    def create_static(self, user_id, col_true, col_false, staicstic):
        with self.connection:
            return self.cursor.execute('''INSERT INTO 'user_statistic' (user_id,сol_true_answer,col_false_answer,col_resh)  VALUES  (?,?,?,?)''',
                                       (user_id, col_true, col_false, staicstic))

    def update_col_true(self, user_id, col_true):
        with self.connection:
            return self.cursor.execute('''UPDATE `user_statistic` SET `сol_true_answer` = ? WHERE `user_id` = ?''',
                                       (col_true, user_id))

    def update_col_false(self, user_id, col_false):
        with self.connection:
            return self.cursor.execute('''UPDATE `user_statistic` SET `сol_false_answer` = ? WHERE `user_id` = ?''',
                                       (col_false, user_id))

    def update_col_false(self, user_id, stat):
        with self.connection:
            return self.cursor.execute('''UPDATE `user_statistic` SET `col_resh` = ? WHERE `user_id` = ?''',
                                       (stat, user_id))

    def close_connection(self):
        self.sqlite_connection.close()
        return True

    def get_task_id_user(self, user_id):
        get_q = f'SELECT task_id FROM user_task WHERE user_id = {user_id};'
        with self.connection:
            result = self.cursor.execute(get_q).fetchall()
            res = str(result[0])[1:]
            res = res[:-2]
            print(res)
            return str(res)

    def get_statistic(self, user_id):
        get_q = f'SELECT * FROM user_statistic WHERE user_id = {user_id};'
        with self.connection:
            result = self.cursor.execute(get_q).fetchall()
            return result

    def get_task(self, id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchall()
            return result
    
    def get_task_answer(self, id):
        with self.connection:
            result = self.cursor.execute('SELECT answer FROM tasks WHERE id = ?', (id,)).fetchall()
            return result
        
    def get_all_task(self, number_task):
        get_q = f'SELECT * FROM tasks WHERE number_task = {number_task};'
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
