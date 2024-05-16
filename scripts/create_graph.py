import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib import pyplot as plt
import japanize_matplotlib
from datetime import datetime
from dateutil.relativedelta import relativedelta

# グラフのスタイルとサイズ
plt.style.use('fast')
plt.rcParams['figure.figsize'] = [12, 9]

# CSVファイルを読み込む
file_path = "C:\\PJD\\BloodDonation\\data\\BloodDonation.csv"
df = pd.read_csv(file_path)

# "year" と "month" を結合して "date" 列を作成
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2))
df = df.groupby(['date'])["blood_donors"].sum().reset_index()


df_train = df.set_index('date')['blood_donors']

latest_date = df_train.index.max()
a_year_ago = df_train.reset_index()
a_year_ago['date'] = pd.to_datetime(a_year_ago['date'])
start_date = latest_date - pd.DateOffset(months=20)
end_date = latest_date - pd.DateOffset(months=9)
filtered_df = a_year_ago[(a_year_ago['date'] >= start_date) & (a_year_ago['date'] <= end_date)]

# 年を1年ずつシフトする関数
def shift_year(date, shift):
    return date.replace(year=date.year + shift)
filtered_df = filtered_df.assign(date=filtered_df['date'].apply(lambda x: shift_year(x, 1)))

# 未来の期間を含むデータフレームの作成
future_dates = pd.date_range(   start=(df_train.index.max()) + relativedelta(months=1), 
                                end=(df_train.index.max()) + relativedelta(months=3), freq='MS' )
future_df = pd.DataFrame(index=future_dates, columns=['blood_donors'])

# 原系列を学習データとする
train = df_train

# 学習
sarima_model = SARIMAX(train, order=(1, 0, 1), seasonal_order=(1, 1, 1, 10))
sarima_fit = sarima_model.fit()

# 予測
# 学習データの期間の予測値
train_pred = sarima_fit.predict(start=train.index[0], end=train.index[-1])
# 未来の期間の予測
future_pred = sarima_fit.forecast(steps=len(future_dates))

# df_train と future_pred を連結して新しい DataFrame を作成
show = pd.concat([df_train, future_pred])
new_columns = {
    'date': show.index,
    'blood_donors': show.values
}
tmp_df = pd.DataFrame(new_columns)

# グラフ化
fig, ax = plt.subplots()

# 予測データを学習データ
ax.plot(tmp_df[-12:]['date'], tmp_df[-12:]['blood_donors'], color="#FF7628", marker='d', markersize=6)
ax.plot(tmp_df[-3:]['date'], tmp_df[-3:]['blood_donors'], color="#01B7D6", marker='o', markersize=8)
# 棒グラフ
ax.bar(filtered_df['date'], filtered_df['blood_donors'], width=12, color="#FFBBBB", alpha=1)

plt.title("全国の総献血者数の推移と予測")
ax.legend(["献血者数", "予測献血者数", "昨年の献血者数"])

plt.xticks(tmp_df[-12:]['date'], [(date.strftime('%Y-%m')) for date in tmp_df[-12:]['date']], rotation=0)

plt.ylabel("献\n血\n者\n数", rotation=0)
y_ticks = range(380000, 450001, 10000)
y_labels = [f'{i//10000} ' for i in y_ticks[:len(tmp_df[-12:]['blood_donors'])]]
plt.yticks(y_ticks[:len(tmp_df[-12:])], y_labels)
plt.ylim(380000, 450000)
plt.grid(axis='y')

plt.savefig(f'../static/images/data/model_graph.png')
plt.close(fig)
