import requests
import json
import re
import csv
from bs4 import BeautifulSoup as bs
import more_itertools as mit
import cloudscraper

orig_tr_dir = '../../PoeCharm/Pob/translate_kr'
tree_dn_file = 'tree_dn.csv'
tree_sd_file = 'tree_sd.csv'
tree_rt_file = 'tree_rt.csv'
passive_tree_file = 'passiveTree.csv'
stat_description_file = 'statDescriptions.csv'
result_dir = '../../translator/translate_kr'

passive_pattern = re.compile(r"passiveSkillTreeData\s+=\s+(\{(.|\n)*?\});\n")

def get_request_en(url):
  scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
  response = scraper.get(url)
  return bs(response.text, 'html.parser')

def get_request_kr(url):
  response = requests.get(url, headers={'user-agent': 'Mozilla/5.0'}, verify=False)
  return bs(response.text, 'html.parser')

def get_json(data):
  script = data.find("script", text=passive_pattern)
  pattern = passive_pattern.search(script.text).group(1)
  json_data = json.loads(pattern)
  if 'root' in json_data:
    json_data.remove('root')
  return json_data['nodes']

def repl(m):
  return next(repl.v)
repl.v=mit.seekable(('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'))


tree_dn_list = {}
tree_sd_list = {}
tree_rt_list = {}
passive_tree_list = {}
desc_list = {}
with open(orig_tr_dir + '/' + tree_dn_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tree_dn_list[row[0].strip()] = row[1].strip()

with open(orig_tr_dir + '/' + tree_sd_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tree_sd_list[row[0].strip()] = row[1].strip()

with open(orig_tr_dir + '/' + tree_rt_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    tree_rt_list[row[0].strip()] = row[1].strip()

with open(orig_tr_dir + '/' + passive_tree_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    passive_tree_list[row[0].strip()] = row[1].strip()

with open(orig_tr_dir + '/' + stat_description_file, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile)
  for row in read_csv:
    desc_list[row[0]] = row[1]



kr_soup = get_request_kr('https://poe.game.daum.net/passive-skill-tree')
en_soup = get_request_en('https://www.pathofexile.com/passive-skill-tree')

kr_node = get_json(kr_soup)
en_node = get_json(en_soup)

# name : tree_dn, stats : tree_sd, reminderText : tree_rt, passiveTree
for key, en_data in en_node.items():
  # 이름 정리
  if 'name' in en_data:
    exist = False
    en_txt = en_data['name']
    kr_txt = kr_node[key]['name']

    for txt_key, val in tree_dn_list.items():
      if(txt_key.strip() == en_txt.strip()):
        exist = True
        tree_dn_list[txt_key] = kr_txt
    if(exist != True):
      tree_dn_list[en_txt] = kr_txt
    exist = False

  # stats 정리
  if 'stats' in en_data:
    for idx in range(len(en_data['stats'])):
      en_txt = en_data['stats'][idx]
      kr_txt = kr_node[key]['stats'][idx]

      for txt_key, val in tree_sd_list.items():
        if(txt_key.strip() == en_txt.strip()):
          exist = True
          tree_sd_list[txt_key] = kr_txt
      if(exist != True):
        tree_sd_list[en_txt] = kr_txt
      exist = False

  # reminderText 정리
  if 'reminderText' in en_data:
    for idx in range(len(en_data['reminderText'])):
      en_txt = en_data['reminderText'][idx]
      kr_txt = kr_node[key]['reminderText'][idx]

      for txt_key, val in tree_rt_list.items():
        if(txt_key.strip() == en_txt.strip()):
          exist = True
          tree_rt_list[txt_key] = kr_txt
      for txt_key, val in passive_tree_list.items():
        if(txt_key.strip() == en_txt.strip()):
          passive_tree_list[txt_key] = kr_txt
      if(exist != True):
        tree_rt_list[en_txt] = kr_txt
      exist = False

  if 'masteryEffects' in en_data:
    for idx in range(len(en_data['masteryEffects'])):
      en_masteryEffects = en_data['masteryEffects'][idx]
      kr_masteryEffects = kr_node[key]['masteryEffects'][idx]

      if 'stats' in en_masteryEffects:
        for idx1 in range(len(en_masteryEffects['stats'])):
          en_txt = en_masteryEffects['stats'][idx1]
          kr_txt = kr_masteryEffects['stats'][idx1]

          for txt_key, val in tree_sd_list.items():
            if(txt_key.strip() == en_txt.strip()):
              exist = True
              tree_sd_list[txt_key] = kr_txt
          if(exist != True):
            tree_sd_list[en_txt] = kr_txt
          exist = False

      if 'reminderText' in en_masteryEffects:
        for idx1 in range(len(en_masteryEffects['reminderText'])):
          en_txt = en_masteryEffects['reminderText'][idx1]
          kr_txt = kr_masteryEffects['reminderText'][idx1]

          for txt_key, val in tree_rt_list.items():
            if(txt_key.strip() == en_txt.strip()):
              exist = True
              tree_rt_list[txt_key] = kr_txt
          if(exist != True):
            tree_rt_list[en_txt] = kr_txt
          exist = False

# And statDescription
for key, en_data in en_node.items():
  # stats 정리
  if 'stats' in en_data:
    for idx in range(len(en_data['stats'])):
      en_txt = re.sub('(?=\d)(\d*\.?\d*)', repl, en_data['stats'][idx])
      repl.v.seek(0)
      kr_txt = re.sub('(?=\d)(\d*\.?\d*)', repl, kr_node[key]['stats'][idx])
      repl.v.seek(0)

      for txt_key, val in desc_list.items():
        if(txt_key.strip() == en_txt.strip()):
          desc_list[txt_key] = kr_txt

  # reminderText 정리
  if 'reminderText' in en_data:
    for idx in range(len(en_data['reminderText'])):
      en_txt = re.sub('(?=\d)(\d*\.?\d*)', repl, en_data['reminderText'][idx])
      repl.v.seek(0)
      kr_txt = re.sub('(?=\d)(\d*\.?\d*)', repl, kr_node[key]['reminderText'][idx])
      repl.v.seek(0)

      for txt_key, val in desc_list.items():
        if(txt_key.strip() == en_txt.strip()):
          desc_list[txt_key] = kr_txt

# name 정보 수정된 것 저장
with open(result_dir + '/' + tree_dn_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tree_dn_list.items():
      spamwriter.writerow([key, val])

# stats 정보 수정된 것 저장
with open(result_dir + '/' + tree_sd_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tree_sd_list.items():
      spamwriter.writerow([key, val])

# reminderText 정보 수정된 것 저장
with open(result_dir + '/' + tree_rt_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in tree_rt_list.items():
      spamwriter.writerow([key, val])

# reminderText 정보 수정된 것 저장
with open(result_dir + '/' + passive_tree_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in passive_tree_list.items():
      spamwriter.writerow([key, val])

# reminderText 정보 수정된 것 statDescriptions에 저장
with open(result_dir + '/' + stat_description_file, 'w', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL, escapechar=None)
    for key, val in desc_list.items():
      spamwriter.writerow([key, val])