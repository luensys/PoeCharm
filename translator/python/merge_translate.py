import csv
import string

translated = {}
with open('../translated.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile, delimiter='	')
  for row in read_csv:
    translated[row[0].strip()] = row[1].strip()

non_translated = {}
did_translated = {}
with open('../non_translated.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile, delimiter='	')
  for row in read_csv:
    if(row[1].strip() == ''):
      non_translated[row[0].strip()] = row[1].strip()
    else:
      did_translated[row[0].strip()] = row[1].strip()

tr_kr = {}
with open('../../PoeCharm/Pob/translate_kr.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_kr[row[0].strip()] = row[1].strip()

tr_cn = {}
with open('../../PoeCharm/Pob/translate_cn.csv', 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_cn[row[0].strip()] = row[1].strip()

diff = []
for key, val in tr_kr.items():
  if(tr_kr[key] != translated[key]):
      tr_kr[key] = translated[key]
      diff.append([key, val, translated[key]])

with open('../merged.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])


for key, val in did_translated.items():
  tr_kr[key] = val

for key, val in tr_kr.items():
  del tr_cn[key]

for key, val in tr_cn.items():
  tr_cn[key] = ''

with open('../diff_translate_kr.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for line in diff:
      spamwriter.writerow(line)

with open('../merged_kr.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])

with open('../need_translate.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in tr_cn.items():
      spamwriter.writerow([key, val])



with open('../translate_kr.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])