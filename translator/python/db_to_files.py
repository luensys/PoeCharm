# loading in modules
import sqlite3

# creating file path
dbfile = '../../resources.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
table_list = [a for a in cur.execute("SELECT value FROM config WHERE name = 'translate_tab_name'")]
# here is you table list
print(table_list[0][0])

# Be sure to close the connection
con.close()