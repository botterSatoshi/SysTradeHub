---
title: 欠損値の表現とその確認方法
free: true
---
欠損値の有無を把握しておくことは重要です。

- `NaN`,`nan`,`NA`：値として使用できない非数を意味する
- `#N/A`,`N/A`：未定義を意味する
- `null`, `NULL`：欠損値を表す

サンプルデータ

|     | A   | B    | C    | D    | E    |
| --- | --- | ---- | ---- | ---- | ---- |
| 0   | 11  | 12.0 | 13.0 | 14.0 | 15   |
| 1   | 21  | NaN  | NaN  | NaN  | NAN  |
| 2   | 31  | 32.0 | NaN  | NaN  | na   |
| 3   | 41  | 42.0 | NaN  | 44.0 | Null |
| 4   | 51  | 52.0 | NaN  | 54.0 | 55   |
| 5   | 61  | 62.0 | NaN  | 64.0 | 65   |
| 6   | 71  | 72.0 | 73.0 | 74.0 | 75   |
## E列が欠損値を含んでいない？
下記は欠損値として扱われない
 - `NAN`
 - `na`
 - `Null`

df.infoで各列の欠損値ではない要素の数を確認できます。
```python
df.info()
```
><class 'pandas.core.frame.DataFrame'>
>RangeIndex: 7 entries, 0 to 6
>Data columns (total 5 columns):
> #   Column  Non-Null Count  Dtype  
>-- 
> 0   A       7 non-null      int64  
> 1   B       6 non-null      float64
> 2   C       2 non-null      float64
> 3   D       5 non-null      float64
> 4   E       7 non-null      object 
>dtypes: float64(3), int64(1), object(1)
>memory usage: 408.0+ bytes

上記で示した通り E列に欠損値は無い判定になっています。
データ型に注目してみるとE列はobject型を判定され`NAN`, `na`, `Null` が文字列として扱われていることがわかります。

## 欠損値の位置と個数

欠損値の位置を確認するには、DataFrameの**isnaメソッド**を使用します。
isnaメソッドは欠損値の位置はtrue、それ以外はfalseのDataFrameを返します。
**isnullメソッド**は**isnaメソッド**の別名で同じです。

```python
df.isna()   # df.isnull()でも同一
```

| |A|B|C|D|E|
|---|---|---|---|---|---|
|0|False|False|False|False|False|
|1|False|True|True|True|False|
|2|False|False|True|True|False|
|3|False|False|True|False|False|
|4|False|False|True|False|False|
|5|False|False|True|False|False|
|6|False|False|False|False|False|
### 列ごとの欠損値は axis=0 にして sum
```python
df.isna().sum(axis=0)
```
>A    0
>B    1
>C    5
>D    2
>E    0
>dtype: int64

### 行ごとの欠損値は axis=1 にして sum
```python
df.isna().sum(axis=1)
```
>0    0
>1    3
>2    2
>3    1
>4    1
>5    1
>6    0
>dtype: int64


## 無効値から欠損値への置き換え
「NAN」 「na」 「Null」のように、無効値として表現したつもりの文字列がpandasで は無効値としてインポートできない場合があります。また、数値データにおいて、正 常値が取りえるはずのない値を例外コードとすることで欠損値を表現するケースも あります。例えば正常値が0から1,023までの値を取りえる数値データにおいて、 「-1」や「9999」などの数値を例外コードにするケースなどが考えられるでしょう。こ のように欠損値として意図していた値が有効値としてインポートされてしまった場 合は、DataFrameのreplace メソッドを使って、欠損値に置換することができます。
replace メソッドは、第一引数に置換前の値、第二引数に置換後の値を指定します。 ここでは「E」列の「NAN」を欠損値に置換します。置換後の値にはNumPyのnan (np. nan)を指定します。

```python
df_replace = df.replace('NAN', np.nan)

df_replace
```

| |A|B|C|D|E|
|---|---|---|---|---|---|
|0|11|12.0|13.0|14.0|15|
|1|21|NaN|NaN|NaN|NaN|
|2|31|32.0|NaN|NaN|na|
|3|41|42.0|NaN|44.0|Null|
|4|51|52.0|NaN|54.0|55|
|5|61|62.0|NaN|64.0|65|
|6|71|72.0|73.0|74.0|75|

複数の値を一度に置換するには、第1引数にdictを指定します。
```python
df_replace = df.replace({
    'NAN': np.nan,
    'na': np.nan
})

df_replace
```

複数置換するもう1つの方法は、第一引数に置換前の値のlistを、第二引数に置換 後の値のlistを指定する方法です。
```python
df.replace(
    ['NAN', 'na'],
    [np.nan, np.nan]
)

df_replace
```

| |A|B|C|D|E|
|---|---|---|---|---|---|
|0|11|12.0|13.0|14.0|15|
|1|21|NaN|NaN|NaN|NaN|
|2|31|32.0|NaN|NaN|NaN|
|3|41|42.0|NaN|44.0|Null|
|4|51|52.0|NaN|54.0|55|
|5|61|62.0|NaN|64.0|65|
|6|71|72.0|73.0|74.0|75|
replace メソッドには正規表現を使用することも可能です。正規表現を使用する場 合は、引数regexにTrueを指定します。正規表現そのものについての解説は他の書 籍に譲りますが、ここでは正規表現を使って「NAN」 「na」 「Null」いずれでも例外値 に置換を行っています。
```python
df_replace = df.replace(r'NAN|na|Null', np.nan, regex=True)

df_replace
```

| |A|B|C|D|E|
|---|---|---|---|---|---|
|0|11|12.0|13.0|14.0|15|
|1|21|NaN|NaN|NaN|NaN|
|2|31|32.0|NaN|NaN|NaN|
|3|41|42.0|NaN|44.0|NaN|
|4|51|52.0|NaN|54.0|55|
|5|61|62.0|NaN|64.0|65|
|6|71|72.0|73.0|74.0|75|
## 欠損値や代入やインポート
DataFrameにNoneやpandas.NA, numpy.nanm float('nan')を代入した場合は欠損値として扱われます。
```python
df.loc[1, 'B'] = None
df.loc[2, 'B'] = np.nan
df.loc[3, 'B'] = pd.NA
df.loc[4, 'B'] = float('nan')

df
```

|     | A   | B    |
| --- | --- | ---- |
| 0   | 1   | 7.0  |
| 1   | 2   | NaN  |
| 2   | 3   | NaN  |
| 3   | 4   | NaN  |
| 4   | 5   | NaN  |
| 5   | 6   | 12.0 |

インポートの際と同様に、欠損値を代入した列のデータ型は自動的にfloat64 変更される点に注意してください。 なっています。pandas.NA そのため、欠損値はfloat64型のnumpy.nan と や float(nan)で代入した場合も同様です。
```python
df.info()
```
> 0   A       6 non-null      int64
> 1   B       6 non-null      **int64**
>dtypes: int64(2)

↓

> 0   A       6 non-null      int64  
> 1   B       2 non-null      **float64**
>dtypes: float64(1), int64(1)


DataFrameのデータ型をfloat32に変換すると、 欠損値はfloat32型のnumpy.nan DataFrameのデータ型をfloat32に変換すると、に変化します。
```python
df_float32 = df.astype('float32')

df_float32.info()
```
> 0   A       6 non-null      float32
> 1   B       2 non-null      **float32**
>dtypes: float32(2)



#
---
## sample code
> [section_4_1.ipynb](books/Pandas&Plotly/src/notebook/section_4_1.ipynb)

