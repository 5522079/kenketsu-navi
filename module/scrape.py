from bs4 import BeautifulSoup
import requests
import csv

file_path = "../data/BloodStock.csv"

def write_to_csv(code, data, file):
    with open(file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([code] + data)

sites = [
    {'url':'https://www.bs.jrc.or.jp/hkd/hokkaido/index.html', 'code': 1, 'class': 'center-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/th/bbc/index.html', 'code': 2, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/ktks/bbc/index.html', 'code': 3, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/tkhr/bbc/index.html', 'code': 4, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/kk/bbc/index.html', 'code': 5, 'class': 'block-main-today-types-state'},
    {'url':'https://www.bs.jrc.or.jp/csk/bbc/index.html', 'code': 6, 'class': 'block-main-today-types-state'}, 
    {'url':'https://www.bs.jrc.or.jp/bc9/bbc/index.html', 'code': 7, 'class': 'block-main-today-types-state'}
]

# ヘッダー
header = ['block_code', '400-a', '400-o', '400-b', '400-ab', '200-a', '200-o', '200-b', '200-ab', 'com-a', 'com-o', 'com-b', 'com-ab']

with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

for site in sites:
    response = requests.get(site['url'])
    soup = BeautifulSoup(response.content, "html.parser")
    
    target_elements = [element.text for element in soup.find_all(lambda tag: tag.name == 'p' and site['class'] in tag.get('class', [])) if element.text.strip()]
    
    write_to_csv(site['code'], target_elements, file_path)
