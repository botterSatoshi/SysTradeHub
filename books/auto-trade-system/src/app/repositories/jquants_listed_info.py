# J-Quants
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests
import json
import pandas as pd

# j-Quants api を用いて上場銘柄一覧を取得、保存するクラス
class JapanStockListedInfo:

    def __init__(self, idToken: str):
        self.ID_TOKEN = idToken


    def set_listed_stocks(self):

        self.LISTED_URL = "https://api.jquants.com/v1/listed/info"

        response = requests.get(
            self.LISTED_URL,
            headers={'Authorization': 'Bearer {}'.format(self.ID_TOKEN)})

        if response.status_code != 200:
            raise Exception(response)
        
        jsonResponse = response.json()
        listed = jsonResponse["info"]

        # DataFrameに変換し、'Date'列をインデックスとして設定
        df = pd.DataFrame(listed)  

        # 書き込む
        JAPAN_ALL_STOCK_DATA_PATH = os.environ['JAPAN_ALL_STOCK_DATA_PATH']
        today_date = datetime.now().strftime('%Y%m%d') # 今日の日付を取得し、フォーマット
        file_name = f"japan_listed_stocks_{today_date}.csv" # ファイル名を生成
        full_path = os.path.join(JAPAN_ALL_STOCK_DATA_PATH, file_name) # フルパスを生成
        df.to_csv(full_path)

        return df

