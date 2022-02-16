import requests
import json
import csv

URL = 'https://poe.game.daum.net/api/trade/data/items'
EN_URL = 'https://www.pathofexile.com/api/trade/data/items'

def get_request(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
  return json.loads(res.text)

translate = {}

kr_items = get_request(URL)
en_items = get_request(EN_URL)

count = 0
for idx, en_item in enumerate(en_items['result']):
  kr_item = kr_items['result'][idx]
  for key in en_item.keys():
    if(isinstance(en_item[key], list) == True):
      pass
    else:
      if(key == 'id'):
        pass
      else:
        translate[en_item[key]] = kr_item[key]
  if(en_item["id"] != kr_item["id"]):
    print(en_item["id"], kr_item["id"])
  for idx1, en_val1 in enumerate(en_item['entries']):
    try:
      val1 = kr_item['entries'][idx1]
      for key2 in en_val1.keys():
        if(isinstance(en_val1[key2], list) == True):
          pass
        else:
          if(isinstance(en_val1[key2], dict) == True):
            pass
          else:
            if 'flags' in en_val1:
              if((key2 == 'name') | (key2 == 'text')):
                print(en_val1[key2], val1[key2])
                translate[en_val1[key2]] = val1[key2] + '(' + en_val1[key2] + ')'
              else:
                translate[en_val1[key2]] = val1[key2]
            else:
              translate[en_val1[key2]] = val1[key2]
        if(key2 == 'flags'):
          if(val1[key2]["unique"] != en_val1[key2]["unique"]):
            print(val1, en_val1)
    except IndexError:
      print(idx1, en_val1)
  count += 1

print(count)

with open('../item_from_api.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in translate.items():
      spamwriter.writerow([key, val])