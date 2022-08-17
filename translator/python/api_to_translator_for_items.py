#-*- coding: utf-8 -*-
import csv

api_dir = '../../api'
api_files = {'accessories' : 'accessories_from_api.csv', 'armour' : 'armours_from_api.csv', 'flasks' : 'flasks_from_api.csv', 'gems' : 'gems_from_api.csv', 'jewels' : 'jewels_from_api.csv', 'weapons' : 'weapons_from_api.csv', 'uniques' : 'uniques_from_api.csv'}

kr_dir = '../../PoeCharm/Pob/translate_kr'
tr_files = {'accessories' : 'Items_Accessories.txt.csv', 'armour' : 'Items_Armour.txt.csv', 'flasks' : 'Items_Flasks.txt.csv', 'gems' : 'Items_Gems.txt.csv', 'jewels' : 'Items_Jewels.txt.csv', 'weapons' : 'Items_Weapons.txt.csv', 'uniques' : 'Uniques.txt.csv'}

result_dir = '../translate_kr'

def file_open(file_dir, file_name):
  data = {}
  with open(file_dir + '/' + file_name, 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile)
    for row in read_csv:
      data[row[0].strip()] = row[1].strip()
  return data

for file_key, file_name in api_files.items():
  orig_list = file_open(kr_dir, tr_files[file_key])
  api_list = file_open(api_dir, file_name)
  
  for key, api_val in api_list.items():
    orig_list[key] = api_val

  # 수정된 정보 저장
  with open(result_dir + '/' + tr_files[file_key], 'w', encoding='utf8') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
      for key, val in orig_list.items():
        spamwriter.writerow([key, val])