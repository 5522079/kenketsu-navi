import os
import csv
import datetime

from bs4 import BeautifulSoup
import requests


file_path = "../data/BloodStock.csv"

sites = [
    {'url':'https://www.bs.jrc.or.jp/hkd/hokkaido/index.html', 'code': 1, 'class': 'center-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/th/bbc/index.html', 'code': 2, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/ktks/bbc/index.html', 'code': 3, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/tkhr/bbc/index.html', 'code': 4, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/kk/bbc/index.html', 'code': 5, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/csk/bbc/index.html', 'code': 6, 'class': 'block-main-today-types-state'}, 
    {'url':'https://www.bs.jrc.or.jp/bc9/bbc/index.html', 'code': 7, 'class': 'block-main-today-types-state'}
]

def write_to_csv(code, data, file):
    with open(file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([code] + data)

# ヘッダー
header = ['block_code', '400-a', '400-o', '400-b', '400-ab', '200-a', '200-o', '200-b', '200-ab', 'com-a', 'com-o', 'com-b', 'com-ab']
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

# スクレイピング
for site in sites:
    response = requests.get(site['url'])
    soup = BeautifulSoup(response.content, "html.parser")
    target_elements = [element.text for element in soup.find_all(lambda tag: tag.name == 'p' and site['class'] in tag.get('class', [])) if element.text.strip()]
    
    write_to_csv(site['code'], target_elements, file_path)

# ファイル名に更新日をつけてリネーム
now = datetime.datetime.today()
new_file_name = str(now.month) + '-' + str(now.day)
new_file_path = f'../data/BloodStock_{new_file_name}.csv'

file_list = os.listdir('./data')
for file in file_list:
    if 'BloodStock' in file:
        current_file_name = file
        current_file_path = f'../data/{current_file_name}'
    else:
        print('ファイルが見つかりませんでした')
        current_file_path = '../data/error.csv'

os.rename(current_file_path, new_file_path)