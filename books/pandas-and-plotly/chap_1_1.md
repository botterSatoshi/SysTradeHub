---
title: 表形式データの構成要素
free: true
---

![](images/Pasted%20image%2020240916153639.png)

![](images/Pasted%20image%2020240916163401.png)

```python
df = pd.DataFrame(
    {
        'A': ('Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo'),
        'B': [1, 10, 100, 1000, 10000],
        'C': np.linspace(0, 2, 5),
    },
    index=('a', 'b', 'c', 'd', 'e')
)
```

|     | A       | B     | C   |
| --- | ------- | ----- | --- |
| a   | Alfa    | 1     | 0.0 |
| b   | Bravo   | 10    | 0.5 |
| c   | Charlie | 100   | 1.0 |
| d   | Delta   | 1000  | 1.5 |
| e   | Echo    | 10000 | 2.0 |

## 列を指定
列を指定するには dictと同じ
```python
df['B`]
```
>a        1
>b       10
>c      100
>d     1000
>e    10000
>Name: B, dtype: int64

## locで行名を指定

```python
df.loc['c']
```
>A    Charlie
>B        100
>C        1.0
>Name: c, dtype: object

## 列名の一覧は culumns
```python
df.columns
```
>Index(['A', 'B', 'C'], dtype='object')

## 行名の一覧は index
```python
df.index
```
>Index(['a', 'b', 'c', 'd', 'e'], dtype='object')

## データは values
```python
df.values
```
>array([['Alfa', 1, 0.0],
>       ['Bravo', 10, 0.5],
>       ['Charlie', 100, 1.0],
>       ['Delta', 1000, 1.5],
>       ['Echo', 10000, 2.0]], dtype=object)




#
---
## sample code 
> [section_1_1.ipynb](books/Pandas&Plotly/src/notebook/section_1_1.ipynb)

