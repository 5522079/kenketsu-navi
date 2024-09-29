# SARIMAモデルを用いた献血者数の予測

予測結果を以下のサイトで公開しています。<br>
[献血ナビ](https://kenketsu-navi-bvf7hwdne8gyaqav.japaneast-01.azurewebsites.net/)
https://kenketsu-navi-bvf7hwdne8gyaqav.japaneast-01.azurewebsites.net/

また、[Qiita](https://qiita.com/5522079/items/8a6b0ceac8d81f053ca1)にプログラムの詳細な内容を記事にしています。<br>

【プログラム】<br>
- [notebooks](./notebooks/) :　データの分析とモデリングに用いたプログラム<br>
  - [visualization.ipynb](./notebooks/visualization.ipynb) :　生データの可視化と結果の作図<br>
  - [analyze.ipynb](./notebooks/analyze.ipynb) :　変動成分の分解、定常性検定、相関分析と結果の作図<br>
  - [model.ipynb](./notebooks/model.ipynb) :　SARIMAモデルの構築と評価<br>

【データ】<br>
[BloodDonation.csv](./data/BloodDonation.csv) :　2017年1月からの47都道府県ごとの献血者数

![image](https://github.com/user-attachments/assets/980fdd2a-f60d-4f1b-81c7-ff6d273791a0)

1. year

   - 西暦<br><span style="font-size: small">2017 から 2024 までの値をとる。</span>

2. month

   - 月<br><span style="font-size: small">1 から 12 までの値をとる。</span>

3. prefecture_id

   - 各都道府県に割り当てた固有の識別番号。<br><span style="font-size: small">1 から 47 の値をとる。[都道府県番号の早見表](https://tundra-bugle-bc4.notion.site/2f462cc8750948878dbfe143640f33ab?pvs=4)</span>

1. blood_donors

   - 総献血者数

2. whole_blood_donation

   - 全血献血の献血者数<br><span style="font-size: small">200mL 献血者数と 400mL 献血者数の合計。</span>

3. 200mL_blood_donation

   - 200mL 献血者数

4. 400mL_blood_donation

   - 400mL 献血者数

5. component_blood_donation

   - 成分献血の献血者数<br><span style="font-size: small">血漿成分献血者数と血小板成分献血者数の合計。</span>

6. PPP_blood_donation

   - 血漿成分献血献血者数

7.  PC_blood_donation

    - 血小板成分献血者数

これらのデータは[日本赤十字社 数値で見る献血事業](https://www.jrc.or.jp/donation/blood/data/)より取得しています。