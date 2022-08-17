import requests
import json
import csv
import re
import more_itertools as mit

URL = 'https://poe.game.daum.net/api/trade/data/stats'
EN_URL = 'https://www.pathofexile.com/api/trade/data/stats'

orig_tr_dir = '../../PoeCharm/Pob/translate_kr'
stat_description_file = 'statDescriptions.csv'
etc_file = 'etcs.csv'
result_dir = '../../translator/translate_kr'

def get_request(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  return json.loads(res.text)

def repl(m):
  return next(repl.v)
repl.v=mit.seekable(('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'))

desc_list = {}
etc_list = {}
with open(orig_tr_dir + '/' + stat_description_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    desc_list[row[0]] = row[1]

en_stat = {}
kr_stat = {}

kr_stats = get_request(URL)
en_stats = get_request(EN_URL)

en_stat_list = {}
kr_stat_list = {}

kr_info = {'유사' : 'Pseudo', '무작위' : 'Explicit', '고정': 'Implicit', '분열된': 'Fractured', '인챈트': 'Enchant', '스컬지': 'Scourge', '제작된': 'Crafted', '장막': 'Veiled', '몬스터': 'Monster', '탐광': 'Delve', '결전': 'Ultimatum'}
for idx, en_val in enumerate(en_stats['result']):
  kr_val = kr_stats['result'][idx]
  # PoB에 필요한 데이터만 사용
  if (en_val['label'] != 'Pseudo'):
    en_stat_list[en_val['label']] = {}
    kr_stat_list[kr_info[kr_val['label']]] = {}
    for idx1, en_val1 in enumerate(en_val['entries']):
      # idx1 : 순서, en_val1 : 영문 아이템 정보
      # print(en_val['label'], en_val1['id'], en_val1['text'])
      # print(kr_info[kr_val['label']], kr_val['entries'][idx1]['id'], kr_val['entries'][idx1]['text'])
      en_stat_list[en_val['label']][en_val1['id']] = en_val1['text']
      kr_stat_list[kr_info[kr_val['label']]][kr_val['entries'][idx1]['id']] = kr_val['entries'][idx1]['text']
# print(en_stat_list)
# print(kr_stat_list)

for key, en_val in en_stat_list.items():
  for key1, en_val1 in en_val.items():
    en_txt = re.sub('(#)', repl, en_val1)
    repl.v.seek(0)
    kr_txt = re.sub('(#)', repl, kr_stat_list[key][key1])
    repl.v.seek(0)
    # print(en_txt)
    # print(kr_txt)
        
    exists = 0
    for key2, val in desc_list.items():
      if(key2.strip() == en_txt.strip()):
        desc_list[key2] = kr_txt
        exists = 1
        
    if(exists == 0) :
      etc_list[en_txt.strip()] = kr_txt


with open(result_dir + '/' + stat_description_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in desc_list.items():
      spamwriter.writerow([key, val])
with open(result_dir + '/' + etc_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_list.items():
      spamwriter.writerow([key, val])