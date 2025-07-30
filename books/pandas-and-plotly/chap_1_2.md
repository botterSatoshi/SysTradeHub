---
title: データの種類とpandasのデータ型
free: true
---
## categoryデータ型 なるもの

なんか enum みたいなやつ

```python
df['category_animal'] = df['category_animal'].cat.set_categories(
    ['cat', 'dog'],
    ordered=False)

df['category_animal'].values
```
>['cat', 'dog', 'dog', 'cat', 'cat'] 
>Categories (2, object): ['cat', 'dog']

#
---
## sample code 
> [section_1_2.ipynb](books/Pandas&Plotly/src/notebook/section_1_2.ipynb)

