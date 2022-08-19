import requests
import json
from datetime import datetime

STATS_KO_URL = 'https://poe.game.daum.net/api/trade/data/stats'
STATS_EN_URL = 'https://www.pathofexile.com/api/trade/data/stats'

ITEMS_KO_URL = 'https://poe.game.daum.net/api/trade/data/items'
ITEMS_EN_URL = 'https://www.pathofexile.com/api/trade/data/items'

STATIC_KO_URL = 'https://poe.game.daum.net/api/trade/data/static'
STATIC_EN_URL = 'https://www.pathofexile.com/api/trade/data/static'

FilterKO = 'FiltersKO.txt'
FilterEN = 'FiltersEN.txt'

StaticKO = 'StaticKO.txt'
StaticEN = 'StaticEN.txt'

ItemsKO = 'ItemsKO.txt'
ItemsEN = 'ItemsEN.txt'

def get_request(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  return json.loads(res.text)

def write_txt(json_data, filename):
  json_string = json.dumps(json_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
  with open("../" + filename, "w") as file:
    file.write(json_string.decode())

def entries_remake(data):
  entries = []
  for index, value in enumerate(data):
    if 'id' in value:
      id = value['id']
    else:
      id = None
    if 'name' in value:
      name = value['name']
    else:
      name = None
    if 'part' in value:
      part = value['part']
    else:
      part = None
    if 'text' in value:
      text = value['text']
    else:
      text = None
    if 'type' in value:
      type_ = value['type']
    else:
      type_ = None
    entries.append({'id': id, 'name': name, 'part': part, 'text': text, 'type': type_})
  return entries

# Filter 정보 업데이트
kr_stats = get_request(STATS_KO_URL)
en_stats = get_request(STATS_EN_URL)

kr_stat_list = {}
en_stat_list = {}
kr_stat_list['result'] = []
en_stat_list['result'] = []

kr_info = {'유사' : 'pseudo', '무작위' : 'explicit', '고정': 'implicit', '분열된': 'fractured', '인챈트': 'enchant', '스컬지': 'scourge', '제작된': 'crafted', '장막': 'veiled', '몬스터': 'monster', '탐광': 'delve', '결전': 'ultimatum'}

# Filter 정보 업데이트
for idx, en_val in enumerate(en_stats['result']):
  # result 안의 배열 Pseudo, Explicit 등
  kr_val = kr_stats['result'][idx]
  label = kr_val['label']
  id = kr_info[label]
  del kr_stats['result'][idx]['label']
  del en_stats['result'][idx]['label']
  
  kr_entries = entries_remake(kr_val['entries']);
  en_entries = entries_remake(en_val['entries']);

  kr_stats['result'][idx]['entries'] = kr_entries
  en_stats['result'][idx]['entries'] = en_entries
  kr_stats['result'][idx]['id'] = kr_info[label]
  kr_stats['result'][idx]['label'] = label
  en_stats['result'][idx]['id'] = kr_info[label]
  en_stats['result'][idx]['label'] = label

now = datetime.now() # current date and time
date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
kr_stats['update'] = date_time
en_stats['update'] = date_time

write_txt(kr_stats, FilterKO)
write_txt(en_stats, FilterEN)


# Static 정보 업데이트
kr_statics = get_request(STATIC_KO_URL)
en_statics = get_request(STATIC_EN_URL)

for idx, en_val in enumerate(en_statics['result']):
  # result 안의 배열 Pseudo, Explicit 등
  kr_val = kr_statics['result'][idx]
  id = en_val['id']
  en_label = en_val['label']
  kr_label = kr_val['label']
  del kr_statics['result'][idx]['id']
  del en_statics['result'][idx]['id']
  del kr_statics['result'][idx]['label']
  del en_statics['result'][idx]['label']
  
  kr_entries = entries_remake(kr_val['entries']);
  en_entries = entries_remake(en_val['entries']);

  kr_statics['result'][idx]['entries'] = kr_entries
  en_statics['result'][idx]['entries'] = en_entries
  kr_statics['result'][idx]['id'] = id
  kr_statics['result'][idx]['label'] = kr_label
  en_statics['result'][idx]['id'] = id
  en_statics['result'][idx]['label'] = en_label

now = datetime.now() # current date and time
date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
kr_statics['update'] = date_time
en_statics['update'] = date_time

write_txt(kr_statics, StaticKO)
write_txt(en_statics, StaticEN)

# Items 정보 업데이트

kr_items = get_request(ITEMS_KO_URL)
en_items = get_request(ITEMS_EN_URL)

for idx, en_val in enumerate(en_items['result']):
  # result 안의 배열 Pseudo, Explicit 등
  kr_val = kr_items['result'][idx]
  id = en_val['id']
  en_label = en_val['label']
  kr_label = kr_val['label']
  del kr_items['result'][idx]['id']
  del en_items['result'][idx]['id']
  del kr_items['result'][idx]['label']
  del en_items['result'][idx]['label']
  
  kr_entries = entries_remake(kr_val['entries']);
  en_entries = entries_remake(en_val['entries']);

  kr_items['result'][idx]['entries'] = kr_entries
  en_items['result'][idx]['entries'] = en_entries
  kr_items['result'][idx]['id'] = id
  kr_items['result'][idx]['label'] = kr_label
  en_items['result'][idx]['id'] = id
  en_items['result'][idx]['label'] = en_label

now = datetime.now() # current date and time
date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
kr_items['update'] = date_time
en_items['update'] = date_time

write_txt(kr_items, ItemsKO)
write_txt(en_items, ItemsEN)