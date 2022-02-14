#-*- coding: utf-8 -*-
import csv
import os

etc_file = '../etcs.csv'

tr_kr = {}
tr_kr_key = {}
with open(etc_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_kr[row[0].strip()] = row[1]
    tr_kr_key[row[0].strip().upper()] = row[0]

with open('../etcs_new.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])
