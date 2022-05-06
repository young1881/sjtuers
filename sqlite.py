import sqlite3 
con = sqlite3.connect('db.sqlite3')
def sql_fetch(con):
    cursorObj = con.cursor()
    # cursorObj.execute('DELETE FROM django_migrations WHERE id = 19')
    cursorObj.execute('SELECT * from Site')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
sql_fetch(con)