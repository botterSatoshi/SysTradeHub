---
title: "クロスバリデーション(KFold, TimeSeriesSplit)"
emoji: "🔖"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: []
published: true
---
# クロスバリデーション

Cross Validationはモデルの成績を測る方法の一つで

大まかに言うと、
様々な方法でデータを学習データとテストデータに分割し、
学習データで学習させたモデルを、
テストデータで評価するという方法です。

> なんてことないいつもやってるわ


## KFold
KFoldとは、訓練データセットを k 個のサブセットに分割して、そのうち k - 1 個のサブセットで学習し、残りの 1 個のサブセットで検証するという作業をすべての組み合わせに対して行う検証方法。

![](images/Pasted-image-20230602114541.png)


## TimeSeriesSplit

TimeSeriesSplit は 時系列データ向けであり、未来のデータを学習して過去のデータを予測すること(リーク)が発生しないように交差検証を実施する手法。

![](images/Pasted%20image-20230602115045.png)