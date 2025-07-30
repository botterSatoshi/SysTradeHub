# NAS
import glob
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import shutil
import pandas as pd

from utils.db_utils import get_encoding


# JAPAN_DAILY_STOCK_PRICES_PATHに保存される毎日の株価データ保存するクラス
class JapanStockDailyQuotes:

    def __init__(self):
        load_dotenv()
        ## 毎日の価格csvデータが保存されるフォルダ
        self.JAPAN_DAILY_STOCK_PRICES_PATH=os.environ['JAPAN_DAILY_STOCK_PRICES_PATH']
        ## 日通し株価四本値
        self.JAPAN_ALL_STOCK_PRICES_PATH=os.environ['JAPAN_ALL_STOCK_PRICES_PATH']
        ## 無効なdbのごみ箱
        self.TRASH_PATH = os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, ".Trash")
        ## バックアップ
        self.BACKUP_PATH = os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, ".Backup")


    ## 毎日の株価データ保存する
    def set_daily_price(self):
        ## 日通し株価四本値csvファイルをすべて取得
        self.db_files = glob.glob(os.path.join(self.JAPAN_ALL_STOCK_PRICES_PATH, '*.csv'))
        ## 毎日の価格csvデータが保存されるファイルをすべて取得
        daily_files = glob.glob(os.path.join(self.JAPAN_DAILY_STOCK_PRICES_PATH, '*.csv'))

        for daily_file in daily_files:
            daily_df = pd.read_csv(daily_file, encoding=get_encoding(daily_file))
            for index, row in daily_df.iterrows():
                # 各行のデータにアクセスする
                row['現在日付'] = pd.to_datetime(row['現在日付'], format='%Y/%m/%d') # 日付の形式を直す
                code =  str.strip(str(row['銘柄コード']))
                db_path = self.get_db_path(code)
                if db_path is None:
                    continue # db がありません。
                print("{}について処理を開始します。".format(code))
                self.set_backup(db_path)
                self.set_daily_quotes(row, db_path)


    ## 前日までの株価が入った日通し株価四本値csvファイルをバックアップフォルダに移動
    def set_backup(self, file_path):
        # ファイル名を取得
        file_name = os.path.basename(file_path)
        # バックアップ先のパスを作成
        backup_path = os.path.join(self.BACKUP_PATH, file_name)
        # ファイルをコピー
        shutil.copy(file_path, backup_path)


    # file_path から code が同じファイルを見つける
    def get_db_path(self ,code: str) -> str:
        for file_path in self.db_files:
            # ファイル名を取得し、拡張子を除去
            file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
            if file_name_without_ext == code:
                self.db_files.remove(file_path)
                return file_path
        return None
    

    def set_daily_quotes(self, row: pd.Series, db_path: str):

        # すでに保存済の csv データを読み込む        
        db_file = pd.read_csv(db_path, encoding=get_encoding(db_path))
        db_file['Date'] = pd.to_datetime(db_file['Date'])
        db_file.set_index('Date', inplace=True)

        # 本日の株価を整理
        df = row.to_frame().T  # SeriesをDataFrameに変換し、転置
        df = df.loc[:, '銘柄コード':] # 銘柄コードより前の列を削除
        daily_df = df.rename(columns={
                '現在日付': 'Date',
                '始値': 'Open',
                '高値': 'High',
                '安値': 'Low',
                '現在値': 'Close',
                '出来高': 'Volume',
                '売買代金': 'TurnoverValue'
            })        
        daily_df['Date'] = pd.to_datetime(daily_df['Date'])
        daily_df.set_index('Date', inplace=True)

        # 行方向の結合
        df = pd.concat([db_file, daily_df], axis=0)
        # インデックスに重複があるかどうかを確認
        if df.index.has_duplicates:
            print("インデックスに重複があります。")
            # 重複するインデックスの特定
            duplicated_index = df.index.duplicated(keep=False)
            # 重複する行に対して、値のある列を選択
            print("")
            #df1_filled = df.fillna(df)
            # 結合の実行
            #result_df = pd.concat([df1_filled, df2[~df2.index.isin(df1.index)]])

        # 'Date'列で降順に並び替え
        df_sorted = df.sort_values(by='Date', ascending=False)
        # 書き込む
        df_sorted.to_csv(db_path)

        print("success:", db_path)



if __name__ == "__main__":
    a = JapanStockDailyQuotes()
    a.set_daily_price()