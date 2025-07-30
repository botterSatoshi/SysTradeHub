import chardet

# ファイルをバイナリモードで読み込み、エンコーディングを検出
def get_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding