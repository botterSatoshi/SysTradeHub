# J-Quants
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests
import pandas as pd

from repositories.jquants_auth_token import JQuantsAuthToken

# j-Quants api を用いて取引カレンダー（営業日）を取得するクラス
class JapanTradingCalendar:

    def __init__(self, idToken: str):
        self.ID_TOKEN = idToken


    def set_trading_calendar(self):
        # 営業日の取得
        self.CALENDAR_URL = "https://api.jquants.com/v1/markets/trading_calendar"

        response = requests.get(
            self.CALENDAR_URL, # + "?holidaydivision=1",
            headers={'Authorization': 'Bearer {}'.format(self.ID_TOKEN)})

        if response.status_code != 200:
            raise Exception(response)
        
        jsonResponse = response.json()
        calendar = jsonResponse["trading_calendar"]

        # DataFrameに変換し、'Date'列をインデックスとして設定
        df = pd.DataFrame(calendar)  
        df['Date'] = pd.to_datetime(df['Date']) # 'Date'列をdatetime型に変換
        df.set_index('Date', inplace=True) # 'Date'列をインデックスに設定

        # 書き込む
        JAPAN_ALL_STOCK_DATA_PATH = os.environ['JAPAN_ALL_STOCK_DATA_PATH']
        today_date = datetime.now().strftime('%Y%m%d') # 今日の日付を取得し、フォーマット
        file_name = f"japan_trading_calendar_{today_date}.csv" # ファイル名を生成
        full_path = os.path.join(JAPAN_ALL_STOCK_DATA_PATH, file_name) # フルパスを生成
        df.to_csv(full_path)

        return df
        

    
if __name__ == "__main__":
    a = JQuantsAuthToken()
    b = JapanTradingCalendar(a.ID_TOKEN)
    b.set_trading_calendar()