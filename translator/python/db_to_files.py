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

# creating file path
dbfile = '../../resources.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
result = [a for a in cur.execute("SELECT value FROM config WHERE name = 'translate_tab_name'")]
table_name = result[0][0]

result = [a for a in cur.execute("SELECT k, v, source FROM " + table_name)]
db_data = {}

for data in result:
  if (data[2] == 'treenode_name'):
    continue
  if (data[2] == 'treenode_optinon'):
    continue
  if (data[2] == 'Items_data'):
    continue
  if data[2] not in db_data.keys():
    db_data[data[2]] = {}
  db_data[data[2]][data[0]] = data[1]

###########################################################
# File Names Read
tr_data = {}
tr_file_names = {}

for f in kr_list:
  with open((kr_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    if(f == tr_kr_orig):
      continue
    if(f == mac_file):
      continue
    tr_data[f.split('.')[0]] = {}
    tr_file_names[f.split('.')[0]] = f

for key1 in db_data:
  with open(result_dir + '/' + tr_file_names[key1], 'w', encoding='utf8') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in db_data[key1].items():
        spamwriter.writerow([key, val])

# Be sure to close the connection
con.close()