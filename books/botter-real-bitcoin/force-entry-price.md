---
title: "発注から約定まで"
emoji: "🔖"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: []
published: true
---

# Force Entry Price

  
Force Entry Priceは買うと決めてから約定するまで指値で追いかけた場合に、実際に約定する価格です。
私が独自に定義した用語です。
fepと略す場合もあります。
いくらで指値を出すかは外部から与える必要があります。
entryと名前がついていますが、exitも同じ計算なので区別はないです。
以下のコードではcalc_force_entry_priceでForce Entry Priceを計算しています。
コード中のforce_entry_timeは約定するまでにかかった時間です。
fetと略す場合もあります。


具体的には以下のように計算します。
詳細はコードを読んでください。

1. 毎時刻、与えられた指値価格で、指値を出す
2. 指値が約定したら、指値をForce Entry Priceとする
3. 指値が約定しなかったら、次の時刻へ進み、1へ戻る

```python
def calc_force_entry_price(entry_price=None, lo=None, pips=None):

    y = entry_price.copy()

    y[:] = np.nan

    force_entry_time = entry_price.copy()

    force_entry_time[:] = np.nan

    for i in range(entry_price.size):

        for j in range(i + 1, entry_price.size):

            if round(lo[j] / pips) < round(entry_price[j - 1] / pips):

                y[i] = entry_price[j - 1]

                force_entry_time[i] = j - i

                break

    return y, force_entry_time
```