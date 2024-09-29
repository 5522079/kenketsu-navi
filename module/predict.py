from datetime import datetime

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

file_path = "../data/BloodDonation.csv"

for i in range(1, 48):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime((df['year'].astype(str)) + '-' + (df['month'].astype(str)))
    df = df[df['prefecture_id'] == i]
    grouped_date_total = df.groupby(['date'])['blood_donors'].sum().to_frame()

    # 予測期間のデータフレーム
    latest_date = df['date'].max() # 最新の日付を取得
    start_date = latest_date + pd.DateOffset(months=1) # 予測期間の開始日と終了日を取得
    end_date = latest_date + pd.DateOffset(months=3)
    future_dates = pd.date_range(start_date, end_date, freq='MS') # 予測期間のインデックスを作成
    model_forecast_result = pd.DataFrame(index=future_dates, columns=['blood_donors'])

    # 学習
    train = grouped_date_total
    sarima_model = SARIMAX(train, order=(0, 1, 0), seasonal_order=(0, 1, 0, 12))
    sarima_fit = sarima_model.fit()

    # 予測
    model_forecast_result['blood_donors'] = sarima_fit.forecast(steps=len(model_forecast_result.index))

    # 昨年のデータ
    last_year_data = grouped_date_total[-29:-21]
    last_year_data.index += pd.DateOffset(years=1)

    # 最新のデータ
    latest_data = grouped_date_total[-5:]

    # 予測データ
    model_data = model_forecast_result 
    data = pd.concat([latest_data, model_data])
    donor_data = (pd.concat([last_year_data['blood_donors'], data['blood_donors']])) 
    donor = donor_data.values.tolist()
    donor.insert(0, i)

    with open('./data_8.csv', mode='a')as csvfile:
        if i == 1:
            date = []
            for d in donor_data.index.tolist():
                date.append(f"{d.year}-{d.month}")
            date.insert(0, 'prefecture_id')
            csvfile.write(','.join(map(str, date)))
            csvfile.write('\n')
        csvfile.write(','.join(map(str, donor)))
        csvfile.write('\n')
    print('都道府県コード', i, 'の書き込みが完了しました')