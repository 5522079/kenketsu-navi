from japanmap import picture
import matplotlib.pyplot as plt
import pandas as pd
import csv
from datetime import datetime

# ステータスに応じた色を返す関数
def status_to_color(status):
    # ステータスごとに色を指定するリスト
    trans_list = [
        {'status': '安心です', 'cols': '#CE0000'},
        {'status': '心配です', 'cols': '#FF5454'},
        {'status': '困っています', 'cols': '#FF9696'},
        {'status': '非常に困ってます', 'cols': 'white'}
    ]
    
    for trans_item in trans_list:
        if status == trans_item['status']:
            return trans_item['cols']

# ログを書く関数
def write_log(message):
    log_entry = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message]
    log_file_path = '../data/log.csv'

    # 既存のログを読み込む
    try:
        with open(log_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            logs = list(reader)
    except FileNotFoundError:
        logs = []

    # 新しいログを先頭に追加
    logs.insert(0, log_entry)

    # ログをファイルに書き込む
    with open(log_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(logs)

# マップの種類
columns_list = ['400-a', '400-o', '400-b', '400-ab', '200-a', '200-o', '200-b', '200-ab', 'com-a', 'com-o', 'com-b', 'com-ab']

# グラフのスタイルとサイズを指定
plt.rcParams['figure.figsize'] = 6, 6

for c in columns_list:
    try:
        df = pd.read_csv('../data/BloodStock.csv')
        # 都道府県ごとの色を設定するリスト
        prefecture_list = [
        {1: {'北海道': '01'}},
        {2: {'青森県': '02'}},
        {2: {'岩手県': '03'}},
        {2: {'宮城県': '04'}},
        {2: {'秋田県': '05'}},
        {2: {'山形県': '06'}},
        {2: {'福島県': '07'}},
        {3: {'茨城県': '08'}},
        {3: {'栃木県': '09'}},
        {3: {'群馬県': '10'}},
        {3: {'埼玉県': '11'}},
        {3: {'千葉県': '12'}},
        {3: {'東京都': '13'}},
        {3: {'神奈川県': '14'}},
        {3: {'新潟県': '15'}},
        {4: {'富山県': '16'}},
        {4: {'石川県': '17'}},
        {4: {'福井県': '18'}},
        {3: {'山梨県': '19'}},
        {3: {'長野県': '20'}},
        {4: {'岐阜県': '21'}},
        {4: {'静岡県': '22'}},
        {4: {'愛知県': '23'}},
        {4: {'三重県': '24'}},
        {5: {'滋賀県': '25'}},
        {5: {'京都府': '26'}},
        {5: {'大阪府': '27'}},
        {5: {'兵庫県': '28'}},
        {5: {'奈良県': '29'}},
        {5: {'和歌山県': '30'}},
        {6: {'鳥取県': '31'}},
        {6: {'島根県': '32'}},
        {6: {'岡山県': '33'}},
        {6: {'広島県': '34'}},
        {6: {'山口県': '35'}},
        {6: {'徳島県': '36'}},
        {6: {'香川県': '37'}},
        {6: {'愛媛県': '38'}},
        {6: {'高知県': '39'}},
        {7: {'福岡県': '40'}},
        {7: {'佐賀県': '41'}},
        {7: {'長崎県': '42'}},
        {7: {'熊本県': '43'}},
        {7: {'大分県': '44'}},
        {7: {'宮崎県': '45'}},
        {7: {'鹿児島県': '46'}},
        {7: {'沖縄県': '47'}}
        ]
        prefecture_dict = {}
        # ブロックごとの色を設定するデータフレーム
        df_color = pd.concat([df[c].apply(status_to_color), df['block_code']], axis=1)
        df_color.columns = ['cols', 'block_code']

        # 各都道府県のステータスに基づき色を設定
        for d in df_color.iterrows():
            for l in prefecture_list:
                if int(d[1]['block_code']) == list(l.keys())[0]:
                    list(l.values())[0][list(list(l.values())[0].keys())[0]] = d[1]['cols']

        # ライブラリが読み込める形式に変換
        for i in range(0, 47):
            l = list(prefecture_list[i].values())[0]
            prefecture_list[i] = l
        prefecture_dict = {list(item.keys())[0]: list(item.values())[0] for item in prefecture_list}

        # マップを作成
        fig, ax = plt.subplots(facecolor='white')
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        plt.imshow(picture(prefecture_dict))
        plt.axis('off')

        # マップを保存
        plt.savefig(f'../static/images/data/map_{c}.png')
        plt.close(fig)  # マップを閉じて次のループへ

        # ログに成功を記録
        write_log(f"Map for {c} created successfully.")
    except Exception as e:
        # ログにエラーを記録
        write_log(f"Error creating map for {c}: {e}")
