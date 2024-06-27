# 献血者予測モデル

作成日：2024年6月<br>

Qiitaに詳細な内容を記事にしていますのでご覧ください。<br>

本プログラムの予測結果は以下のWebサイトにて公開しています。<br>
**献血ナビ** : https://kenketsu-navi-test.azurewebsites.net/

【プログラム】<br>
- note　データの分析とモデリングに用いたプログラム<br>
  - visualization.ipynb　生データの可視化と結果の作図<br>
  - analyze.ipynb　変動成分の分解、定常性検定、相関分析と結果の作図<br>
  - model.ipynb　SARIMAモデルの構築と評価<br>

【サンプルデータ】<br>
BloodDonation.csv　2017年1月からの47都道府県ごとの献血者数
