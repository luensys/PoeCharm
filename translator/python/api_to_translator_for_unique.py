#-*- coding: utf-8 -*-
import csv

api_dir = '../../api'
api_file = 'unique_from_api.csv'

kr_dir = '../../PoeCharm/Pob/translate_kr'
tr_file = 'Uniques.txt.csv'

result_dir = '../translate_kr'

api_list = {}
tr_list = {}
with open(api_dir + '/' + api_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    api_list[row[0].strip()] = row[1].strip()

with open(kr_dir + '/' + tr_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_list[row[0].strip()] = row[1].strip()

for key, val in api_list.items():
  tr_list[key] = api_list[key]


# name 정보 수정된 것 저장
with open(result_dir + '/' + tr_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tr_list.items():
      spamwriter.writerow([key, val])
    