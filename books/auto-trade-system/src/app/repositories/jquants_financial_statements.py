# J-Quants
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests
import json
import pandas as pd

from repositories.jquants_auth_token import JQuantsAuthToken

# j-Quants api を用いて財務情報を取得、保存するクラス
class JapanFinancialStatements:

    def __init__(self, idToken: str):
        self.ID_TOKEN = idToken
 

    def set_financial_statements(self):
        self.STATEMENTS_URL = "https://api.jquants.com/v1/fins/statements"

        today_date = datetime.now().strftime('%Y%m%d') # 今日の日付を取得し、フォーマット

        response = requests.get(
            self.STATEMENTS_URL + "?date={}".format(today_date),
            headers={'Authorization': 'Bearer {}'.format(self.ID_TOKEN)})

        if response.status_code != 200:
            raise Exception(response)
        
        jsonResponse = response.json()
        statements = jsonResponse["statements"]
        if len(statements) == 0:
            return None

        # DataFrameに変換
        df = pd.DataFrame(statements) 

        # 書き込む
        JAPAN_ALL_STOCK_FINANCIAL_RESULTS_PATH = os.environ['JAPAN_ALL_STOCK_FINANCIAL_RESULTS_PATH']
        file_name = f"japan_financial_statements_{today_date}.csv" # ファイル名を生成
        full_path = os.path.join(JAPAN_ALL_STOCK_FINANCIAL_RESULTS_PATH, file_name) # フルパスを生成
        df.to_csv(full_path)

        return df
    

if __name__ == "__main__":
    a = JQuantsAuthToken()
    b = JapanFinancialStatements(a.ID_TOKEN)
    b.set_financial_statements()