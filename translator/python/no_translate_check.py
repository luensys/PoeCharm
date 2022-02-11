import csv

# 
f = open('../../PoeCharm/Pob/translate_cn.csv', 'r')
rdr = csv.reader(f)
tr_cn = []
for line in rdr:
  tr_cn.append(line)
f.close()

# 
f = open('../../PoeCharm/Pob/translate_kr.csv', 'r')
rdr = csv.reader(f)
tr_kr = []

for line in rdr:
  tr_kr.append(line)
f.close()

# 
for idx, line in enumerate(tr_kr):
  if(line[0] == line[1]):
    del tr_kr[idx]

with open('test.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in tr_kr:
      spamwriter.writerow(['\"'+line[0]+'\"', '\"'+line[1]+'\"'])

count = 0
for line in tr_kr:
  count += 1

print(count)
