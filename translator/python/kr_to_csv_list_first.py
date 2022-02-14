#-*- coding: utf-8 -*-
import csv
import os

path_dir = '../../PoeCharm/Pob/translate_cn'
f_list = os.listdir(path_dir)

result_dir = '../translate_kr'
tr_kr_orig = '../../PoeCharm/Pob/translate_kr/translate_kr.csv'
tr_kr_dir = '../../PoeCharm/Pob/translate_kr'
tr_kr_etc = '../../PoeCharm/Pob/translate_kr/etcs.csv'

tr_kr = {}
etc_kr = {}
tr_kr_key = {}
with open(tr_kr_orig, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_kr[row[0].strip()] = row[1]
    etc_kr[row[0].strip()] = row[1]
    tr_kr_key[row[0].strip().upper()] = row[0]

for f in f_list:
  new_kr = {}
  need_kr = {}
  tr_cn = {}
  tr_cn_key = {}
  with open((path_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      tr_cn[row[0].strip()] = row[1]
      tr_cn_key[row[0].strip().upper()] = row[0]
  
  for key, val in tr_cn_key.items():
    try:
      if(tr_cn_key[key].strip().upper() == tr_kr_key[key].strip().upper()):
        if(tr_kr_key[key].strip().upper() != tr_kr[tr_kr_key[key].strip()].strip().upper()):
          new_kr[tr_cn_key[key]] = tr_kr[tr_kr_key[key].strip()]
          del etc_kr[tr_kr_key[key].strip()]
    except KeyError:
      need_kr[tr_cn_key[key]] = ''
      pass

  with open(result_dir + '/' + f, 'w') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in new_kr.items():
        spamwriter.writerow([key, val])
  
with open(result_dir + '/etcs.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_kr.items():
      spamwriter.writerow([key, val])

with open(result_dir + '/no_tr.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_kr.items():
      spamwriter.writerow([key, key])
  
with open('../need.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in need_kr.items():
      spamwriter.writerow([key, val])

