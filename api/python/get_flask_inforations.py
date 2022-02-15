import requests
import json
import time
import csv

URL = 'https://poe.game.daum.net/api/trade'
EN_URL = 'https://www.pathofexile.com/api/trade'
search_uri = '/search/Archnemesis'
item_info_uri = '/data/items'
fetch_uri = '/fetch/'
flask_file = '../../PoeCharm/Pob/translate_kr/Flask_tag.csv'
result_file = '../Flask_tag.csv'

def get_request(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  return json.loads(res.text)

def post_request(url, json_data):
  res = requests.post(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, json=json_data)
  return json.loads(res.text)

def reshape(lst, n):
    return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

# query = {"query":{"status":{"option":"online"},"type":"루비 플라스크","stats":[{"type":"and","filters":[],"disabled":False}],"filters":{"type_filters":{"filters":{"rarity":{"option":"magic"}},"disabled":False}}},"sort":{"price":"asc"}}
query_base = {"query":{"status":{"option":"online"},"stats":[{"type":"and","filters":[],"disabled":False}],"filters":{"type_filters":{"filters":{"rarity":{"option":"magic"}},"disabled":False}}},"sort":{"price":"asc"}}
kr_types = ["루비 플라스크", "사파이어 플라스크", "토파즈 플라스크", "화강암 플라스크", "수은 플라스크", "자수정 플라스크", "석영 플라스크", "비취 플라스크"]

tags = {}
with open(flask_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tags[row[0].strip()] = row[1].strip()

for kr_type in kr_types:
  query = query_base.copy()
  query['query']['type'] = kr_type
  response = requests.post(URL + search_uri, json=query, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  result = json.loads(response.text)
  items = result['result']

  fetchs = reshape(items, 10)

  for fetch in fetchs:
    en_info = get_request(EN_URL + fetch_uri + ','.join(fetch))
    kr_info = get_request(URL + fetch_uri + ','.join(fetch))
    for idx, item in enumerate(en_info['result']):
      try:
        en_explicit = item['item']['extended']['mods']['explicit']
        kr_explicit = kr_info['result'][idx]['item']['extended']['mods']['explicit']
        for index, explicit in enumerate(en_explicit):
          tags[explicit['name']] = kr_explicit[index]['name']
      except KeyError:
        pass
    time.sleep(30)
    
  with open('../Flask_tag.csv', 'w') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in tags.items():
        spamwriter.writerow([key, val])