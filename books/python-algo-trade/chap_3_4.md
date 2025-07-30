---
title: chap_3_4
free: true
---
## 3.4 HDF5

そもそもHDF5って？

- Hierarchical Data Formatの略（5はバージョン）で、名前の通り階層化された形でデータを保存することができるファイル形式です。
- ある種フォルダやファイルシステムに感覚が近く、1つのファイル内に整理しつつ様々な複数ファイルを保存できます。

## 3.4.2 TsTables の使用

https://pypi.org/project/tstables/

TsTables は、PyTables を使用して HDF5 ファイルに時系列データを保存する Python パッケージです。

### 例

この例では、ビットコインの価格データを分単位で読み込み、一定範囲のデータを取得します。ここでの完全な例とその他の例については、 [EXAMPLES.md を](https://pypi.org/project/tstables/EXAMPLES.md)参照してください。

```python
# Class to use as the table description
class BpiValues(tables.IsDescription):
    timestamp = tables.Int64Col(pos=0)
    bpi = tables.Float64Col(pos=1)

# Use pandas to read in the CSV data
bpi = pandas.read_csv('bpi_2014_01.csv',index_col=0,names=['date','bpi'],parse_dates=True)

f = tables.open_file('bpi.h5','a')

# Create a new time series
ts = f.create_ts('/','BPI',BpiValues)

# Append the BPI data
ts.append(bpi)

# Read in some data
read_start_dt = datetime(2014,1,4,12,00)
read_end_dt = datetime(2014,1,4,14,30)

rows = ts.read_range(read_start_dt,read_end_dt)

# `rows` will be a pandas DataFrame with a DatetimeIndex.
```

既存のbpi.h5 HDF5 ファイルを開いて、そこから時系列を取得する方法は次のとおりです。

```python
f = tables.open_file('bpi.h5','r')
ts = f.root.BPI._f_get_timeseries()

# Read in some data
read_start_dt = datetime(2014,1,4,12,00)
read_end_dt = datetime(2014,1,4,14,30)

rows = ts.read_range(read_start_dt,read_end_dt)
```


#
---
## sample code
>