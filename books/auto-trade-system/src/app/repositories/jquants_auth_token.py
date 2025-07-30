# J-Quants
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests
import json
import pandas as pd

# j-Quants api を用いて日本株情報を取得、保存するクラス
class JQuantsAuthToken:

    def __init__(self):
        load_dotenv() # .envファイルから環境変数を読み込む
        self.REFRESH_TOKEN = self.get_reflesh_token()
        self.ID_TOKEN = self.get_id_token()

    # リフレッシュトークンを取得します。
    # 本APIにより取得するリフレッシュトークンの有効期間は１週間です。
    def get_reflesh_token(self):
       
        self.REFRESH_TOKEN_URL = "https://api.jquants.com/v1/token/auth_user"

        body = json.dumps({
            "mailaddress": os.environ['JQUANTS_MAIL'],
            "password": os.environ['JQUANTS_PASSWORD']
        })

        response = requests.post(
            self.REFRESH_TOKEN_URL,
            data=body,
            headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            raise Exception(response)

        jsonResponse = response.json()
        refreshToken = jsonResponse["refreshToken"]
            
        return refreshToken


    # IDトークンを取得します。
    def get_id_token(self):
        """
        リフレッシュトークンを用いてIDトークンを取得することができます。
        IDトークンの有効期間は24時間です。
        """
        self.ID_TOKEN_URL_BASE = "https://api.jquants.com/v1/token/auth_refresh?refreshtoken="

        response = requests.post(
            self.ID_TOKEN_URL_BASE + self.REFRESH_TOKEN,
            headers={"Content-Type": "application/json"})
        
        if response.status_code != 200:
            raise Exception(response)

        jsonResponse = response.json()
        idToken = jsonResponse["idToken"]
            
        return idToken
        
