from flask import Flask, render_template, request
import csv
import pandas as pd
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('top.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nationwide')
def nationwide():
    areas = [
            {"code" : 1, "name" : '北海道'},
            {"code" : 2, "name" : '青森'},
            {"code" : 3, "name" : '岩手'},
            {"code" : 4, "name" : '宮城'},
            {"code" : 5, "name" : '秋田'},
            {"code" : 6, "name" : '山形'},
            {"code" : 7, "name" : '福島'},
            {"code" : 8, "name" : '茨城'},
            {"code" : 9, "name" : '栃木'},
            {"code" : 10, "name" : '群馬'},
            {"code" : 11, "name" : '埼玉'},
            {"code" : 12, "name" : '千葉'},
            {"code" : 13, "name" : '東京'},
            {"code" : 14, "name" : '神奈川'},
            {"code" : 15, "name" : '新潟'},
            {"code" : 16, "name" : '富山'},
            {"code" : 17, "name" : '石川'},
            {"code" : 18, "name" : '福井'},
            {"code" : 19, "name" : '山梨'},
            {"code" : 20, "name" : '長野'},
            {"code" : 21, "name" : '岐阜'},
            {"code" : 22, "name" : '静岡'},
            {"code" : 23, "name" : '愛知'},
            {"code" : 24, "name" : '三重'},
            {"code" : 25, "name" : '滋賀'},
            {"code" : 26, "name" : '京都'},
            {"code" : 27, "name" : '大阪'},
            {"code" : 28, "name" : '兵庫'},
            {"code" : 29, "name" : '奈良'},
            {"code" : 30, "name" : '和歌山'},
            {"code" : 31, "name" : '鳥取'},
            {"code" : 32, "name" : '島根'},
            {"code" : 33, "name" : '岡山'},
            {"code" : 34, "name" : '広島'},
            {"code" : 35, "name" : '山口'},
            {"code" : 36, "name" : '徳島'},
            {"code" : 37, "name" : '香川'},
            {"code" : 38, "name" : '愛媛'},
            {"code" : 39, "name" : '高知'},
            {"code" : 40, "name" : '福岡'},
            {"code" : 41, "name" : '佐賀'},
            {"code" : 42, "name" : '長崎'},
            {"code" : 43, "name" : '熊本'},
            {"code" : 44, "name" : '大分'},
            {"code" : 45, "name" : '宮崎'},
            {"code" : 46, "name" : '鹿児島'},
            {"code" : 47, "name" : '沖縄'}
    ]
    update = load_log()

    status_levels, predict_levels = [], []
    total_donors, total_blood, total_rooms = 0, 0, 0
    for i in range(1, 48):
        stock, color, level = load_status(i)
        date, data = chart(i)
        donors, blood = calculate(i)
        total_donors += donors
        total_blood += blood
        total_rooms += len(load_room(i))
        status_levels.append(level)
        predict_levels.append(100 - (sum(data[13:])/sum(data[5:8])) * 100)
    status_data = [{"code": area["code"], "name": area["name"], "number": level} for area, level in zip(areas, status_levels)]
    predict_data = [{"code": area["code"], "name": area["name"], "number": level} for area, level in zip(areas, predict_levels)]

    return render_template('nationwide.html', update = update, predict_areas_data = predict_data, status_areas_data = status_data,
                           total_blood_donors = total_donors, total_blood = int(total_blood), total_rooms = total_rooms
                           )

@app.route('/prefecture', methods=['POST'])
def pref():
    prefecture_id = int(request.form.get('prefecture_id'))
    prefecture_name = request.form.get('prefecture_name')

    blood_donors, blood = calculate(prefecture_id)
    stock, color, level = load_status(prefecture_id)
    chart_index, chart_data = chart(prefecture_id)
    rooms_detail = load_room(prefecture_id)
    update = load_log()
    return render_template('prefecture.html', prefecture_name=prefecture_name, update = update,
                           a4 = stock[0], o4 = stock[1], b4 = stock[2], ab4 = stock[3],
                           a2 = stock[4], o2 = stock[5], b2 = stock[6], ab2 = stock[7],
                           ac = stock[8], oc = stock[9], bc = stock[10], abc = stock[11],
                           a4_col = color[0], o4_col = color[1], b4_col = color[2], ab4_col = color[3],
                           a2_col = color[4], o2_col = color[5], b2_col = color[6], ab2_col = color[7],
                           ac_col = color[8], oc_col = color[9], bc_col = color[10], abc_col = color[11],
                           total_blood_donors = blood_donors, total_blood = blood, total_rooms = len(rooms_detail),
                           months = chart_index, data1 = chart_data[:8], data2 = chart_data[8:]
                           )

def calculate(prefecture_id):
    file_path = "./data/BloodDonation.csv"
    df = pd.read_csv(file_path)

    pref_df = df[df['prefecture_id'] == prefecture_id]
    total_blood_donors = sum(pref_df['blood_donors'])
    total_blood = (sum(pref_df['200mL_blood_donation']) * 200 + sum(pref_df['400mL_blood_donation']) * 400) / 1000
    return total_blood_donors, total_blood

def chart(prefecture_id):
    with open('./data/data_8.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    tmp = data[0][9:]
    chart_data_index = [re.search(r'-(\d+)', date).group(1) + '月' for date in tmp]

    chart_data = []
    for d in data[1:]:
        if d[0] == str(prefecture_id):
            chart_data.append(d[1:17])
    chart_data = [int(float(value)) for sublist in chart_data for value in sublist]
    
    return chart_data_index, chart_data

def load_status(prefecture_id):
    status_color = {'安心です': '#d65f4e', '心配です': '#fedbc7', '困っています': '#d1e5f0', '非常に困ってます': '#4394c3'}
    status_level = {'安心です': 3, '心配です': 2, '困っています': 1, '非常に困ってます': 0}
    # {block_code : [prefecture_id]}
    prefecture_dict = {
                       1 : [1], 
                       2 : [2, 3, 4, 5, 6, 7], 
                       3 : [8, 9, 10, 11, 12, 13, 14, 15, 19, 20], 
                       4 : [16, 17, 18, 21, 22, 23, 24], 
                       5 : [25, 26, 27, 28, 29, 30], 
                       6 : [31, 32, 33, 34, 35, 36, 37, 38, 39], 
                       7 : [40, 41, 42, 43, 44, 45, 46, 47]
                       }

    with open('./data/BloodStock.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        blood_stock = list(reader)

    block_code = -1
    for i in range(1, 8):
        if prefecture_id in prefecture_dict[i]:
            block_code = i
    
    status = blood_stock[block_code][1 : 13]

    colors = []
    level = 0
    for lis in status:
        if status_color[lis] == '#fedbc7' or status_color[lis] == '#d1e5f0':
            colors.append([status_color[lis], '#333'])
        else:
            colors.append([status_color[lis], '#fff'])
        level += status_level[lis]

    return status, colors, level

def load_log():
    with open('./data/log.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        logs = list(reader)
        date = str(logs[0][0])
        update_date = re.sub(r'\d{4}-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}', lambda x: f"{int(x.group(1))}月{int(x.group(2))}日", date)
    return update_date

def load_room(prefecture_id):
    with open('./data/BloodRoom.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rooms = list(reader)

    rooms_detail = []
    for room in rooms:
        if room[0] == str(prefecture_id):
            rooms_detail.append(room[1:])
    return rooms_detail

if __name__ == '__main__':
    app.run(debug=True)
