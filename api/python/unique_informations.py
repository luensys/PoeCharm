import requests
import json
import time
import csv
import re
import more_itertools as mit
import cloudscraper

URL = 'https://poe.game.daum.net/api/trade'
EN_URL = 'https://www.pathofexile.com/api/trade'
search_uri = '/search/Sanctum'
# search_uri = '/search/Standard'
item_info_uri = '/data/items'
fetch_uri = '/fetch/'
orig_tr_dir = '../../PoeCharm/Pob/translate_kr'
unique_file = 'Uniques.txt.csv'
stat_description_file = 'statDescriptions.csv'
etcs_file = 'etcs.csv'
temp_file = 'temp.csv'
result_dir = '../../translator/translate_kr'

def get_request_kr(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, verify=False)
  return json.loads(res.text)

def get_request_en(url):
  scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
  res = scraper.get(url)
  return json.loads(res.text)

def post_request(url, json_data):
  scraper = cloudscraper.create_scraper(delay=15,   browser={'custom': 'ScraperBot/1.0',})
  res = scraper.post(url, json=json_data)
  return json.loads(res.text)

def reshape(lst, n):
  return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

def repl(m):
  return next(repl.v)
repl.v=mit.seekable(('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'))

# https://poe-query.vercel.app/ 참조
query_base = {"query":{"status":{"option":"any"},"stats":[{"type":"and","filters":[],"disabled":False}]},"sort":{"price":"asc"}}

unique_list = {}
desc_list = {}
etcs_list = {}
etc_list = {}
with open(orig_tr_dir + '/' + unique_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    unique_list[row[0].strip()] = row[1].strip()

with open(orig_tr_dir + '/' + stat_description_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    desc_list[row[0]] = row[1]

with open(orig_tr_dir + '/' + etcs_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    etcs_list[row[0]] = row[1]

# unique_list = {"Animate Weapon": "무기 기동"}

count = 0
for en_type, kr_type in unique_list.items():
  # 마지막에 놓을 경우 continue 될 때 카운트가 올라가지 않아 제일 앞으로 옮김
  count = count + 1
  # 너무 많으면 오래 걸려서 끊어서 진행하려고 skip 관련 부분 추가
  # if count > 20:
  #   continue
  print(str(count) + ' / ' + str(len(unique_list)))
  print(kr_type)
  
  query = query_base.copy()
  query['query']['term'] = en_type
  result = post_request(EN_URL + search_uri, json_data=query)
  if not 'result' in result:
    print('is not response for sale')
    continue
  items = result['result']

  fetchs = reshape(items, 1)

  if len(fetchs) < 1:
    print('is not for sale')
    # 확인 완료 후 무조건 15초 딜레이
    time.sleep(15)
    continue
  fetch = fetchs[0]
  en_info = get_request_en(EN_URL + fetch_uri + ','.join(fetch))
  kr_info = get_request_kr(URL + fetch_uri + ','.join(fetch))
  # print(en_info)
  # print(kr_info)

  if 'result' in kr_info and 'item' in en_info['result'][0]:
    if 'implicitMods' in en_info['result'][0]['item']:
      print(en_info['result'][0]['item']['implicitMods'])
      print(kr_info['result'][0]['item']['implicitMods'])
      for idx in range(len(kr_info['result'][0]['item']['implicitMods'])):
        en_txt = re.sub('[+-]?(?=\d)(\d*\.?\d*)', repl, en_info['result'][0]['item']['implicitMods'][idx])
        repl.v.seek(0)
        kr_txt = re.sub('[+-]?(?=\d)(\d*\.?\d*)', repl, kr_info['result'][0]['item']['implicitMods'][idx])
        repl.v.seek(0)

        exists = 0
        for key, val in desc_list.items():
          if(key.strip() == en_txt.strip()):
            desc_list[key] = kr_txt
            exists = 1
        for key, val in etcs_list.items():
          if(key.strip() == en_txt.strip()):
            etcs_list[key] = kr_txt
            exists = 1

        if(exists == 0) :
          etc_list[en_txt.strip()] = kr_txt

    if 'explicitMods' in en_info['result'][0]['item']:
      print(en_info['result'][0]['item']['explicitMods'])
      print(kr_info['result'][0]['item']['explicitMods'])
      for idx in range(len(kr_info['result'][0]['item']['explicitMods'])):
        en_txt = re.sub('(?=\d)(\d*\.?\d*)', repl, en_info['result'][0]['item']['explicitMods'][idx])
        repl.v.seek(0)
        kr_txt = re.sub('(?=\d)(\d*\.?\d*)', repl, kr_info['result'][0]['item']['explicitMods'][idx])
        repl.v.seek(0)
        # print(en_txt)
        # print(kr_txt)
        
        exists = 0
        for key, val in desc_list.items():
          if(key.strip() == en_txt.strip()):
            desc_list[key] = kr_txt
            exists = 1
        for key, val in etcs_list.items():
          if(key.strip() == en_txt.strip()):
            etcs_list[key] = kr_txt
            exists = 1
            
        if(exists == 0) :
          etc_list[en_txt.strip()] = kr_txt

  else:
    print('item not exists')
  
  # count 수에 따라 한 번씩 저장 함
  if ((count % 10) == 0):
    # 유니크 정보 수정된 것 저장
    with open(result_dir + '/' + stat_description_file, 'w', encoding='utf8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
        for key, val in desc_list.items():
          spamwriter.writerow([key, val])
    with open(result_dir + '/' + etcs_file, 'w', encoding='utf8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
        for key, val in etcs_list.items():
          spamwriter.writerow([key, val])
    with open(result_dir + '/' + temp_file, 'w', encoding='utf8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
        for key, val in etc_list.items():
          spamwriter.writerow([key, val])
    print(count, 'file saved')

  # 확인 완료 후 무조건 15초 딜레이
  time.sleep(15)

# 유니크 정보 수정된 것 저장
with open(result_dir + '/' + stat_description_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in desc_list.items():
      spamwriter.writerow([key, val])
with open(result_dir + '/' + etcs_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etcs_list.items():
      spamwriter.writerow([key, val])
with open(result_dir + '/' + temp_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in etc_list.items():
      spamwriter.writerow([key, val])