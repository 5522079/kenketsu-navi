import csv
import os
import re

import pandas as pd


PREFECTURE_NAMES = {
    1: '北海道',
    2: '青森',
    3: '岩手',
    4: '宮城',
    5: '秋田',
    6: '山形',
    7: '福島',
    8: '茨城',
    9: '栃木',
    10: '群馬',
    11: '埼玉',
    12: '千葉',
    13: '東京',
    14: '神奈川',
    15: '新潟',
    16: '富山',
    17: '石川',
    18: '福井',
    19: '山梨',
    20: '長野',
    21: '岐阜',
    22: '静岡',
    23: '愛知',
    24: '三重',
    25: '滋賀',
    26: '京都',
    27: '大阪',
    28: '兵庫',
    29: '奈良',
    30: '和歌山',
    31: '鳥取',
    32: '島根',
    33: '岡山',
    34: '広島',
    35: '山口',
    36: '徳島',
    37: '香川',
    38: '愛媛',
    39: '高知',
    40: '福岡',
    41: '佐賀',
    42: '長崎',
    43: '熊本',
    44: '大分',
    45: '宮崎',
    46: '鹿児島',
    47: '沖縄',
}

AREAS = [{"code": code, "name": name} for code, name in PREFECTURE_NAMES.items()]


def calculate(prefecture_id):
    file_path = './data/BloodDonation.csv'
    df = pd.read_csv(file_path)

    pref_df = df[df['prefecture_id'] == prefecture_id]
    total_blood_donors = sum(pref_df['blood_donors'])
    total_blood = (sum(pref_df['200mL_blood_donation']) * 200 + sum(pref_df['400mL_blood_donation']) * 400) / 1000

    return total_blood_donors, total_blood


def chart(prefecture_id):
    with open('./data/graph.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    tmp = data[0][1:9]
    chart_data_index = [re.search(r'-(\d+)', date).group(1) + '月' for date in tmp]

    chart_data = []
    for row in data[1:]:
        if row[0] == str(prefecture_id):
            chart_data.append(row[1:])
    chart_data = [int(float(value)) for sublist in chart_data for value in sublist]

    return chart_data_index, chart_data


def load_status(prefecture_id):
    status_color = {'安心です': '#d65f4e', '心配です': '#fedbc7', '困っています': '#d1e5f0', '非常に困ってます': '#4394c3'}
    status_level = {'安心です': 3, '心配です': 2, '困っています': 1, '非常に困ってます': 0}
    prefecture_dict = {
        1: [1],
        2: [2, 3, 4, 5, 6, 7],
        3: [8, 9, 10, 11, 12, 13, 14, 15, 19, 20],
        4: [16, 17, 18, 21, 22, 23, 24],
        5: [25, 26, 27, 28, 29, 30],
        6: [31, 32, 33, 34, 35, 36, 37, 38, 39],
        7: [40, 41, 42, 43, 44, 45, 46, 47],
    }

    file_name = None
    for file in os.listdir('./data'):
        if 'BloodStock' in file:
            file_name = file

    if file_name is None:
        raise FileNotFoundError('BloodStock CSV not found in data directory')

    with open(f'./data/{file_name}', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        blood_stock = list(reader)

    block_code = -1
    for i in range(1, 8):
        if prefecture_id in prefecture_dict[i]:
            block_code = i

    status = blood_stock[block_code][1:13]

    colors = []
    level = 0
    for item in status:
        if status_color[item] == '#fedbc7' or status_color[item] == '#d1e5f0':
            colors.append([status_color[item], '#333'])
        else:
            colors.append([status_color[item], '#fff'])
        level += status_level[item]

    return status, colors, level


def load_update():
    date = ''
    for file in os.listdir('./data'):
        if 'BloodStock' in file:
            match = re.search(r'BloodStock_([0-9]{1,2})-([0-9]{1,2})\.csv', file)
            if match:
                month = match.group(1)
                day = match.group(2)
                date = f"{int(month)}月{int(day)}日"
            break

    return date


def load_room(prefecture_id):
    with open('./data/BloodRoom.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rooms = list(reader)

    rooms_detail = []
    for room in rooms:
        if room[0] == str(prefecture_id):
            rooms_detail.append(room[1:])
    return rooms_detail