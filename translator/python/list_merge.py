#-*- coding: utf-8 -*-
import csv
import os

cn_dir = '../../PoeCharm/Pob/translate_cn'
kr_dir = '../../PoeCharm/Pob/translate_kr'
cn_list = os.listdir(cn_dir)
kr_list = os.listdir(kr_dir)

result_dir = '../translate_kr'
tr_kr_orig = 'translate_kr.csv'
mac_file = '.DS_Store'
tr_kr_dir = '../../PoeCharm/Pob/translate_kr'
temp_file = 'Uniques.txt.csv'

if(os.path.isdir(result_dir) != True):
  os.makedirs(result_dir)

# get kr all key and values
tr_kr = {}
etc_kr = {}
need_kr = {}
check = {}
completed = {}
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
          etc_kr_key[row[0].strip().upper()] = row[0]
          etc_kr[row[0].strip()] = row[1]
  
with open('../etcs_start.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_kr.items():
      spamwriter.writerow([key, val])
  
with open('../tr_start.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tr_kr.items():
      spamwriter.writerow([key, val])

# compare with cn csv list
for f in cn_list:
  new_kr = {}
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
        del etc_kr[tr_kr_key[key].strip()]
        new_kr[tr_cn_key[key]] = tr_kr[tr_kr_key[key].strip()]
        completed[tr_cn_key[key]] = tr_kr[tr_kr_key[key].strip()]
        if(tr_kr_key[key].strip().upper() == tr_kr[tr_kr_key[key].strip()].strip().upper()):
          need_kr[tr_cn_key[key]] = ''
          check[tr_cn_key[key]] = tr_kr[tr_kr_key[key].strip()]
          if(f == temp_file):
            temp[tr_cn_key[key]] = ''
    except KeyError:
      need_kr[tr_cn_key[key]] = ''
      new_kr[tr_cn_key[key]] = tr_cn_key[key].strip()
      if(f == temp_file):
        temp[tr_cn_key[key]] = ''

  with open(result_dir + '/' + f, 'w') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in new_kr.items():
        spamwriter.writerow([key, val])
  
with open(result_dir + '/etcs.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_kr.items():
      spamwriter.writerow([key, val])

# speadsheet에 번역 완료로 올리기 위한 포맷으로 저장
with open('../completed.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in completed.items():
      spamwriter.writerow([key, val])

# speadsheet에 사용되지 않음으로 올리기 위한 포맷으로 저장
with open('../non_use.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in etc_kr.items():
      spamwriter.writerow([key, val])

# 번역이 필요한 데이타 저장
with open('../need_translate.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in need_kr.items():
      spamwriter.writerow([key, val])
  
# 혹시 실수 한 것이 있을 수 있으므로 체크할 것에 대한 정보 저장
with open('../check.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in check.items():
      spamwriter.writerow([key, val])


# 특정 파일 타겟으로 필요한 번역 정리
with open('../temp.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='	')
    for key, val in temp.items():
      spamwriter.writerow([key, val])