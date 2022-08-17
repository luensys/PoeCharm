import csv
import string

tr_kr_key = {}
tr_kr = {}
with open('../translate_kr_.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_kr_key[row[0].strip().upper()] = row[0].strip()
    tr_kr[row[0].strip()] = row[1].strip()

tr_cn_key = {}
with open('../../PoeCharm/Pob/translate_cn.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_cn_key[row[0].strip().upper()] = row[0].strip()

for key, val in tr_cn_key.items():
  try:
    if(tr_kr_key[key].upper() == tr_cn_key[key].upper()):
      if(tr_kr_key[key] != tr_cn_key[key]):
        tr_kr[tr_cn_key[key]] = tr_kr[tr_kr_key[key]]
        del tr_kr[tr_kr_key[key]]
  except KeyError:
    pass

with open('../spread_upload.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])

with open('../translate_kr.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])