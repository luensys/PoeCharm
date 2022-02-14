#-*- coding: utf-8 -*-
import csv

tr_kr_key = {}
tr_kr = {}
with open('../../PoeCharm/Pob/translate_kr.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_kr_key[row[0].strip().upper()] = row[0].strip()
    tr_kr[row[0].strip()] = row[1].strip()

tr_cn_key = {}
with open('../../PoeCharm/Pob/translate_cn.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_cn_key[row[0].strip().upper()] = row[0].strip()

add_trans = {}
for key, val in tr_cn_key.items():
  try:
    if(tr_kr_key[key].upper() == tr_cn_key[key].upper()):
      pass
  except KeyError:
    add_trans[tr_cn_key[key]] = ''

remove_trans = {}
for key, val in tr_kr_key.items():
  try:
    if(tr_kr_key[key].upper() == tr_cn_key[key].upper()):
      pass
  except KeyError:
    remove_trans[tr_kr_key[key]] = tr_kr[tr_kr_key[key]]

with open('../add_translate_from_cn.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in add_trans.items():
      spamwriter.writerow([key, val])

with open('../no_more_translate.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in remove_trans.items():
      spamwriter.writerow([key, val])