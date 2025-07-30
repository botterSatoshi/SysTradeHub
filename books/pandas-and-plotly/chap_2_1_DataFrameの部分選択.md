---
title: DataFrameの部分選択
free: true
---
```python
import pandas as pd
import numpy as np

df = pd.DataFrame(
    data=np.arange(20).reshape(5, 4),
    index=['a', 'b', 'c', 'd', 'e'],
    columns=['Alpha', 'Bravo', 'Charlie', 'Delta']
)
```

|     | Alpha | Bravo | Charlie |
| --- | ----- | ----- | ------- |
| a   | 0     | 1     | 2       |
| b   | 4     | 5     | 6       |
| c   | 8     | 9     | 10      |
| d   | 12    | 13    | 14      |
| e   | 16    | 17    | 18      |
### DataFrameから1つだけの要素を選択するには at

```python
df.at['d', 'Bravo']
```
>13

### DataFrameから行番号と列番号を使って1つだけの要素を選択するには iat

```python
df.iat[3, 1]
```
>13

### 1行の要素を選択するには loc

```python
df.loc['d', :]  # df.loc['d'] と同じ
```
>Alpha      12
>Bravo      13
>Charlie    14
>Delta      15
>Name: d, dtype: int64

選択した1行は `Series`インスタンスであることに注意してください

#### locの行名をlistで指定
loc を使った1行の選択でも行名を list で指定すると、得られる結果はDataFrameのインスタンスになります。

```python
df.loc[['d'], :]    # df.loc[['d']] と同じ
```

|     | Alpha | Bravo | Charlie | Delta |
| --- | ----- | ----- | ------- | ----- |
| d   | 12    | 13    | 14      | 15    |

```python
df.loc[:, 'Bravo']  # df['Bravo'] と同じ
```
>a     1
>b     5
>c     9
>d    13
>e    17
Name: Bravo, dtype: int64

1行の選択の時と同じく列名を list で指定すると、得られる結果はDataFrameのインスタンスになります。
```python
df.loc[:, ['Bravo']]
```

| |Bravo|
|---|---|
|a|1|
|b|5|
|c|9|
|d|13|
|e|17|

### 複数行の要素や複数列を選択
listにして指定。結果は当然 DataFrame

```python
df.loc[['a', 'c', 'e'], :]  # df.loc[['a', 'c', 'e']] と同じ
```

|     | Alpha | Bravo | Charlie | Delta |
| --- | ----- | ----- | ------- | ----- |
| a   | 0     | 1     | 2       | 3     |
| c   | 8     | 9     | 10      | 11    |
| e   | 16    | 17    | 18      | 19    |
```python
df.loc[:, ['Bravo', 'Delta']]   # df[['Bravo', 'Delta']] と同じ
```
|     | Bravo | Delta |
| --- | ----- | ----- |
| a   | 1     | 3     |
| b   | 5     | 7     |
| c   | 9     | 11    |
| d   | 13    | 15    |
| e   | 17    | 19    |
```python
df.loc[['a', 'c', 'e'], ['Bravo', 'Delta']]
```
||Bravo|Delta|
|---|---|---|
|a|1|3|
|c|9|11|
|e|17|19|

### 行番号や列番号を指定して複数要素を選択
```python
df.iloc[[0, 2, 4], [1, 3]]
```

| |Bravo|Delta|
|---|---|---|
|a|1|3|
|c|9|11|
|e|17|19|

#### スライシングを使って選択することも可能

```python
# df.loc['b':'d', 'Bravo':'Delta'] でも実現できるがilocを使ったほうが分かりやすい

df.iloc[1:4, 1:4]
```

| |Bravo|Charlie|Delta|
|---|---|---|---|
|b|5|6|7|
|c|9|10|11|
|d|13|14|15|
#### 行番号や列番号が numpyでもOK
```python
row_indices = np.array([0, 2, 3])
col_indices = np.arange(1, 4)

df.iloc[row_indices, col_indices]
```

|     | Bravo | Charlie | Delta |
| --- | ----- | ------- | ----- |
| a   | 1     | 2       | 3     |
| c   | 9     | 10      | 11    |
| d   | 13    | 14      | 15    |

## もっと柔軟な方法

### DataFrameのfilterメソッドその１
完全一致指定
指定した行名、列名と完全に一致した要素を選択するもの

```python
df.filter(['Alpha', 'Charlie'])
```

| |Alpha|Charlie|
|---|---|---|
|a|0|2|
|b|4|6|
|c|8|10|
|d|12|14|
|e|16|18|
### DataFrameのfilterメソッドその2
部分一致
指定した文字列を含む行名、列名を選択
```python
df.filter(like='r')
```

| |Bravo|Charlie|
|---|---|---|
|a|1|2|
|b|5|6|
|c|9|10|
|d|13|14|
|e|17|18|
### DataFrameのfilterメソッドその3

filterでは行名と列名を同時に指定することはできません。
#### 正規表現を使って列名を選択

引数`regex`を指定します。列名の途中に`l`があり`a`で終わる列を選択しています。
```python
df.filter(regex='.*l.*a')
```

|     | Alpha | Delta |
| --- | ----- | ----- |
| a   | 0     | 3     |
| b   | 4     | 7     |
| c   | 8     | 11    |
| d   | 12    | 15    |
| e   | 16    | 19    |

#### 正規表現を使って行名を選択

filterメソッドの `axis`を`axis=0`（`axis=index'でも同じ）にすることで、条件に該当する行を選択することができます
```python
df.filter(['a', 'e'], axis=0)   # df.filter(['a', 'e'], axis='index') でも同じ
```

| |Alpha|Bravo|Charlie|Delta|
|---|---|---|---|---|
|a|0|1|2|3|
|e|16|17|18|19|

### boolean indexing（ブーリアンインデクシング）

選択する要素を**True**と**False**で選択する方法を**ブーリアンインデクシング**と言います。

事前にtrue,falseでマスクして選択する方法

行`a`, `d`, `e`を選択するマスクを作成し、DataFrameのlocに指定して対象の行を選択しています。
```python
row_mask = [True, False, False, True, True]

df.loc[row_mask]    # df.iloc[row_bool] や df[row_bool] と同じ
```

| |Alpha|Bravo|Charlie|Delta|
|---|---|---|---|---|
|a|0|1|2|3|
|d|12|13|14|15|
|e|16|17|18|19|

ilocや角括弧でも同じ結果を得ることができます。

#### 行と列を同時にマスクする
行のマスクと列のマスクを同時に指定することができます。

```python
col_mask = [False, True, False, True]

df.loc[row_mask, col_mask]  # df.iloc[row_mask, col_mask] と同じ
```

|     | Bravo | Delta |
| --- | ----- | ----- |
| a   | 1     | 3     |
| d   | 13    | 15    |
| e   | 17    | 19    |

#### マスクの作成テクニック
true,false マスクは、Seriesに比較演算を行って作成することができます

```python
# 列 Alphaで値が6より大きい行を選択するマスクを作成
row_mask = df.loc[:, 'Alpha'] > 6   # df['Alpha'] > 6 でも同じ

row_mask
```
>a    False
>b    False
>c     True
>d     True
>e     True
Name: Alpha, dtype: bool

```python
# 行 d で値が偶数の列を選択するマスク
col_mask = df.loc['d', :] % 2 == 0  # df.loc['d'] % 2 == 0 でも同じ

col_mask
```
>Alpha       True
>Bravo      False
>Charlie     True
>Delta      False
Name: d, dtype: bool

#### マスクに論理演算

論理否定は **~**（チルダ）
```python
df.loc[~row_mask, ~col_mask]
```


|     | Bravo | Delta |
| --- | ----- | ----- |
| a   | 1     | 3     |
| b   | 5     | 7     |

論理積は **&**（アンパサンド）,論理和は **|**（バーティカル）
```python
# c, e の行がTrueになる二値マスク
row_mask2 = df.loc[:, 'Alpha'].isin([8, 16])    # df['Alpha'].isin([8, 16]) でも同じ

# Delta の列がTrueになる二値マスク
col_mask2 = df.loc['b', :] == 7             # df.loc['b'] == 7 でも同じ

df.loc[row_mask & row_mask2, col_mask | col_mask2]
```

| |Alpha|Charlie|Delta|
|---|---|---|---|
|c|8|10|11|
|e|16|18|1|

--
```python
df.loc[df.loc[:, 'Alpha'] > 6]
df.loc[df.loc[:, 'Bravo'] == 9]
df.loc[df.loc[:, 'Charlie'] < 12]
```

#### isinから作成するマスク

boolean indexingのマスクは `isin`メソッドから作成することもできます。
df の `isin`メソッドは、指定されたlist中に値のある個所にはtrueを、それ以外の個所にはfalseのdfを作成するものです。

```python
df.isin([0, 5, 10, 15])
```

| |Alpha|Bravo|Charlie|Delta|
|---|---|---|---|---|
|a|True|False|False|False|
|b|False|True|False|False|
|c|False|False|True|False|
|d|False|False|False|True|
|e|False|False|False|False|
dfから選択した1行、あるいは1列のSeriesにisinメソッドを使用することで、マスクを作成できます。

```python
row_mask = df['Alpha'].isin([0, 8, 16])

df.loc[row_mask]
```
Alphaに 0, 8, 16 がある行を抽出

|     | Alpha | Bravo | Charlie | Delta |
| --- | ----- | ----- | ------- | ----- |
| a   | 0     | 1     | 2       | 3     |
| c   | 8     | 9     | 10      | 11    |
| e   | 16    | 17    | 18      | 19    |

#### 文字列を条件式にした選択

dfのqueryメソッドによって条件に応じた行の選択を行うことができます。

```python
df.query('Alpha > 6')
```


|     | Alpha | Bravo | Charlie | Delta |
| --- | ----- | ----- | ------- | ----- |
| c   | 8     | 9     | 10      | 11    |
| d   | 12    | 13    | 14      | 15    |
| e   | 16    | 17    | 18      | 19    |

```python
df.query('Alpha > 6')
df.query('Bravo == 9')
df.query('Charlie < 12')
```


# 
---
## sample code
> [section_2_1.ipynb](books/Pandas&Plotly/src/notebook/section_2_1.ipynb)

