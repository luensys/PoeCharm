#-*- coding: utf-8 -*-
import csv
import os

cn_dir = '../../PoeCharm/Pob/translate_cn'
kr_dir = '../../PoeCharm/Pob/translate_kr'
cn_list = os.listdir(cn_dir)
kr_list = os.listdir(kr_dir)

result_dir = '../translate_kr'
tr_kr_orig = 'translate_kr.csv'
tr_kr_dir = '../../PoeCharm/Pob/translate_kr'

if(os.path.isdir(result_dir) != True):
  os.makedirs(result_dir)

# get kr all key and values
tr_kr = {}
etc_kr = {}
tr_kr_key = {}
for f in kr_list:
  with open((kr_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    if(f == tr_kr_orig):
      continue
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      tr_kr[row[0].strip()] = row[1]
      etc_kr[row[0].strip()] = row[1]
      tr_kr_key[row[0].strip().upper()] = row[0]

# compare with cn csv list
for f in cn_list:
  new_kr = {}
  need_kr = {}
  tr_cn = {}
  tr_cn_key = {}
  with open((cn_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      tr_cn[row[0].strip()] = row[1]
      tr_cn_key[row[0].strip().upper()] = row[0]
  
  for key, val in tr_cn_key.items():
    try:
      if(tr_cn_key[key].strip().upper() == tr_kr_key[key].strip().upper()):
        new_kr[tr_cn_key[key]] = tr_kr[tr_kr_key[key].strip()]
        del etc_kr[tr_kr_key[key].strip()]
    except KeyError:
      need_kr[tr_cn_key[key]] = ''
      new_kr[tr_cn_key[key]] = tr_cn_key[key].strip()

  with open(result_dir + '/' + f, 'w') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in new_kr.items():
        spamwriter.writerow([key, val])
  
with open(result_dir + '/etcs.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_kr.items():
      spamwriter.writerow([key, val])
  
with open(result_dir + '/en.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in need_kr.items():
      spamwriter.writerow([key, key])
  
with open('../need.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in need_kr.items():
      spamwriter.writerow([key, val])

