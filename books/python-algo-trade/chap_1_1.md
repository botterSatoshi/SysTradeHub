---
title: chap_1_1
free: true
---
## 2024.10 quandl は使えない

本書に記載の下記のコードは動かない
```python
import quandl as q
q.ApiConfig.api_key = c['quandl']['api_key']
d = q.get('BCHAIN/MKPRU')
d['SMA'] = d['Value'].rolling(100).mean()
d.loc['2013-1-1':].plot(title='BTC/USD exchange rate',
                        figsize=(10, 6));
```
>QuandlError: (Status 410) Something went wrong. Please try again. If you continue to have problems, please contact us at connect@quandl.com.
>Output is truncated. View as a [scrollable element](command:cellOutput.enableScrolling?f564612b-afb2-493f-899d-1d8f0b7c29d1) or open in a [text editor](command:workbench.action.openLargeOutput?f564612b-afb2-493f-899d-1d8f0b7c29d1). Adjust cell output [settings](command:workbench.action.openSettings?%5B%22%40tag%3AnotebookOutputLayout%22%5D)...

以下のように修正する
↓



以後、import quandl を使う部分は置き換えて読む必要がある


#
---
## sample code
>![[books/pythonからはじめるアルゴリズムトレード/src/ch01/01_pyalgo.ipynb]]