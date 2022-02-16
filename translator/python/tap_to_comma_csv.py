#-*- coding: utf-8 -*-
import csv

read_file_name = '../temp.csv'
write_file_name = '../temp_.csv'

read_data = {}
with open(read_file_name, 'r', encoding='utf8') as csvfile:
  read_csv = csv.reader(csvfile, delimiter='	')
  for row in read_csv:
    read_data[row[0].strip()] = row[1].strip()

with open(write_file_name, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for key, val in read_data.items():
      spamwriter.writerow([key, val])