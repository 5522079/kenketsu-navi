from bs4 import BeautifulSoup
import requests
import csv

# 保存するファイルを指定する
file_path = "../data/BloodStock.csv"

# CSVファイルに書き込む関数
def write_to_csv(code, data, file):
    with open(file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([code] + data)

# 複数のWebサイトのURLをリストに格納する
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

# ヘッダー行をCSVファイルに書き込む
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

# 各Webサイトを順に処理する
for site in sites:
    # 指定したURLから情報を取得し，変数に格納する
    response = requests.get(site['url'])
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 指定したクラス属性を持つすべての<p>タグの要素を取得し、空でないテキストを持つ要素のみをリストに格納する
    target_elements = [element.text for element in soup.find_all(lambda tag: tag.name == 'p' and site['class'] in tag.get('class', [])) if element.text.strip()]
    
    # 都道府県コードとデータをCSVファイルに書き込む
    write_to_csv(site['code'], target_elements, file_path)
