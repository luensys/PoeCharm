import requests
import json
import time
import csv
import re

URL = 'https://poe.game.daum.net/api/trade'
EN_URL = 'https://www.pathofexile.com/api/trade'
search_uri = '/search/Standard'
item_info_uri = '/data/items'
fetch_uri = '/fetch/'
orig_tr_dir = '../../PoeCharm/Pob/translate_kr'
gem_file = 'Items_Gems.txt.csv'
stat_description_file = 'statDescriptions.csv'
result_dir = '../../translator/translate_kr'

def get_request(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  return json.loads(res.text)

def post_request(url, json_data):
  res = requests.post(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, json=json_data)
  return json.loads(res.text)

def reshape(lst, n):
    return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

query_base = {"query":{"status":{"option":"online"},"stats":[{"type":"and","filters":[],"disabled":False}]},"sort":{"price":"asc"}}


gem_list = {}
desc_list = {}
with open(orig_tr_dir + '/' + gem_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    gem_list[row[0].strip()] = row[1].strip()

with open(orig_tr_dir + '/' + stat_description_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    desc_list[row[0]] = row[1]

# gem_list = {"Animate Weapon": "무기 기동"}

count = 1
for en_type, kr_type in gem_list.items():
  # 너무 많으면 오래 걸려서 끊어서 진행하려고 skip 관련 부분 추가
  if count > 100:
    count = count + 1
    continue
  print(kr_type)
  query = query_base.copy()
  query['query']['type'] = kr_type
  response = requests.post(URL + search_uri, json=query, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  result = json.loads(response.text)
  items = result['result']

  fetchs = reshape(items, 1)

  fetch = fetchs[0]
  en_info = get_request(EN_URL + fetch_uri + ','.join(fetch))
  kr_info = get_request(URL + fetch_uri + ','.join(fetch))
  
  # print(kr_info['result'][0]['item']['secDescrText'])
  # print(kr_info['result'][0]['item']['explicitMods'])
  # print(kr_info['result'][0]['item']['descrText'])
  # print(en_info['result'][0]['item']['secDescrText'])
  # print(en_info['result'][0]['item']['explicitMods'])
  # print(en_info['result'][0]['item']['descrText'])

  if 'result' in kr_info and 'item' in en_info['result'][0] and 'explicitMods' in en_info['result'][0]['item']:
    for idx in range(len(kr_info['result'][0]['item']['explicitMods'])):
      en_txt = re.sub(r'([0-9]+[.,]*)+', '{0}', en_info['result'][0]['item']['explicitMods'][idx])
      kr_txt = re.sub(r'([0-9]+[.,]*)+', '{0}', kr_info['result'][0]['item']['explicitMods'][idx])

      for key, val in desc_list.items():
        if(key.strip() == en_txt.strip()):
          desc_list[key] = kr_txt
  else:
    print('item not exists')

  time.sleep(15)
  count = count + 1

# 젬 정보 수정된 것 저장
with open(result_dir + '/' + stat_description_file, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in desc_list.items():
      spamwriter.writerow([key, val])