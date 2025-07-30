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
from repositories.jquants_auth_token import JQuantsAuthToken
from utils.db_utils import get_encoding

# j-Quants api を用いて取引カレンダー（営業日）を取得するクラス
class JapanAllStockData:

    def __init__(self, idToken: str):
        self.ID_TOKEN = idToken    
        ## 上場銘柄一覧
        self.JAPAN_ALL_STOCK_DATA_PATH = os.environ['JAPAN_ALL_STOCK_DATA_PATH']
        # 保存済の日通し株価四本値
        self.JAPAN_ALL_STOCK_PRICES_PATH = os.environ['JAPAN_ALL_STOCK_PRICES_PATH']
        # 新しく日通し株価四本値を取得して保存
        self.TRASH_PATH = os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, ".Trash")
        self.DAILY_QUOTES_URL = "https://api.jquants.com/v1/prices/daily_quotes"

    def get_listed_stocks(self):
        # 'japan_listed_stocks'を含むファイルをすべて取得
        files = glob.glob(os.path.join(self.JAPAN_ALL_STOCK_DATA_PATH, 'japan_listed_stocks*'))
        # 日付を抽出して最も新しいファイルを選ぶ
        latest_file = max(files, key=lambda path: datetime.strptime(os.path.basename(path).split('_')[-1].split('.')[0], '%Y%m%d'))
        # 検出されたエンコーディングを使用してCSVを読み込む
        df_listed_stocks = pd.read_csv(latest_file, encoding=get_encoding(latest_file))

        return df_listed_stocks

    # すでに csv ファイルがある銘柄について 足りない日次を追加する
    def set_already_stock_data(self):
        # 'japan_listed_stocks'を使用してCSVを読み込む
        df_listed_stocks = self.get_listed_stocks()

        # 'japan_listed_stocks'を含むファイルをすべて取得
        files = glob.glob(os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, '*.csv'))

        headers = {'Authorization': 'Bearer {}'.format(self.ID_TOKEN)}

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
                response = requests.get(self.DAILY_QUOTES_URL + "?code={}".format(code), headers=headers)
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
                destination_path = os.path.join(self.TRASH_PATH, file_name)
                shutil.move(file, destination_path)
                print("trash:", file_name)

    # csv ファイルがない銘柄を取得する
    def set_enough_stock_data(self):
        # 'japan_listed_stocks'を使用してCSVを読み込む
        df_listed_stocks = self.get_listed_stocks()

        # 'japan_listed_stocks'を含むファイルをすべて取得
        files = glob.glob(os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, '*.csv'))
        already_codes = [os.path.splitext(os.path.basename(file))[0] for file in files]

        headers = {'Authorization': 'Bearer {}'.format(self.ID_TOKEN)}

        for index, row in df_listed_stocks.iterrows():
            code = str(row['Code'])

            if code in already_codes:
                already_codes.remove(code)
                continue

            # 株価を取得する
            print("{} を取得します.".format(code))
            response = requests.get(self.DAILY_QUOTES_URL + "?code={}".format(code), headers=headers)
            jsonResponse = response.json()
            daily_quotes = jsonResponse["daily_quotes"]
            if len(daily_quotes) == 0:
                continue
            df = pd.DataFrame(daily_quotes) 
            df = df.drop(columns='Code')
            df['Date'] = pd.to_datetime(df['Date']) # 'Date'列をdatetime型に変換
            df.set_index('Date', inplace=True) # 'Date'列をインデックスに設定
            # 'Date'列で降順に並び替え
            df_sorted = df.sort_values(by='Date', ascending=False)
            # 書き込む
            df_sorted.to_csv(os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, "{}.csv".format(code)))

            print("success:", code)

        print(already_codes)


    # 4桁の code.csv を 5桁の code.csv に変える
    def set_code(self):
        # 'japan_listed_stocks'を使用してCSVを読み込む
        df_listed_stocks = self.get_listed_stocks()

        # 'japan_listed_stocks'を含むファイルをすべて取得
        files = glob.glob(os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, '*.csv'))
        already_codes = [os.path.splitext(os.path.basename(file))[0] for file in files]

        for index, row in df_listed_stocks.iterrows():        
            code = str(row['Code'])
            code4 = code
            if len(code4) > 4:
                code4 = code4[:4]

            if code4 in already_codes:
                i = already_codes.index(code4)
                target_file = files[i]
                folder_path = os.path.dirname(target_file)
                new_file = os.path.join(folder_path, code) + ".csv"
                # ファイルが存在するかどうかを判定
                if os.path.exists(new_file):
                    print("{}ファイルは存在します。".format(code))
                    continue
                # ファイルをリネーム
                print("rename: {}->{}".format(target_file, new_file))
                os.rename(target_file, new_file)

                
    # def move_done_file(self):
    #     # 'japan_listed_stocks'を含むファイルをすべて取得
    #     files = glob.glob(os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, '*.csv'))
    #     already_codes = [os.path.splitext(os.path.basename(file))[0] for file in files]

    #     DONE_PATH = os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, 'done') 

    #     for i in range(len(already_codes)):
    #         code = already_codes[i]
    #         if len(code) > 4:
    #             shutil.move(files[i], DONE_PATH)
    #             continue


    
if __name__ == "__main__":

    a = JQuantsAuthToken()
    b = JapanAllStockData(a.ID_TOKEN)
    b.set_enough_stock_data()

    # b.set_code()

    # b.move_done_file()

