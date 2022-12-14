import sys
import csv
import json
import re
import time
import requests
import more_itertools as mit
import cloudscraper

# gem과 unique의 경우 stat api 외에 trade에서도 정보를 가져와야하기 때문에
# 이를 위한 작업이 이루어지도록 설계 됨

# gem, unique 중 하나를 입력 받아야 동작하도록 함
if len(sys.argv) < 2 :
  print("실행 인자가 부족합니다. gem 또는 unique를 입력해주세요.")
  exit()

if sys.argv[1] != 'gem' and sys.argv[1] != 'unique':
  print("인자는 gem 또는 unique만 가능합니다.")
  exit()

# 어떤 아이템, 몇 개의 아이템을 작업할 것인지 설정
ItemType = sys.argv[1]
StartCount = 3
MaxCount = 0

# 한글, 영문 api 주소
League = 'Sanctum' # 현재 리그명 또는 Standard를 선택
URL = 'https://poe.game.daum.net/api/trade'
EN_URL = 'https://www.pathofexile.com/api/trade'
search_uri = '/search/' + League
item_info_uri = '/data/items'
fetch_uri = '/fetch/'

# Trade 검색 쿼리 https://poe-query.vercel.app/ 참조
if ItemType == 'gem' :
  query_base = {"query":{"status":{"option":"online"},"stats":[{"type":"and","filters":[],"disabled":False}],"filters": {"misc_filters": {"filters": {"quality": {"min": 10,"max": None}},"disabled": False}}},"sort":{"price":"asc"}}
else :
  query_base = {"query":{"status":{"option":"online"},"stats":[{"type":"and","filters":[],"disabled":False}]},"sort":{"price":"asc"}}

# 각 폴더 정의
orig_tr_dir = '../../PoeCharm/Pob/translate_kr'
result_dir = '../../translator/translate_kr'

# 각 파일명 정의
unique_file = 'Uniques.txt.csv'
gem_file = 'Items_Gems.txt.csv'
stat_description_file = 'statDescriptions.csv'
etcs_file = 'etcs.csv'

def file_open(list, file_name):
  with open(orig_tr_dir + '/' + file_name, 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      list[row[0].strip()] = row[1].strip()

def file_write(list, file_name, keys):
  with open(result_dir + '/' + file_name, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    key_count = 0
    for key, val in list.items():
      spamwriter.writerow([keys[key_count], val])
      key_count = key_count + 1

# file내 정보를 읽어 옴
item_list = {}
desc_list = {}
etcs_list = {}
desc_keys = {}
etcs_keys = {}
if ItemType == 'unique' :
  file_open(item_list, unique_file)
else :
  file_open(item_list, gem_file)

file_open(desc_list, stat_description_file)
desc_keys = list(desc_list.keys())
file_open(etcs_list, etcs_file)
etcs_keys = list(etcs_list.keys())

# 주요 함수 선언
def get_request_kr(url):
  res = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, verify=False)
  return json.loads(res.text)

def get_request_en(url):
  scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
  res = scraper.get(url)

  return json.loads(res.text)

def post_request_kr(url, json_data):
  res = requests.post(url, json=json_data, verify=False)
  return json.loads(res.text)

def post_request_en(url, json_data):
  scraper = cloudscraper.create_scraper(delay=15,   browser={'custom': 'ScraperBot/1.0',})
  res = scraper.post(url, json=json_data)
  return json.loads(res.text)

def reshape(lst, n):
    return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

def repl(m):
  return next(repl.v)
repl.v=mit.seekable(('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'))

def number_to_blanket(text):
  result = re.sub('[+-]?(?=\d)(\d*\.?\d*)', repl, text)
  repl.v.seek(0)
  return result

def desc_change(en_txt, kr_txt, insertion):
  en_txt = number_to_blanket(en_txt).strip()
  kr_txt = number_to_blanket(kr_txt).strip()

  # 수정할 내용이 있는지 확인
  exist = False
  if en_txt in desc_list:
    desc_list[en_txt] = kr_txt
    exist = True
  else :
    for en_key in desc_list:
      if en_key.lower() == en_txt.lower():
        desc_keys[desc_keys.index(en_key)] = en_txt
        desc_list[en_key] = kr_txt
        exist = True
        break

  # 수정할 내용이 없을 경우 데이터 추가
  if exist == False and insertion == True:
    desc_list[en_txt] = kr_txt
    desc_keys.append(en_txt)

def etcs_change(en_txt, kr_txt, insertion):
  en_txt = number_to_blanket(en_txt).strip()
  kr_txt = number_to_blanket(kr_txt).strip()

  # 수정할 내용이 있는지 확인
  # etcs의 경우 수정할 경우만 수정하고 추가는 하지 않음
  exist = False
  if en_txt in etcs_list:
    etcs_list[en_txt] = kr_txt
    exist = True
  else :
    for en_key in etcs_list:
      if en_key.lower() == en_txt.lower():
        etcs_keys[etcs_keys.index(en_key)] = en_txt
        etcs_list[en_key] = kr_txt
        exist = True
        break

  # 수정할 내용이 없을 경우 데이터 추가
  if exist == False and insertion == True:
    etcs_list[en_txt] = kr_txt
    etcs_keys.append(en_txt)

def check_desc_list(en_txt, kr_txt, insertion):
  en_txts = en_txt.splitlines()
  kr_txts = kr_txt.splitlines()
  if len(en_txts) > 0 :
    for idx in range(len(en_txts)) :
      desc_change(en_txts[idx], kr_txts[idx], insertion)
  else :
    desc_change(en_txt, kr_txt, insertion)

def check_etcs_list(en_txt, kr_txt, insertion):
  en_txts = en_txt.splitlines()
  kr_txts = kr_txt.splitlines()
  if len(en_txts) > 0 :
    for idx in range(len(en_txts)) :
      etcs_change(en_txts[idx], kr_txts[idx], insertion)
  else :
    etcs_change(en_txt, kr_txt, insertion)



# item_list = {"Heavy Strike": "묵직한 타격"}
# item_list = {"Astramentis": "별의 보석(Astramentis)"}

# 아이템 리스트 순서대로 올라가면서 데이터를 가져옴
count = 0
for en_type, kr_type in item_list.items():
  # 마지막에 놓을 경우 continue 될 때 카운트가 올라가지 않아 제일 앞으로 옮김
  count = count + 1

  # 얼마나 남았는지 표시
  print(str(count) + ' / ' + str(len(item_list)))
  print(kr_type)

  # 원하는 횟수만큼 동작
  if MaxCount != 0 and count > MaxCount:
    continue
  if StartCount != 0 and count < StartCount:
    continue

  # 한글 api에서 데이터를 불러옴
  query = query_base.copy()
  query['query']['term'] = en_type
  result = post_request_en(EN_URL + search_uri, json_data=query)

  # 결과가 없을 때는 생략 (단, 15초 쉬는 부분은 필요 함)
  if 'result' not in result:
    print('is not response for sale')
    # api 밴을 방지하기 위한 15초 딜레이
    time.sleep(15)
    continue

  # 모든 결과 중 첫 번째 결과에 대한 거래 정보를 가져옴
  # 이 정보를 이용해 item의 상세내용을 가져옴
  items = result['result']
  fetchs = reshape(items, 1)

  # 만일 아이템 개수가 여러개가 아닐 경우 판매되는 것이 없는 것으로 판단하여 생략
  if len(fetchs) < 1:
    print('is not for sale')
    # api 밴을 방지하기 위한 15초 딜레이
    time.sleep(15)
    continue
  fetch = fetchs[0]
  en_info = get_request_en(EN_URL + fetch_uri + ','.join(fetch))
  kr_info = get_request_kr(URL + fetch_uri + ','.join(fetch))

  # 정보 확인을 위한 출력 부분
  # print('아이템 정보 전체')
  # print(kr_info['result'][0]['item'])
  # print('한글 정보')
  # print(kr_info['result'][0]['item']['secDescrText'])
  # print(kr_info['result'][0]['item']['explicitMods'])
  # print(kr_info['result'][0]['item']['descrText'])
  # print('영문 정보')
  # print(en_info['result'][0]['item']['secDescrText'])
  # print(en_info['result'][0]['item']['explicitMods'])
  # print(en_info['result'][0]['item']['descrText'])

  # 일반 속성이 있으면 작업
  if 'result' in kr_info and 'item' in en_info['result'][0] and 'explicitMods' in en_info['result'][0]['item']:
    print('item explicitMods exists')
    for idx in range(len(kr_info['result'][0]['item']['explicitMods'])):
      check_desc_list(en_info['result'][0]['item']['explicitMods'][idx], kr_info['result'][0]['item']['explicitMods'][idx], True)
      check_etcs_list(en_info['result'][0]['item']['explicitMods'][idx], kr_info['result'][0]['item']['explicitMods'][idx], False)
  else:
    print('item explicitMods not exists')

  # 추가 속성이 있으면 작업
  if 'result' in kr_info and 'item' in en_info['result'][0] and 'implicitMods' in en_info['result'][0]['item']:
    print('item implicitMods exists')
    for idx in range(len(kr_info['result'][0]['item']['implicitMods'])):
      check_desc_list(en_info['result'][0]['item']['implicitMods'][idx], kr_info['result'][0]['item']['implicitMods'][idx], True)
      check_etcs_list(en_info['result'][0]['item']['implicitMods'][idx], kr_info['result'][0]['item']['implicitMods'][idx], False)
  else:
    print('item implicitMods not exists')

  # 아이템(젬) 설명 문구가 있을 경우 업데이트 하도록 함
  if 'result' in kr_info and 'item' in en_info['result'][0] and 'secDescrText' in en_info['result'][0]['item']:
    print('item secDescrText exists')
    for idx in range(len(kr_info['result'][0]['item']['secDescrText'])):
      check_etcs_list(en_info['result'][0]['item']['secDescrText'], kr_info['result'][0]['item']['secDescrText'], True)
  else:
    print('item secDescrText not exists')



  # 젬 정보 수정된 것 저장 10번마다 한 번씩 저장하도록 함
  if ((count % 10) == 0):
    print('file write')
    file_write(desc_list, stat_description_file, desc_keys)
    file_write(etcs_list, etcs_file, etcs_keys)

  # api 밴을 방지하기 위한 15초 딜레이
  time.sleep(15)


# 젬 정보 수정된 것 저장
file_write(desc_list, stat_description_file, desc_keys)
file_write(etcs_list, etcs_file, etcs_keys)