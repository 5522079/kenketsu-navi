import pandas as pd

file_path = "data/BloodDonation.csv"
df = pd.read_csv(file_path)

prefecture_id = 12
if prefecture_id != 0:
    pref_df = df[df['prefecture_id'] == prefecture_id] 
    print('献血に協力していただいた人数')
    print(sum(pref_df['blood_donors']), '人')
    print('献血でいただいた血液の総量')
    print((sum(pref_df['200mL_blood_donation']) * 200 + sum(pref_df['400mL_blood_donation']) * 400) / 1000, 'kL')
else:
    pref_df = df[df['prefecture_id'] == prefecture_id] 
    print('献血に協力していただいた人数')
    print(sum(df['blood_donors']), '人')
    print('献血でいただいた血液の総量')
    print((sum(df['200mL_blood_donation']) * 200 + sum(df['400mL_blood_donation']) * 400) / 1000, 'kL')