# J-Quants
"""
日通し株価四本値の更新が遅れた場合に、すでに存在するcsvファイルに
今日までの価格を追加する
上場銘柄一覧にない名側はTrashフォルダに移動
"""
import glob
import os
from datetime import datetime
import requests
import pandas as pd
import chardet
import shutil

# トークンの読み込み
from repositories.jquants import JapanStockDataHandler
_super = JapanStockDataHandler()

# ファイルをバイナリモードで読み込み、エンコーディングを検出
def get_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding
    

## 上場銘柄一覧
JAPAN_ALL_STOCK_DATA_PATH = os.environ['JAPAN_ALL_STOCK_DATA_PATH']
# 'japan_listed_stocks'を含むファイルをすべて取得
files = glob.glob(os.path.join(JAPAN_ALL_STOCK_DATA_PATH, 'japan_listed_stocks*'))
# 日付を抽出して最も新しいファイルを選ぶ
latest_file = max(files, key=lambda path: datetime.strptime(os.path.basename(path).split('_')[-1].split('.')[0], '%Y%m%d'))
# 検出されたエンコーディングを使用してCSVを読み込む
df_listed_stocks = pd.read_csv(latest_file, encoding=get_encoding(latest_file))


# 保存済の日通し株価四本値
JAPAN_ALL_STOCK_PRICES_PATH = os.environ['JAPAN_ALL_STOCK_PRICES_PATH']
# 'japan_listed_stocks'を含むファイルをすべて取得
files = glob.glob(os.path.join(JAPAN_ALL_STOCK_PRICES_PATH, '*.csv'))

# 新しく日通し株価四本値を取得して保存
TRASH_PATH = JAPAN_ALL_STOCK_PRICES_PATH + "\\.Trash"
DAILY_QUOTES_URL = "https://api.jquants.com/v1/prices/daily_quotes"

headers = {'Authorization': 'Bearer {}'.format(_super.ID_TOKEN)}

for file in files:
    # すでに保存しているファイル
    file_name = os.path.basename(file)
    code = os.path.splitext(file_name)[0]
    if df_listed_stocks['Code'].str.contains(code).any():
        # すでに保存している株価情報 df_stock_price
        df2 = pd.read_csv(file, encoding=get_encoding(file))
        if len(df2.columns) == 7:
            df2.columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'AdjustmentClose']
        df2['Date'] = pd.to_datetime(df2['Date']) # 'Date'列をdatetime型に変換
        df2.set_index('Date', inplace=True) # 'Date'列をインデックスに設定

        # 新しい株価情報 df
        response = requests.get(DAILY_QUOTES_URL + "?code={}".format(code), headers=headers)
        jsonResponse = response.json()
        daily_quotes = jsonResponse["daily_quotes"]
        if len(daily_quotes) == 0:
            continue
        df1 = pd.DataFrame(daily_quotes) 
        df1 = df1.drop(columns='Code')
        df1['Date'] = pd.to_datetime(df1['Date']) # 'Date'列をdatetime型に変換
        df1.set_index('Date', inplace=True) # 'Date'列をインデックスに設定

        # df1のインデックスにある行をdf2から削除
        df3 = df2.drop(df1.index, errors='ignore')
        # 行方向の結合
        df4 = pd.concat([df1, df3], axis=0)
        # 'Date'列で降順に並び替え
        df_sorted = df4.sort_values(by='Date', ascending=False)
        # 書き込む
        df_sorted.to_csv(file)

        print("success:", file_name)

    else:
        # ファイルを移動
        destination_path = os.path.join(TRASH_PATH, file_name)
        shutil.move(file, destination_path)
        print("trash:", file_name)



