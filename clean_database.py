import os
import sqlite3

connection = sqlite3.connect('{0}.db' . format(os.getenv('NAME')))
cursor = connection.cursor()

ignored_users = os.getenv('IGNORED_USERS', '').split(',')

cursor.execute("""
--sql
UPDATE messages SET ignore = 1 WHERE author IN ({0}) AND ignore = 0
;
""" . format(
        ('?, ' * (len(ignored_users) - 1)) + '?'
    ),
    ignored_users
)

cursor.execute("""
--sql
    UPDATE messages SET ignore = 1 WHERE length < 5 AND ignore = 0
;
""")

cursor.execute("""
--sql
    UPDATE messages SET ignore = 1 WHERE message NOT LIKE "% % %" AND ignore = 0;
""")

