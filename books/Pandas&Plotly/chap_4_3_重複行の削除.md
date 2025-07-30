---
title: 重複行の削除
free: true
---
レコードが重複していないことが前提の表形式データでも、記録時のトラブルやヒュー マンエラーによって重複した行が存在することがあります。また、複数の表形式データ を結合した際にバグなどによって重複行が発生する場合もありえるでしょう。本節では 重複行の確認方法と重複行を削除する方法について紹介します。重複行を含んだ状態 で可視化を行うと、データ理解の妨げになる場合があります。

サンプルデータ

|     | A   | B   | C    |
| --- | --- | --- | ---- |
| 0   | 10  | 100 | 1000 |
| 1   | 20  | 100 | 1000 |
| 2   | 20  | 200 | 1000 |
| 3   | 30  | 300 | 2000 |
| 4   | 40  | 300 | 3000 |
| 5   | 40  | 300 | 3000 |
| 6   | 40  | 300 | 3000 |

## 重複行の判定
最初に本節でサンプルとして扱う表形式データを作成します。「A」「B」 「C」それぞ れの列で重複した値が存在しています。また、行番号 「4」から「6」ではすべての列の 値が一致しています。


重複行を確認するには、DataFrameのduplicatedメソッドを使用します。 duplicated メソッドは重複した行にTrue、そうではない行にFalseのブール値を出力 するメソッドです。標準ではすべての列の値が一致した行を重複行と見なします。引 数keepに'first'を指定すると重複する行の中で先頭をFalseに、'last'を指定すると末 尾行をFalseにします。省略時は'first'が適用されます。
```python
df.duplicated()     # duplicated(keep='first')と同じ
```
>0    False
>1    False
>2    False
>3    False
>4    False
>5     True
>6     True
>dtype: bool


引数keepにFalse を指定すると、重複する行がすべてTrueとなります。なおkeep = True を指定することはできません。
```python
df.duplicated(keep=False)
```
>0    False
>1    False
>2    False
>3    False
>4     True
>5     True
>6     True
>dtype: bool

重複行の判定にすべての列の値を用いるのではなく、特定の列で判定することも 可能です。重複判定に用いる列を指定するには、引数subsetに列名を指定します。 引数 subset は引数 keepと併用することが可能です。
```python
df.duplicated(subset='A')
```
>0    False
>1    False
>2     True
>3    False
>4    False
>5     True
>6     True
>dtype: bool

```python
df.duplicated(subset='C', keep='last')
```
>0     True
>1     True
>2    False
>3    False
>4     True
>5     True
>6    False
>dtype: bool


引数 subset は複数列の組み合わせで指定することもできます。指定した複数列の 値がすべて一致した行がTrueとなります。複数列を指定する場合は列名のlistで指 定します。
```python
df.duplicated(subset=['A', 'B'], keep='last')
```
>0    False
>1    False
>2    False
>3    False
>4     True
>5     True
>6    False
>dtype: bool

## 重複行の削除
重複行を削除するには、DataFrameのdrop_duplicates メソッドを使用します。引 数keepで重複行から残す行を指定します。省略時は'first'が適用されます。
```python
df_drop = df.drop_duplicates()  # drop_duplicates(keep='first')と同じ

df_drop
```

|     | A   | B   | C    |
| --- | --- | --- | ---- |
| 0   | 10  | 100 | 1000 |
| 1   | 20  | 100 | 1000 |
| 2   | 20  | 200 | 1000 |
| 3   | 30  | 300 | 2000 |
| 4   | 40  | 300 | 3000 |

drop_duplicates メソッドも引数subsetで重複判定に使用する列を指定可能です。 引数subset を指定しなかった場合、引数keepをどのように指定しても同じ結果の表 が得られます(重複した行の先頭を残しても末尾を残しても同じです)。引数 subset で列を指定した場合、引数keepの指定によって結果が変わる場合があります。
例えば、以下の例では引数subsetに「A」列を指定しており、引数 keepが'first'で も'last'でも「A」列の結果は同じです。一方で他の列は値が異なる可能性があり、 'first'と'last'で「B」列の結果が変わっています。

```python
df_drop = df.drop_duplicates(subset='A', keep='first')

df_drop
```

| |A|B|C|
|---|---|---|---|
|0|10|100|1000|
|1|20|100|1000|
|3|30|300|2000|
|4|40|300|3000|
```python
df_drop = df.drop_duplicates(subset='A', keep='last')

df_drop
```

| |A|B|C|
|---|---|---|---|
|0|10|100|1000|
|2|20|200|1000|
|3|30|300|2000|
|6|40|300|3000|

drop_duplicatesメソッドもsubsetに複数列をlistで指定できます。
```python
df_drop = df.drop_duplicates(subset=['B', 'C'], keep='last')

df_drop
```

| |A|B|C|
|---|---|---|---|
|1|20|100|1000|
|2|20|200|1000|
|3|30|300|2000|
|6|40|300|3000|

drop_duplicates メソッドも dropnaメソッドと同様に、結果の行番号は削除前の行 番号を引き継ぎます。drop_duplicatesメソッドは引数ignore_indexにTrueを指定 することで結果の行番号を振りなおすことが可能です。

```python
df_drop = df.drop_duplicates(
    subset='A',
    keep='first',
    ignore_index=True
)

df_drop
```

|     | A   | B   | C    |
| --- | --- | --- | ---- |
| 0   | 10  | 100 | 1000 |
| 1   | 20  | 100 | 1000 |
| 2   | 30  | 300 | 2000 |
| 3   | 40  | 300 | 3000 |



#
---
## sample code
> [section_4_3.ipynb](books/Pandas&Plotly/src/notebook/section_4_3.ipynb)

