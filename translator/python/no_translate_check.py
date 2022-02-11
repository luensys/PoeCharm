import csv

# 
f = open('../../PoeCharm/Pob/translate_cn.csv', 'r')
rdr = csv.reader(f)
tr_cn = []
for line in rdr:
  tr_cn.append(line)
f.close()

# 
f = open('../translate____.tsv', 'r')
rdr = csv.reader(f, delimiter='	')
tr_kr = []

for line in rdr:
  tr_kr.append(line)
f.close()

# 
for idx, line in enumerate(tr_kr):
  if(line[0] == line[1]):
    del tr_kr[idx]

with open('../translate_kr_.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for line in tr_kr:
      spamwriter.writerow(line)

with open('../spread_upload.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for line in tr_kr:
      spamwriter.writerow(line)

count = 0
for line in tr_kr:
  count += 1

print(count)
