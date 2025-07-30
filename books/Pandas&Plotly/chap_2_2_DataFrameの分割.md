---
title: DataFrameの分割
free: true
---
サンプルデータ
```python
df.shape
```
>(200000, 16)

## 指定した位置での分割

- 前半150000行  
```python
df1 = df.iloc[:150000]

df1.shape
```
>(150000, 16)

- 後半150000行
```python
df2 = df.iloc[150000:]

df2.shape
```
>(50000, 16)

- 前半12列
```python
df3 = df.iloc[:, :12]

df3.shape
```
>(200000, 12)

- 後半4列
```python
df4 = df.iloc[:, 12:]

df4.shape
```
>(200000, 4)



## カテゴリ別に分割
下表のようなカテゴリがあるデータを読み込んだとする

| col_unordered |
| ------------- |
| Rabbit        |
| Dog           |
| Rabbit        |
| Hamster       |
| Mouse         |
| Cat           |
| Dog           |
| Ferret        |
dfにカテゴリの設定をします
```python
unordered_categories = [
    'Mouse',
    'Cat',
    'Dog',
    'Hamster',
    'Rabbit',
    'Ferret']
df['col_unordered'] = df['col_unordered'].cat.set_categories(
    unordered_categories,
    ordered=False)
```

カテゴリ分けした行数は、df.groupbyの sizeメソッドで確認できます。
```python
gb = df.groupby('col_unordered')

gb.size()
```
>col_unordered
>**Mouse**      33383
>**Cat**        33273
>**Dog**        33384
>**Hamster**    33287
>**Rabbit**     33602
>**Ferret**     33071
dtype: int64

### 特定のカテゴリに該当する行を得る

```python
df_mouse = gb.get_group('Mouse')
# df.loc[df.loc[:, 'col_unordered'] == 'Mouse'] や
# df.query('col_unordered == "Mouse"') でも同じ

df_mouse.head()
```

|     | col_int8 | ... | col_datetime        | col_ordered | col_unordered |
| --- | -------- | :-: | ------------------- | ----------- | ------------- |
| 4   | 12       | ... | 1700-01-05 16:37:16 | EXTRA-SMALL | Mouse         |
| 17  | -118     | ... | 1700-01-18 13:00:45 | MIDDLE      | Mouse         |
| 23  | 18       | ... | 1700-01-24 08:47:02 | EXTRA-LARGE | Mouse         |
| 27  | -44      | ... | 1700-01-28 20:33:08 | LARGE       | Mouse         |
| 41  | -51      | ... | 1700-02-11 21:55:07 | MIDDLE      | Mouse         |

### Groupebyは反復可能(iterable)でありforループが使える

```python
gb = df.groupby('col_unordered')
for group, df_group in gb:
    print(group, df_group.shape)
```
>Mouse (33383, 16)
>Cat (33273, 16)
>Dog (33384, 16)
>Hamster (33287, 16)
>Rabbit (33602, 16)
>Ferret (33071, 16)

## ランダム分割

sckit-learnの機能を使って全体の80%(160000行)を学習データに、残りの20%(40000行)をテストデータにランダムに分割する

```python
from sklearn.model_selection import train_test_split

df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
# train_test_split(df, test_size=40000) と同じ

df_train.shape, df_test.shape
```
>((160000, 16), (40000, 16))


行番号を学習データ、テストデータそれぞれ連番に振りなおしたい場合は`reset_index`を使う。
引数`drop`を省略（=False）にすると、元の行番号が新たな列となって残ってしまうので注意

```python
df_train = df_train.reset_index(drop=True)

df_train.head()
```

|     | col_int8 | ... | col_datetime        | col_ordered | col_unordered |
| --- | -------- | :-: | ------------------- | ----------- | ------------- |
| 0   | -72      | ... | 2049-01-09 18:47:58 | MIDDLE      | Cat           |
| 1   | 94       | ... | 2125-11-21 10:48:47 | MIDDLE      | Mouse         |
| 2   | 10       | ... | 1906-08-25 14:16:24 | EXTRA-SMALL | Hamster       |
| 3   | 29       | ... | 2209-07-26 05:46:58 | SMALL       | Rabbit        |
| 4   | -65      | ... | 1956-08-04 01:10:50 | EXTRA-SMALL | Ferret        |



---
## sample code
> [section_2_2.ipynb](books/Pandas&Plotly/src/notebook/section_2_2.ipynb)

