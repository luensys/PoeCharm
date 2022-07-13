#-*- coding: utf-8 -*-
import csv
import os

tr_kr_orig = 'translate_kr.csv'
mac_file = '.DS_Store'
temp_file = 'statDescriptions.csv'
result_dir = '../translate_kr'

poecharm_tr_dir = '../translate_kr'
poecharm_tr_list = os.listdir(poecharm_tr_dir)

kr_dir = '../../PoeCharm/Pob/translate_kr'
kr_list = os.listdir(kr_dir)

# get poe translated all key and values
tr_kr = {}
etc_kr = {}
need_kr = {}
check = {}
completed = {}
tr_kr_key = {}
etc_kr_key = {}
temp = {}
for f in poecharm_tr_list:
  with open((poecharm_tr_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    if(f == tr_kr_orig):
      continue
    if(f == mac_file):
      continue
    if(f == temp_file):
      continue
    read_csv = csv.reader(csvfile, delimiter='\t')
    for row in read_csv:
      if(row[0].strip().upper() != row[1].strip().upper()):
        tr_kr[row[0].strip()] = row[1]
        tr_kr_key[row[0].strip().upper()] = row[0]
        etc_kr_key[row[0].strip().upper()] = row[0]
        etc_kr[row[0].strip()] = row[1]

# compare with kr csv list
for f in kr_list:
  new_kr = {}
  orig_kr = {}
  orig_kr_key = {}
  with open((kr_dir + '/' + f), 'r', encoding='utf8') as csvfile:
    if(f == tr_kr_orig):
      continue
    if(f == mac_file):
      continue
    if(f == temp_file):
      continue
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      orig_kr[row[0].strip()] = row[1]
      orig_kr_key[row[0].strip().upper()] = row[0]
  
  for key, val in orig_kr_key.items():
    try:
      if(orig_kr_key[key].strip().upper() == tr_kr_key[key].strip().upper()):
        del etc_kr[tr_kr_key[key].strip()]
        new_kr[orig_kr_key[key]] = tr_kr[tr_kr_key[key].strip()]
        completed[orig_kr_key[key]] = tr_kr[tr_kr_key[key].strip()]
        if(tr_kr_key[key].strip().upper() == tr_kr[tr_kr_key[key].strip()].strip().upper()):
          need_kr[orig_kr_key[key]] = ''
          check[orig_kr_key[key]] = tr_kr[tr_kr_key[key].strip()]
          if(f == temp_file):
            temp[orig_kr_key[key]] = ''
    except KeyError:
      need_kr[orig_kr_key[key]] = ''
      new_kr[orig_kr_key[key]] = orig_kr_key[key].strip()
      if(f == temp_file):
        temp[orig_kr_key[key]] = ''

  with open(result_dir + '/' + f, 'w') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in new_kr.items():
        spamwriter.writerow([key, val])