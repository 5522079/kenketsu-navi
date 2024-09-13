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
    return render_template('nationwide.html')

@app.route('/prefecture', methods=['POST'])
def pref():
    prefecture_id = int(request.form.get('prefecture_id'))
    prefecture_name = request.form.get('prefecture_name')

    blood_donors, blood = calculate(prefecture_id)
    stock, color = status(prefecture_name)
    chart_index, chart_data = chart(prefecture_id)
    
    return render_template('prefecture.html', prefecture_name=prefecture_name,
                           a4 = stock[0], o4 = stock[1], b4 = stock[2], ab4 = stock[3],
                           a2 = stock[4], o2 = stock[5], b2 = stock[6], ab2 = stock[7],
                           ac = stock[8], oc = stock[9], bc = stock[10], abc = stock[11],
                           a4_col = color[0], o4_col = color[1], b4_col = color[2], ab4_col = color[3],
                           a2_col = color[4], o2_col = color[5], b2_col = color[6], ab2_col = color[7],
                           ac_col = color[8], oc_col = color[9], bc_col = color[10], abc_col = color[11],
                           total_blood_donors = blood_donors, total_blood = blood,
                           months = chart_index, data1 = chart_data[:8], data2 = chart_data[8:])

def calculate(prefecture_id):
    file_path = "../data/BloodDonation.csv"
    df = pd.read_csv(file_path)

    pref_df = df[df['prefecture_id'] == prefecture_id]
    total_blood_donors = sum(pref_df['blood_donors'])
    total_blood = (sum(pref_df['200mL_blood_donation']) * 200 + sum(pref_df['400mL_blood_donation']) * 400) / 1000
    return total_blood_donors, total_blood

def chart(prefecture_id):
    with open('./data_8.csv', 'r') as csvfile:
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

def status(prefecture_name):
    status_dict = [
        {'安心です': '#F67280'},
        {'心配です': '#C06C84'},
        {'困っています': '#6C5B7B'},
        {'非常に困ってます': '#355C7D'}
        ]

    prefecture_dict = [
        {1: {'北海道': 1}},
        {2: {'青森': 2}},
        {2: {'岩手': 3}},
        {2: {'宮城': 4}},
        {2: {'秋田': 5}},
        {2: {'山形': 6}},
        {2: {'福島': 7}},
        {3: {'茨城': 8}},
        {3: {'栃木': 9}},
        {3: {'群馬': 10}},
        {3: {'埼玉': 11}},
        {3: {'千葉': 12}},
        {3: {'東京': 13}},
        {3: {'神奈川': 14}},
        {3: {'新潟': 15}},
        {4: {'富山': 16}},
        {4: {'石川': 17}},
        {4: {'福井': 18}},
        {3: {'山梨': 19}},
        {3: {'長野': 20}},
        {4: {'岐阜': 21}},
        {4: {'静岡': 22}},
        {4: {'愛知': 23}},
        {4: {'三重': 24}},
        {5: {'滋賀': 25}},
        {5: {'京都': 26}},
        {5: {'大阪': 27}},
        {5: {'兵庫': 28}},
        {5: {'奈良': 29}},
        {5: {'和歌山': 30}},
        {6: {'鳥取': 31}},
        {6: {'島根': 32}},
        {6: {'岡山': 33}},
        {6: {'広島': 34}},
        {6: {'山口': 35}},
        {6: {'徳島': 36}},
        {6: {'香川': 37}},
        {6: {'愛媛': 38}},
        {6: {'高知': 39}},
        {7: {'福岡': 40}},
        {7: {'佐賀': 41}},
        {7: {'長崎': 42}},
        {7: {'熊本': 43}},
        {7: {'大分': 44}},
        {7: {'宮崎': 45}},
        {7: {'鹿児島': 46}},
        {7: {'沖縄': 47}}
        ]
    
    prefecture_name = prefecture_name

    with open('../data/BloodStock.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        blood_stock = list(reader)

    block_code = -1
    for dic in prefecture_dict:
        for key, value in dic.items():
            if prefecture_name in value:
                block_code = key

    status = blood_stock[block_code][1 : 13]

    color = []
    for lis in status:
        for dic in status_dict:
            for key, value in dic.items():
                if key in lis:
                    color.append(value)

    return status, color

if __name__ == '__main__':
    app.run(debug=True)
