---
title: DataFrame同士の結合
free: true
---
データが複数の表形式データに分かれていた場合、可視化を行う前に結合する必要があります。

行方向の結合と列方向の結合があります。pandasでは、行方向の結合では列インデックスがキーとなります。列方向の結合では行インデックスがキーとなる場合と、指定した列の値がキーとなる場合があります。

|        |            |                |
| ------ | ---------- | -------------- |
| 行方向の結合 | 列インデックスがキー | concat         |
| 列方向の結合 | 行インデックスがキー | concat<br>join |
|        | 列の値がキー     | join<br>merge  |
キーとは、結合するデータ同士の仲介となる識別情報です。結合先と結合元でキーが一致する箇所が結合されます。

![](images/Pasted%20image%2020240922160029.png)

## 行方向の結合の種類
外部結合で値が存在しない部分には**NaN**が記入されます。

![](images/Pasted%20image%2020240922160915.png)

## 列方向の結合の種類


![](images/Pasted%20image%2020240922161806.png)


## pandas の結合機能

|                  | 行方向<br>内部結合<br>外部結合 | 列方向<br>内部結合<br>外部結合 | 列方向<br>結合先-外部結合<br>結合元-外部結合 | キー                         |
| ---------------- | :-----------------: | :-----------------: | :-------------------------: | -------------------------- |
| pd.**concat**    |          〇          |          〇          |              ×              | 行方向：列インデックス<br>列方向：行インデックス |
| df.**join**      |          ×          |          〇          |              〇              |                            |
| pandas.**merge** |          ×          |          〇          |              〇              |                            |

## 行方向の結合
サンプルデータ

|     | Name    | Value |
| --- | ------- | ----- |
| a   | Alpha   | 100   |
| b   | Bravo   | 200   |
| c   | Charlie | 300   |
=df1

|     | Name    | Value |
| --- | ------- | ----- |
| d   | Delta   | 400   |
| e   | Echo    | 500   |
| f   | Foxtrot | 600   |
=df2

|     | Name    | ID  |
| --- | ------- | --- |
| 0   | Delta   | 111 |
| 1   | Echo    | 222 |
| 2   | Foxtrot | 333 |
=df3

### 結合
行方向の結合を行うには pandas.concat関数を使用して、結合方向として引数axis=0を指定します。
```python
df = pd.concat([df1, df2], axis=0)

df
```

|     | Name    | Value |
| --- | ------- | ----- |
| a   | Alpha   | 100   |
| b   | Bravo   | 200   |
| c   | Charlie | 300   |
| d   | Delta   | 400   |
| e   | Echo    | 500   |
| f   | Foxtrot | 600   |

### 外部結合
pandas.conatでは引数joinで結合方法を外部結合か内部結合を指定できます。
引数を省略するとjoin='order'として外部結合が指定されます。
```python
df = pd.concat([df1, df3], axis=0)

df
```

|     | Name    | Value | ID    |
| --- | ------- | ----- | ----- |
| a   | Alpha   | 100.0 | NaN   |
| b   | Bravo   | 200.0 | NaN   |
| c   | Charlie | 300.0 | NaN   |
| 0   | Delta   | NaN   | 111.0 |
| 1   | Echo    | NaN   | 222.0 |
| 2   | Foxtrot | NaN   | 333.0 |

### 内部結合
内部結合を行うには引数join='inner'に指定します。サンプルコードでは、df1とdf3で共通した列「Name」だけのデータが作成されました。
```python
df = pd.concat([df1, df3], axis=0, join='inner')

df
```

| |Name|
|---|---|
|a|Alpha|
|b|Bravo|
|c|Charlie|
|0|Delta|
|1|Echo|
|2|Foxtrot|

## 列方向の結合
サンプルデータ

|     | Name    | Value |
| --- | ------- | ----- |
| a   | Alpha   | 100   |
| b   | Bravo   | 200   |
| c   | Charlie | 300   |
=df1

|     | ID  |
| --- | --- |
| a   | 11  |
| b   | 22  |
| d   | 44  |
=df4

|         | Value5 |
| ------- | ------ |
| Charlie | 1000   |
| Delta   | 2000   |
| Echo    | 3000   |
=df5


### concatによる列の結合
concatの引数 axis=1 を指定することで列結合を行うことができます。
行結合と同じく joinで内部結合innner'か、外部結合'outer'かを指定できます。


```python
df = pd.concat([df1, df4], axis=1)

df
```

| |Name|Value|ID|
|---|---|---|---|
|a|Alpha|100.0|11.0|
|b|Bravo|200.0|22.0|
|c|Charlie|300.0|NaN|
|d|NaN|NaN|44.0|

### joinによる列の結合

#### 内部結合
内部結合を how='inner'として指定しています。外部結合はhow='outer'です

```python
df = df1.join(df4, how='inner')

df
```

| |Name|Value|ID|
|---|---|---|---|
|a|Alpha|100|11|
|b|Bravo|200|22|

#### 結合先-外部結合
結合先-外部結合を行うには 引数how='left'で指定します。引数を省略した場合はhow='left'

```python
df = df1.join(df4, how='left')

df
```

|     | Name    | Value | ID   |
| --- | ------- | ----- | ---- |
| a   | Alpha   | 100   | 11.0 |
| b   | Bravo   | 200   | 22.0 |
| c   | Charlie | 300   | NaN  |


#### 結合元-外部結合
how='right'

```python
df = df1.join(df4, how='right')

df
```

| |Name|Value|ID|
|---|---|---|---|
|a|Alpha|100.0|11|
|b|Bravo|200.0|22|
|d|NaN|NaN|4|

#### 結合先の列と結合元のインデックスが一致する行を外部結合
joinメソッドの引数onに結合先の列を指定
するとdf1の列「Name」で値が「Charlie」だった行に対してdf5でインデックスが「Charlie」だった行が結合されます。

```python
df = df1.join(df5, on='Name')

df
```

|     | Name    | Value | Value5 |
| --- | ------- | ----- | ------ |
| a   | Alpha   | 100   | NaN    |
| b   | Bravo   | 200   | NaN    |
| c   | Charlie | 300   | 1000.0 |


### mergeによる列の結合
サンプルデータ

|     | Name    | ID  | Value1 |
| --- | ------- | --- | ------ |
| a   | Alpha   | 11  | 100    |
| b   | Bravo   | 22  | 200    |
| c   | Charlie | 33  | 100    |
| d   | Delta   | 44  | 400    |
=df1

|     | Name    | Number | Value2 |
| --- | ------- | ------ | ------ |
| e   | Echo    | 11     | 200    |
| d   | Delta   | 22     | 100    |
| c   | Charlie | 33     | 400    |
| b   | Bravo   | 44     | 200    |
=df2

mergeの第１引数は結合先（左テーブル）、第2引数は結合元（右テーブル）です。
- 引数'how'で結合方法を指定します。
	- 省略すると how='innner' になります。
- 引数'on'にはキーとする列を指定します。

Name列をキーとして内部結合する場合には on='Name'を指定します。
内部結合の結果、Nameが共通している`Brabo`, `Charlie`, `Delta` の行が残りました。
**pandas**.merge でも **DataFrame**.mergeでも実現可能

```python
df = pd.merge(df1, df2, how='inner', on='Name')
# df = df1.merge(df2, how='inner', on='Name') でも実現可能

df
```

|     | Name    | ID  | Value1 | Number | Value2 |
| --- | ------- | --- | ------ | ------ | ------ |
| 0   | Bravo   | 22  | 200    | 44     | 200    |
| 1   | Charlie | 33  | 100    | 33     | 400    |
| 2   | Delta   | 44  | 400    | 22     | 100    |
インデックスが連番に変わっています。


#### 結合先-外部結合
引数 how='left' で結合先-外部結合になります。
結合先であるdf1が持っていた行はすべて残っていますが、df2の対応していない`Alpha`の行はNumberとValue2がNaNになっています。
```python
df = pd.merge(df1, df2, how='left', on='Name')

df
```

|     | Name    | ID  | Value1 | Number | Value2 |
| --- | ------- | --- | ------ | ------ | ------ |
| 0   | Alpha   | 11  | 100    | NaN    | NaN    |
| 1   | Bravo   | 22  | 200    | 44.0   | 200.0  |
| 2   | Charlie | 33  | 100    | 33.0   | 400.0  |
| 3   | Delta   | 44  | 400    | 22.0   | 100.0  |
#### 結合元-外部結合
引数 how='right' で結合元-外部結合になります。
結合元であるdf2が持っていた行はすべて残っていますが、df1の対応していない`Echo`の行はIDとValue1がNaNになっています。
```python
df = pd.merge(df1, df2, how='right', on='Name')

df
```

|     | Name    | ID   | Value1 | Number | Value2 |
| --- | ------- | ---- | ------ | ------ | ------ |
| 0   | Echo    | NaN  | NaN    | 11     | 200    |
| 1   | Delta   | 44.0 | 400.0  | 22     | 100    |
| 2   | Charlie | 33.0 | 100.0  | 33     | 400    |
| 3   | Bravo   | 22.0 | 200.0  | 44     | 200    |

#### 外部結合
how='outer'で外部結合になります。
```python
df = pd.merge(df1, df2, how='outer', on='Name')

df
```

|Name|ID|Value1|Number|Value2|
|---|---|---|---|---|
|0|Alpha|11.0|100.0|NaN|NaN|
|1|Bravo|22.0|200.0|44.0|200.0|
|2|Charlie|33.0|100.0|33.0|400.0|
|3|Delta|44.0|400.0|22.0|100.0|
|4|Echo|NaN|NaN|11.0|200.0|


#### 結合先と結合元で異なる列名を指定
引数`left_on`と`right_on`を指定します。
結合先と結合元で共通する列名は、接続語として`_x`と`_y`が自動的に追加されます。


ここでは、結合先df1の列名を「Value1」、結合元df2の列名を「Value2」にして結合しています。
```python
df = pd.merge(df1, df2, left_on='Value1', right_on='Value2')

df
```

|     | Name_x  | ID  | Value1 | Name_y  | Number | Value2 |
| --- | ------- | --- | ------ | ------- | ------ | ------ |
| 0   | Alpha   | 11  | 100    | Delta   | 22     | 100    |
| 1   | Charlie | 33  | 100    | Delta   | 22     | 100    |
| 2   | Bravo   | 22  | 200    | Echo    | 11     | 200    |
| 3   | Bravo   | 22  | 200    | Bravo   | 44     | 200    |
| 4   | Delta   | 44  | 400    | Charlie | 33     | 400    |

df1とdf2で列名「Name」が共通していたため、自動的に「Name_x」「Name_y」に変化して結合されています。

接続語は引数`suffixes`で指定することもできます。
```python
df = pd.merge(df1, df2, left_on='Value1', right_on='Value2', suffixes=['-1', '-2'])

df
```

|     | Name-1  | ID  | Value1 | Name-2  | Number | Value2 |
| --- | ------- | --- | ------ | ------- | ------ | ------ |
| 0   | Alpha   | 11  | 100    | Delta   | 22     | 100    |
| 1   | Charlie | 33  | 100    | Delta   | 22     | 100    |
| 2   | Bravo   | 22  | 200    | Echo    | 11     | 200    |
| 3   | Bravo   | 22  | 200    | Bravo   | 44     | 200    |
| 4   | Delta   | 44  | 400    | Charlie | 33     | 400    |

listにした複数キーを指定することも
```python
df = pd.merge(df1, df2, left_on=['Name', 'ID'], right_on=['Name', 'Number'])

df
```

| <br> | Name    | ID  | Value1 | Number | Value2 |
| ---- | ------- | --- | ------ | ------ | ------ |
| 0    | Charlie | 33  | 100    | 33     | 400    |

NameがCharlie、IDが33の組み合わせの行だけが共通していたので結合されています。


#
---
## sample code
> [section_2_3.ipynb](books/Pandas&Plotly/src/notebook/section_2_3.ipynb)

