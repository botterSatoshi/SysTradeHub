---
title: PythonのデータオブジェクトとDataFrameの相互変換
free: true
---
## 基本

```python
data = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11]
]

df = pd.DataFrame(
    data,
    columns=['A', 'B', 'C', 'D'],
    index=['a', 'b', 'c']
)
```

| |A|B|C|D|
|---|---|---|---|---|
|a|0|1|2|3|
|b|4|5|6|7|
|c|8|9|10|11|

## dict型からも df に変換できるよ

```python
df = pd.DataFrame(
    {
        'A': {'a': 0, 'b': 4, 'c': 8},
        'B': {'a': 1, 'b': 5, 'c': 9},
        'C': {'a': 2, 'b': 6, 'c': 10},
        'D': {'a': 3, 'b': 7, 'c': 11}
    }
)
```

逆に dict型として吐き出せる
```python
df.to_dict()
```

>{'A': {'a': 0, 'b': 4, 'c': 8}, 'B': {'a': 1, 'b': 5, 'c': 9}, 'C': {'a': 2, 'b': 6, 'c': 10}, 'D': {'a': 3, 'b': 7, 'c': 11}}

### value部分をlistにしたい時

to_dictメソッドの引数 `orient='list'` にすると、valueがlistになったdictを出力することができる

```python
df.to_dict(orient='list')
```

>{'A': [0, 4, 8], 'B': [1, 5, 9], 'C': [2, 6, 10], 'D': [3, 7, 11]}

### value部分をpandasi.Seriesにしたい時

to_dictメソッドの引数 `orient='series'` にすると、valueがpandasi.Seriesになったdictを出力することができる

```python
df.to_dict(orient='series')
```

> {
'A': a    0
 b    4
 c    8
 Name: A, dtype: int64,
 'B': a    1
 b    5
 c    9
 Name: B, dtype: int64,
 'C': a     2
 b     6
 c    10
 Name: C, dtype: int64,
 'D': a     3
 b     7
 c    11
 Name: D, dtype: int64
 }


### 行名, 列名, valueをそれぞれlistにしたい時

to_dictメソッドの引数 `orient='split'` にすると、行名, 列名, valueをそれぞれlistになったdictを出力することができる

```python
df.to_dict(orient='split')
```

>{'index': ['a', 'b', 'c'],
 'columns': ['A', 'B', 'C', 'D'],
 'data': [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]}

### 行ごとにdictになったlistの出力

to_dictメソッドの引数 `orient='records'` にすると、行ごとにdictになったlistを出力することができる

```python
df.to_dict(orient='records')
```

>[{'A': 0, 'B': 1, 'C': 2, 'D': 3},
 {'A': 4, 'B': 5, 'C': 6, 'D': 7},
 {'A': 8, 'B': 9, 'C': 10, 'D': 11}]
 
---
## sample code
> [section_1_4.ipynb](books/Pandas&Plotly/src/notebook/section_1_4.ipynb)

