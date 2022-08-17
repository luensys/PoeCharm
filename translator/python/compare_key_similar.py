#-*- coding: utf-8 -*-
import csv
import os
from difflib import SequenceMatcher

cn_dir = '../../PoeCharm/Pob/translate_cn'
kr_dir = '../../PoeCharm/Pob/translate_kr'
cn_list = os.listdir(cn_dir)
kr_list = os.listdir(kr_dir)

result_dir = '../translate_kr'
tr_kr_orig = 'translate_kr.csv'
mac_file = '.DS_Store'
tr_kr_dir = '../../PoeCharm/Pob/translate_kr'
temp_file = 'Uniques.txt.csv'

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if(os.path.isdir(result_dir) != True):
  os.makedirs(result_dir)

# get kr all key and values
tr_kr = {}
etc_kr = {}
tr_kr_key = {}
etc_kr_key = {}
temp = {}
for f in kr_list:
  with open((kr_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    if(f == tr_kr_orig):
      continue
    if(f == mac_file):
      continue
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      if(row[0].strip().upper() != row[1].strip().upper()):
        if row[0].strip().upper() in tr_kr_key:
          continue
        else:
          tr_kr[row[0].strip()] = row[1]
          tr_kr_key[row[0].strip().upper()] = row[0]

with open((kr_dir + '/etcs.csv'), 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    if(row[0].strip().upper() != row[1].strip().upper()):
      etc_kr_key[row[0].strip().upper()] = row[0]
      etc_kr[row[0].strip()] = row[1]
    
# get cn all key and values
tr_cn = {}
etc_cn = {}
tr_cn_key = {}
etc_cn_key = {}
temp = {}
for f in cn_list:
  with open((cn_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    if(f == mac_file):
      continue
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      if(row[0].strip().upper() != row[1].strip().upper()):
        if row[0].strip().upper() in tr_cn_key:
          continue
        else:
          tr_cn[row[0].strip()] = row[1]
          tr_cn_key[row[0].strip().upper()] = row[0]
          etc_cn_key[row[0].strip().upper()] = row[0]
          etc_cn[row[0].strip()] = row[1]
   
# 동일 키 값은 우선 삭제
for upper_key, cn_key in etc_cn_key.items():
  try:
    if(cn_key.strip().upper() == tr_kr_key[upper_key].strip().upper()):
      del tr_cn_key[upper_key]
  except KeyError:
    pass

count = 0
similar_text = {}
print(len(tr_cn_key), len(etc_kr_key))
for upper_key, cn_key in tr_cn_key.items():
  count += 1
  for kr_upper_key, kr_key in etc_kr_key.items():
    try:
      compare = similar(tr_cn_key[upper_key].strip().upper(), tr_kr_key[kr_upper_key].strip().upper())
      if((compare > 0.8) & (compare < 1.0)):
        print(similar(tr_cn_key[upper_key], tr_kr_key[kr_upper_key]))
        print(tr_cn_key[upper_key], tr_kr_key[kr_upper_key], tr_kr[kr_key.strip()])
        similar_text[tr_kr_key[kr_upper_key]] = [tr_cn_key[upper_key], tr_kr[kr_key.strip()]]
    except KeyError:
      pass
  print(str(count) + ' of ' + str(len(tr_cn_key)) + ' text was compared')

with open('../similar.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in similar_text.items():
      spamwriter.writerow([key, val[0], val[1]])