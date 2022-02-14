#-*- coding: utf-8 -*-
import csv

# 
tr_kr = {}
tr_kr_key = {}
with open('./translate_kr_orig.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile, delimiter='	')
  for row in read_csv:
    tr_kr_key[row[0].strip()] = row[0].strip()
    tr_kr[row[0].strip()] = row[1].strip()
    
non_tr = {}
non_check = {}
for key, val in tr_kr_key.items():
  if(tr_kr_key[key].upper() == tr_kr[key].upper()):
    non_tr[tr_kr_key[key]] = ''
    non_check[tr_kr_key[key]] = ''
    del tr_kr[tr_kr_key[key]]

with open('../translated.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])

with open('../non_translated.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in non_tr.items():
      spamwriter.writerow([key, val])

with open('../non_translated_check.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in non_check.items():
      spamwriter.writerow([key, val])

with open('../translate_kr_.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])

count = 0
for line in tr_kr:
  count += 1

print(count)
