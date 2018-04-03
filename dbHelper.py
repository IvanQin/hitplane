import sqlite3


class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql = 'create table if not exists gamedata (userName varchar(20), level varchar(10), score int)'
        self.cursor.execute(sql)
        self.conn.commit()

    def add_record(self, player_name, level, score):
        sql = 'insert into gamedata (userName, level, score) values (?,?,?)'
        self.cursor.execute(sql, (player_name, level, score))
        self.conn.commit()

    def is_user_exist(self, player_name):
        sql = 'select * from gamedata where userName=?'
        self.cursor.execute(sql, (player_name,))
        values = self.cursor.fetchall()
        return len(values) > 0

    def update_record(self, player_name, level, score):
        sql = 'update gamedata set level=?, score=? where userName=?'
        self.cursor.execute(sql, (level, score, player_name))
        self.conn.commit()

    def find_top_score(self):
        sql = 'select * from gamedata order by score desc'
        self.cursor.execute(sql)
        values = self.cursor.fetchall()
        return values

    def close(self):
        self.conn.close()
