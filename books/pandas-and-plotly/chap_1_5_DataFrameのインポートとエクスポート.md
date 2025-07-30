---
title: DataFrameのインポートとエクスポート
free: true
---
## インポートテクニック

インポートする際、データ型を指定することでメモリを節約することができます。


```python
df = pd.read_csv(
    'sample_1_5.csv',
    parse_dates=[13]
)
```

時刻データの列は、引数`parse_dates`で列番号を指定できます。
時刻データが複数ある場合でもlistで複数指定します。


### 行インデックス付きのcsvをインポートする場合

行インデックス付きで記録されているCSVファイルをインポートする際には、read_csv 関数の引数 index_col に**行インデックスが記録された列**の列番号を指定します。

```python
df_index_col = pd.read_csv('dump_1_5a.csv', index_col=0)
```



---
## sample code
> [section_1_5.ipynb](books/Pandas&Plotly/src/notebook/section_1_5.ipynb)

