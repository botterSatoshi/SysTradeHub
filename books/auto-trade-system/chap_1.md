---
title: J-Quants API の使い方
free: true
---

# J-Quants API の使い方

認証は以下の手順を踏む **1.** と **2.** で2回 トークンを取得する点が珍しいところだろう

1. Web画面かAPIでリフレッシュトークンを取得する。
- メールアドレスとパスワードを用いて
2. リフレッシュトークンを用いて専用APIでIDトークンを取得する。
3.  IDトークンを用いて、各種情報を取得するAPIを利用する。

## Web画面かAPIでリフレッシュトークンを取得する。

### Web画面にサインイン

https://jpx-jquants.com/

![](images/Pasted-image-20230606122151.png)

![](images/Pasted-image-20230606122302.png)

### API でトークン取得する場合

```python
import requests
import json

data={"mailaddress":"<YOUR EMAIL_ADDRESS>", "password":"<YOUR PASSWORD>"}
r_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
r_post.json()
```

## リフレッシュトークンを用いて専用APIでIDトークンを取得する。

リフレッシュトークンを用いてIDトークンを取得することができます。

```python
import requests
import json

REFRESH_TOKEN = "YOUR refreshtokenID"
r_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={REFRESH_TOKEN}")
r_post.json()
```

## 上場銘柄一覧 の取得

上場企業の情報を取得する事ができます

```
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/listed/info", headers=headers)
r.json()
```


### データ項目概要

|変数名|説明|型|備考|
|---|---|---|---|
|Date|情報適用年月日|String|YYYY-MM-DD|
|Code|銘柄コード|String||
|CompanyName|会社名|String||
|CompanyNameEnglish|会社名（英語）|String||
|Sector17Code|17業種コード|String|[17業種コード及び業種名](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info/sector17code)を参照|
|Sector17CodeName|17業種コード名|String|[17業種コード及び業種名](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info/sector17code)を参照|
|Sector33Code|33業種コード|String|[33業種コード及び業種名](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info/sector33code)を参照|
|Sector33CodeName|33業種コード名|String|[33業種コード及び業種名](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info/sector33code)を参照|
|ScaleCategory|規模コード|String||
|MarketCode|市場区分コード|String|[市場区分コード及び市場区分](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info/marketcode)を参照|
|MarketCodeName|市場区分名|String|[市場区分コード及び市場区分](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info/marketcode)を参照|


## [株価四本値(/prices/daily_quotes)](https://jpx.gitbook.io/j-quants-ja/api-reference/daily_quotes)

```python
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/prices/daily_quotes?code=86970&date=20230324", headers=headers)
r.json()
```

### データ項目概要

|変数名|説明|型|備考|
|---|---|---|---|
|Date|日付|String|YYYY-MM-DD|
|Code|銘柄コード|String||
|Open|始値（調整前）|Number||
|High|高値（調整前）|Number||
|Low|安値（調整前）|Number||
|Close|終値（調整前）|Number||
|Volume|取引高（調整前）|Number||
|TurnoverValue|取引代金|Number||
|AdjustmentFactor|調整係数|Number|株式分割1:2の場合、権利落ち日のレコードにおいて本項目に”0 .5”が収録されます。|
|AdjustmentOpen|調整済み始値|Number|※1|
|AdjustmentHigh|調整済み高値|Number|※1|
|AdjustmentLow|調整済み安値|Number|※1|
|AdjustmentClose|調整済み終値|Number|※1|
|AdjustmentVolume|調整済み取引高|Number|※1|
|MorningOpen|前場始値|Number|※2|
|MorningHigh|前場高値|Number|※2|
|MorningLow|前場安値|Number|※2|
|MorningClose|前場終値|Number|※2|
|MorningVolume|前場売買高|Number|※2|
|MorningTurnoverValue|前場取引代金|Number|※2|
|MorningAdjustmentOpen|調整済み前場始値|Number|※1, ※2|
|MorningAdjustmentHigh|調整済み前場高値|Number|※1, ※2|
|MorningAdjustmentLow|調整済み前場安値|Number|※1, ※2|
|MorningAdjustmentClose|調整済み前場終値|Number|※1, ※2|
|MorningAdjustmentVolume|調整済み前場売買高|Number|※1, ※2|
|AfternoonOpen|後場始値|Number|※2|
|AfternoonHigh|後場高値|Number|※2|
|AfternoonLow|後場安値|Number|※2|
|AfternoonClose|後場終値|Number|※2|
|AfternoonVolume|後場売買高|Number|※2|
|AfternoonAdjustmentOpen|調整済み後場始値|Number|※1, ※2|
|AfternoonAdjustmentHigh|調整済み後場高値|Number|※1, ※2|
|AfternoonAdjustmentLow|調整済み後場安値|Number|※1, ※2|
|AfternoonAdjustmentClose|調整済み後場終値|Number|※1, ※2|
|AfternoonAdjustmentVolume|調整済み後場売買高|Number|※1, ※2|

※1 過去の分割等を考慮した調整済みの項目です ※2 Premiumプランのみ取得可能な項目です


#
---
## sample code
>