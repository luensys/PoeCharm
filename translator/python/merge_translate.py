import csv

translated = {}
with open('../translated.csv') as csvfile:
  read_csv = csv.reader(csvfile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
  for row in read_csv:
    translated[row[0]] = row[1]

tr_kr = {}
with open('../../PoeCharm/Pob/translate_kr.csv') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tr_kr[row[0]] = row[1]

diff = []
for key, val in tr_kr.items():
  if(tr_kr[key] != translated[key]):
      tr_kr[key] = translated[key]
      diff.append([key, val, translated[key]])

with open('../merged.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for line in tr_kr:
      spamwriter.writerow(line)

with open('../diff_translate_kr.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for line in diff:
      print(line)
      spamwriter.writerow(line)