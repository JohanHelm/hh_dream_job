import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_vacancy_id(self, vacancy_id):
        with self.connection:
            self.cursor.execute("INSERT INTO allready_applyed ('id') VALUES (?)", (vacancy_id, ))

    def get_already_applied(self):
        with self.connection:
            return self.cursor.execute("SELECT id FROM allready_applyed").fetchall()
