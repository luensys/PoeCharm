# loading in modules
import sqlite3
import os
import csv

result_dir = '../translate_kr'
kr_dir = '../../PoeCharm/Pob/translate_kr'
kr_list = os.listdir(kr_dir)

result_dir = '../translate_kr'
tr_kr_orig = 'translate_kr.csv'
mac_file = '.DS_Store'

if(os.path.isdir(result_dir) != True):
  os.makedirs(result_dir)

###########################################################
# DB read

# get db file path
dbfile = '../resources.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
result = [a for a in cur.execute("SELECT value FROM config WHERE name = 'translate_tab_name'")]
table_name = result[0][0]

result = [a for a in cur.execute("SELECT k, v, source FROM " + table_name)]
db_data = {}
tr_file_names = []

for data in result:
  if data[2] not in tr_file_names:
    tr_file_names.append(data[2])
  if data[2] not in db_data.keys():
    db_data[data[2]] = {}
  db_data[data[2]][data[0]] = data[1]

###########################################################
# File Names Read

for key1 in tr_file_names:
  with open(result_dir + '/' + key1 + '.csv', 'w', newline='', encoding='utf8') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in db_data[key1].items():
        spamwriter.writerow([key, val])

# Be sure to close the connection
con.close()