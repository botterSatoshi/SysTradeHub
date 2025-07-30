# J-Quants
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests
import json
import pandas as pd

from repositories.jquants_auth_token import JQuantsAuthToken

# j-Quants api を用いて決算発表予定日を取得、保存するクラス
class JapanFinancialAnnouncement:

    def __init__(self, idToken: str):
        self.ID_TOKEN = idToken

    
    def set_financial_announcement(self):

        self.ANNOUNCEMENT_URL = "https://api.jquants.com/v1/fins/announcement"

        response = requests.get(
            self.ANNOUNCEMENT_URL,
            headers={'Authorization': 'Bearer {}'.format(self.ID_TOKEN)})

        if response.status_code != 200:
            raise Exception(response)
        
        jsonResponse = response.json()
        announcement = jsonResponse["announcement"]
        if len(announcement) == 0:
            return None

        # DataFrameに変換
        df = pd.DataFrame(announcement)  

        # 書き込む
        JAPAN_ALL_STOCK_FINANCIAL_RESULTS_PATH = os.environ['JAPAN_ALL_STOCK_FINANCIAL_RESULTS_PATH']
        today_date = datetime.now().strftime('%Y%m%d') # 今日の日付を取得し、フォーマット
        file_name = f"japan_financial_announcement_{today_date}.csv" # ファイル名を生成
        full_path = os.path.join(JAPAN_ALL_STOCK_FINANCIAL_RESULTS_PATH, file_name) # フルパスを生成
        df.to_csv(full_path)

        return df


    

if __name__ == "__main__":
    a = JQuantsAuthToken()
    b = JapanFinancialAnnouncement(a.ID_TOKEN)
    b.set_financial_announcement()