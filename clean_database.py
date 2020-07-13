import os
import sqlite3

connection = sqlite3.connect('{0}.db' . format(os.getenv('NAME')))
cursor = connection.cursor()

ignored_users = os.getenv('IGNORED_USERS', '').split(',')
ignored_words = os.getenv('IGNORED_WORDS', '').split(',')

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
UPDATE messages SET ignore = 1 WHERE ({0}) AND ignore = 0
;
""" . format(
        ('message LIKE ? OR ' * (len(ignored_words) - 1)) + 'message LIKE ?'
    ),
    list(map(lambda word: '"%{0}%"' . format (word), ignored_words))
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

cursor.execute("""
--sql
    UPDATE messages SET ignore = 1 WHERE
        message LIKE '% a %' AND
        message NOT LIKE '% hade a %' AND
        message NOT LIKE '% skjer a %' AND
        message NOT LIKE '% a ye %' AND
        ignore = 0
;
""")

cursor.execute("""
--sql
    UPDATE messages SET ignore = 1 WHERE (
        message LIKE '% the %' OR
        message LIKE '% if %' OR
        message LIKE '% of %' OR
        message LIKE '% and %' OR
        message LIKE '% that %' OR
        message LIKE '% have %' OR
        message LIKE '% not %' OR
        message LIKE '% his %' OR
        message LIKE '% from %' OR
        message LIKE '% they %' OR
        message LIKE '% we %' OR
        message LIKE '% will %' OR
        message LIKE '% my %' OR
        message LIKE '% would %' OR
        message LIKE '% there %' OR
        message LIKE '% which %' OR
        message LIKE '% when %' OR
        message LIKE '% make %' OR
        message LIKE '% can %' OR
        message LIKE '% just %' OR
        message LIKE '% know %' OR
        message LIKE '% some %' OR
        message LIKE '% other %' OR
        message LIKE '% only %' OR
        message LIKE '% look %'
    )
    AND ignore = 0
;
""")

