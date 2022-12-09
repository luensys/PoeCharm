import requests
import json
import csv
import cloudscraper

URL = 'https://poe.game.daum.net/api/trade/data/items'
EN_URL = 'https://www.pathofexile.com/api/trade/data/items'

def get_request_kr(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, verify=False)
  return json.loads(res.text)

def get_request_en(url):
  scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
  res = scraper.get(url)
  return json.loads(res.text)

translate = {}
items = {}
uniques = {}
accessories = {}
armours = {}
flasks = {}
gems = {}
jewels = {}
weapons = {}

kr_items = get_request_kr(URL)
en_items = get_request_en(EN_URL)

item_ids = ['accessories', 'armour', 'flasks', 'gems', 'jewels', 'weapons']
for idx, en_item in enumerate(en_items['result']):
  kr_item = kr_items['result'][idx]
  # PoB에 필요한 데이터만 사용
  if en_item['id'] in item_ids:
    for idx1, en_val1 in enumerate(en_item['entries']):
      # idx1 : 아이템 번호, en_val1 : 영문 아이템 정보
      try:
        val1 = kr_item['entries'][idx1]
        # val1 : 한글 아이템 정보
        if 'name' in en_val1.keys():
          uniques[en_val1['name']] = val1['name'] + '(' + en_val1['name'] + ')'
        else:
          if 'flags' in en_val1.keys():
            print(en_val1['name'])
          if en_item['id'] == 'accessories':
            accessories[en_val1['text']] = val1['text']
          elif en_item['id'] == 'armour':
            armours[en_val1['text']] = val1['text']
          elif en_item['id'] == 'flasks':
            flasks[en_val1['text']] = val1['text']
          elif en_item['id'] == 'gems':
            gem_en_txt = en_val1['text'].replace(" Support", "")
            gems[gem_en_txt] = val1['text']
          elif en_item['id'] == 'jewels':
            jewels[en_val1['text']] = val1['text']
          elif en_item['id'] == 'weapons':
            weapons[en_val1['text']] = val1['text']
          
      except IndexError:
        print(idx1, en_val1)


with open('../uniques_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in uniques.items():
      spamwriter.writerow([key, val])

with open('../armours_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in armours.items():
      spamwriter.writerow([key, val])

with open('../accessories_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in accessories.items():
      spamwriter.writerow([key, val])

with open('../flasks_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in flasks.items():
      spamwriter.writerow([key, val])

with open('../gems_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in gems.items():
      spamwriter.writerow([key, val])

with open('../jewels_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in jewels.items():
      spamwriter.writerow([key, val])

with open('../weapons_from_api.csv', 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in weapons.items():
      spamwriter.writerow([key, val])