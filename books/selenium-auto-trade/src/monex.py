#
# マネックス証券サイトへログイン
#

import json
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# 設定ファイルを取得
login_info = json.load(open("login_info.json", "r", encoding="utf-8"))

# ログインサイト名
site_name = "sec_monex"

# ログイン画面URL
url_login = login_info[site_name]["url"]

# ユーザー名とパスワードの指定
USER = login_info[site_name]["id"]
PASS = login_info[site_name]["pass"]

# Firefoxのヘッドレスモードを有効にする
options = FirefoxOptions()
options.add_argument('--headless')

# Firefoxを起動する
browser = Firefox(options=options)

# ログイン画面取得
browser.get(url_login)

# 入力
e = browser.find_element_by_id("loginid")
e.clear()
e.send_keys(USER)
e = browser.find_element_by_id("passwd")
e.clear()
e.send_keys(PASS)

# ログイン
button = browser.find_element_by_xpath("//form[@id='contents']/div/p/input")
button.click()

# ページロード完了まで待機
WebDriverWait(browser, 10).until(
    ec.presence_of_element_located((By.CLASS_NAME, "user-info"))
)

# ログインできたか確認（画面キャプチャ取る）
browser.save_screenshot("../screenshots/sec_monex/home.png")

browser.quit()
