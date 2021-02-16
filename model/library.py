import sqlite3
from datetime import datetime


class Library():
    def __init__(self):
        self.conn = sqlite3.connect('db/library.db')

    def findAll(self):
        c = self.conn.cursor()
        c.execute(
            f"SELECT title FROM books"
        )
        return [r[0] for r in c.fetchall()]

    def findBooksByTarget(self, target):
        c = self.conn.cursor()
        # Create table
        c.execute(
            f"SELECT b.title FROM books b, books_tags_link bt, tags t WHERE b.id=bt.book AND bt.tag=t.id AND t.name='{target}'"
        )
        return [r[0] for r in c.fetchall()]

    def closeConnection(self):
        self.conn.close()
