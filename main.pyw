"""
Save auto repair notes.

Created on 25.05.2017

@author: Ruslan Dolovanyuk

"""

import sqlite3

from drawer import Drawer


def setup(conn, cursor):
    """Create table in database."""
    script = '''CREATE TABLE window (
                id INTEGER PRIMARY KEY NOT NULL,
                px INTEGER NOT NULL,
                py INTEGER NOT NULL,
                sx INTEGER NOT NULL,
                sy INTEGER NOT NULL) WITHOUT ROWID
             '''
    cursor.execute(script)
    script = '''INSERT INTO window (id, px, py, sx, sy)
             VALUES (1, 0, 0, 800, 600)'''
    cursor.execute(script)
    script = '''CREATE TABLE category (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL) WITHOUT ROWID
             '''
    cursor.execute(script)
    script = '''CREATE TABLE main (
                id INTEGER PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                company TEXT,
                model TEXT,
                serial TEXT,
                data TEXT,
                category INTEGER NOT NULL) WITHOUT ROWID
             '''
    cursor.execute(script)
    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect('autonotes.db')
    cursor = conn.cursor()

    str_sql = 'SELECT * FROM sqlite_master WHERE name = "main"'
    cursor.execute(str_sql)
    if not cursor.fetchone():
        setup(conn, cursor)

    drawer = Drawer(conn, cursor)
    drawer.mainloop()

    cursor.close()
    conn.close()
