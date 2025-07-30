---
title: ループ処理への対応
free: true
---
まず強調しておきたい点は、可能な限りDataFrameのループ処理は避けた方が早いということ
しかし、複雑な処理を行おうとするとどうしてもループ処理を行わなければならない場合がある

サンプルデータ

| |carat|cut|color|clarity|depth|table|price|x|y|z|
|---|---|---|---|---|---|---|---|---|---|---|
|0|0.23|Ideal|E|SI2|61.5|55.0|326|3.95|3.98|2.43|
|1|0.21|Premium|E|SI1|59.8|61.0|326|3.89|3.84|2.31|
|2|0.23|Good|E|VS1|56.9|65.0|327|4.05|4.07|2.31|
|3|0.29|Premium|I|VS2|62.4|58.0|334|4.20|4.23|2.63|
|4|0.31|Good|J|SI2|63.3|58.0|335|4.34|4.35|2.75|
|...|...|...|...|...|...|...|...|...|...|...|
|53935|0.72|Ideal|D|SI1|60.8|57.0|2757|5.75|5.76|3.50|
|53936|0.72|Good|D|SI1|63.1|55.0|2757|5.69|5.75|3.61|
|53937|0.70|Very Good|D|SI1|62.8|60.0|2757|5.66|5.68|3.56|
|53938|0.86|Premium|H|SI2|61.0|58.0|2757|6.15|6.12|3.74|
|53939|0.75|Ideal|D|SI2|62.2|55.0|2757|5.83|5.87|3.64|

53940 rows × 10 columns


## iterrowsメソッドを使う方法
iterrowsメソッドを使うことで、各行の行名とSeriesを取り出すことが可能です。
得られたSeriesは角括弧でSeriesのインデックス名を指定して部分選択することができます。
インデックス名をlistで指定し、複数選択することも可能です。

```python
for index, record in df.iterrows():
    print(f'index {index}:  price {record["price"]}')
    print(record[['carat', 'cut', 'color', 'clarity']], '\n')
    if index > 2:
        break
```
>index 0:  price 326
>carat       0.23
>cut        Ideal
>color          E
>clarity      SI2
>Name: 0, dtype: object 
>
>index 1:  price 326
>carat         0.21
>cut        Premium
>color            E
>clarity        SI1
>Name: 1, dtype: object 
>
>index 2:  price 327
>carat      0.23
>cut        Good
>color         E
>clarity     VS1
>Name: 2, dtype: object 
>
>index 3:  price 334
>carat         0.29
>cut        Premium
>color            I
>clarity        VS2
>Name: 3, dtype: object 

## itertuplesメソッドを使う方法
itertuplesメソッドの場合は、レコードはnamedtuples形式で取り出されます。
行名は index属性として格納されます。
```python
for record in df.itertuples():
    print(f'index {record.Index}:  price {record.price}')
    print(record.carat, record.cut, record.color, record.clarity, '\n')
    if record.Index > 2:
        break
```
>index 0:  price 326
>0.23 Ideal E SI2 
>
>index 1:  price 326
>0.21 Premium E SI1 
>
>index 2:  price 327
>0.23 Good E VS1 
>
>index 3:  price 334
>0.29 Premium I VS2 

## 列方向のループ itemsメソッド
列方向のループには **items**メソッドを使います。
転地して .T.iterrows() でも同じ結果
```python
for label, content in df[['price', 'carat', 'cut', 'color', 'clarity']].items():
    print(f'label: {label}')
    print(f'{content[0]}  {content[1]}  {content[2]}  {content[3]} ...\n')

# df[['price', 'carat', 'cut', 'color', 'clarity']].T.iterrows() でも同じ結果
```
>label: price
>326  326  327  334 ...
>
>label: carat
>0.23  0.21  0.23  0.29 ...
>
>label: cut
>Ideal  Premium  Good  Premium ...
>
>label: color
>E  E  E  I ...
>
>label: clarity
>SI2  SI1  VS1  VS2 ...





#
---
## sample code
> [section_3_3.ipynb](books/Pandas&Plotly/src/notebook/section_3_3.ipynb)

