---
title: イントロ
free: true
---
## Pandas&Plotlyの本を実践してみた記録です。

この本
[pandas&Plotly 2D/3Dデータビジュアライゼーション実装ハンドブック](https://www.amazon.co.jp/pandas-plotly-2D-3D-%E3%83%87%E3%83%BC%E3%82%BF%E3%83%93%E3%82%B8%E3%83%A5%E3%82%A2%E3%83%A9%E3%82%A4%E3%82%BC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%AE%9F%E8%A3%85%E3%83%8F%E3%83%B3%E3%83%89%E3%83%96%E3%83%83%E3%82%AF/dp/479806890X)

### 1. 本書で紹介するpandas の機能

| 表形式データの操作         | DataFrame(略称df)のメソッド/属性            | pandas(略称pd)での関数      | 本書での記載                                                                     |
| ----------------- | ---------------------------------- | --------------------- | -------------------------------------------------------------------------- |
| データ型の取得           | df.dtypes                          |                       | [1.2 データの種類とpandasのデータ型](books/Pandas&Plotly/chap_1_2_データの種類とpandasのデータ型.md)              |
| データ型の変更           | df.astype<br>df.cat.set_categories | pd.to_datetime        | [1.2 データの種類とpandasのデータ型](books/Pandas&Plotly/chap_1_2_データの種類とpandasのデータ型.md)              |
| 行数と列数の取得          | df.shape                           |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 全要素数の取得           | df.size                            |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 行名や列名の取得          | df.axes<br>df.index<br>df.columns  |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 概要の取得             | df.info                            |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 先頭行の取得            | df.head                            |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 末尾行の取得            | df.tail                            |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 要約統計量の算出          | df.describe                        |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| 集約                | df.agg                             |                       | [1.3 DataFrameの情報の確認](books/Pandas&Plotly/chap_1_3_DataFrameの情報の確認.md)                 |
| Numpy ndarrayへの変換 | df.to_numpy                        |                       | [1.4 PythonのデータオブジェクトとDataFrameの相互変換](books/Pandas&Plotly/chap_1_4_PythonのデータオブジェクトとDataFrameの相互変換.md) |
| dictへの変換          | df.to_dict                         |                       | [1.4 PythonのデータオブジェクトとDataFrameの相互変換](books/Pandas&Plotly/chap_1_4_PythonのデータオブジェクトとDataFrameの相互変換.md) |
| csvファイルのインポート     |                                    | pd.read_csv           | [1.5 DataFrameのインポートとエクスポート](books/Pandas&Plotly/chap_1_5_DataFrameのインポートとエクスポート.md)          |
| csvファイルのエクスポート    | df.to_csv                          |                       | [1.5 DataFrameのインポートとエクスポート](books/Pandas&Plotly/chap_1_5_DataFrameのインポートとエクスポート.md)          |
| tsvファイルのインポート     |                                    | pd.read_table         | [1.5 DataFrameのインポートとエクスポート](books/Pandas&Plotly/chap_1_5_DataFrameのインポートとエクスポート.md)          |
| Excelファイルのインポート   |                                    | pd.read_excel         | [1.5 DataFrameのインポートとエクスポート](books/Pandas&Plotly/chap_1_5_DataFrameのインポートとエクスポート.md)          |
| Excelファイルのエクスポート  | df.to_excel                        | pd.ExcelWriter        | [1.5 DataFrameのインポートとエクスポート](books/Pandas&Plotly/chap_1_5_DataFrameのインポートとエクスポート.md)          |
| 要素の取得             | df.at<br>df.iat                    |                       | [2.1 DataFrameの部分選択](books/Pandas&Plotly/chap_2_1_DataFrameの部分選択.md)                  |
| 複数要素の取得           | df.loc<br>df.iloc<br>df.filter     |                       | [2.1 DataFrameの部分選択](books/Pandas&Plotly/chap_2_1_DataFrameの部分選択.md)                  |
| ブーリアンインデクシング      | df.loc<br>df.iloc                  |                       | [2.1 DataFrameの部分選択](books/Pandas&Plotly/chap_2_1_DataFrameの部分選択.md)                  |
| 二値マスクの作成          | df.isin                            |                       | [2.1 DataFrameの部分選択](books/Pandas&Plotly/chap_2_1_DataFrameの部分選択.md)                  |
| 条件に応じた行の抽出        | df.quary                           |                       | [2.1 DataFrameの部分選択](books/Pandas&Plotly/chap_2_1_DataFrameの部分選択.md)                  |
| カテゴリ別の分割          | df.groupby                         |                       | [2.2 DataFrameの分割](books/Pandas&Plotly/chap_2_2_DataFrameの分割.md)                    |
| 行番号の振り直し          | df.reset_index                     |                       | [2.2 DataFrameの分割](books/Pandas&Plotly/chap_2_2_DataFrameの分割.md)                    |
| 行方向の結合            |                                    | pd.concat             | [2.3 DataFrame同士の結合](books/Pandas&Plotly/chap_2_3_DataFrame同士の結合.md)                  |
| 列方向の結合            | df.join<br>df.merge                | pd.concat<br>pd.merge | [2.3 DataFrame同士の結合](books/Pandas&Plotly/chap_2_3_DataFrame同士の結合.md)                  |
| 列の追加              | df.assign                          |                       | [2.4 行や列の追加と削除](books/Pandas&Plotly/chap_2_4_行や列の追加と削除.md)                       |
| 列の挿入              | df.insert                          |                       | [2.4 行や列の追加と削除](books/Pandas&Plotly/chap_2_4_行や列の追加と削除.md)                       |
| 行や列の削除            | df.drop                            |                       | [2.4 行や列の追加と削除](books/Pandas&Plotly/chap_2_4_行や列の追加と削除.md)                       |
| 二値マスクに応じた代入       | df.mask<br>df.where                |                       | [3.1 値の演算](books/Pandas&Plotly/chap_3_1_値の演算.md)                            |
| 行方向のシフト           | df.shift                           |                       | [3.1 値の演算](books/Pandas&Plotly/chap_3_1_値の演算.md)                            |
| 累積和の算出            | df.cumsum                          |                       | [3.1 値の演算](books/Pandas&Plotly/chap_3_1_値の演算.md)                            |
| 移動平均の算出           | df.rolling                         |                       | [3.1 値の演算](books/Pandas&Plotly/chap_3_1_値の演算.md)                            |
| 関数適用              | df.applymap<br>df.apply            |                       | [3.2 自作関数を適用した操作](books/Pandas&Plotly/chap_3_2_自作関数を適用した操作.md)                     |
| 行方向のループ           | df.iterrows<br>df.itertuples       |                       | [3.3 ループ処理への対応](books/Pandas&Plotly/chap_3_3_ループ処理への対応.md)                       |
| 列方向のループ           | df.items                           |                       | [3.3 ループ処理への対応](books/Pandas&Plotly/chap_3_3_ループ処理への対応.md)                       |
| 欠損箇所の二値マスクの取得     | df.isna<br>df.isnull               |                       | [4.1 欠損値の表現とその確認方法](books/Pandas&Plotly/chap_4_1_欠損値の表現とその確認方法.md)                   |
| 値の置換              | df.replace                         |                       | [4.1 欠損値の表現とその確認方法](books/Pandas&Plotly/chap_4_1_欠損値の表現とその確認方法.md)                   |
| 欠損値の除外            | df.dropna                          |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 欠損値の穴埋め           | df.fillna                          |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 平均値の算出            | df.mean                            |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 中央値の算出            | df.median                          |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 最小値の算出            | df.min                             |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 最大値の算出            | df.max                             |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 欠損値の補間            | df.interpolate                     |                       | [4.2 欠損値の除外・穴埋め・補間](books/Pandas&Plotly/chap_4_2_欠損値の除外・穴埋め・補間.md)                   |
| 重複行の二値マスクの取得      | df.duplicated                      |                       | [4.3 重複行の削除](books/Pandas&Plotly/chap_4_3_重複行の削除.md)                          |
| 重複行の削除            | df.drop_duplicate                  |                       | [4.3 重複行の削除](books/Pandas&Plotly/chap_4_3_重複行の削除.md)                          |
|                   |                                    |                       |                                                                            |

### 2. 本書で紹介するPlotly のグラフ

| グラフの名前               | GraphObjects(略称go)でのクラス | Plotly Express(略称px)での関数                | DataFrame(略称df)からの呼び出し       | 本書でのグラフの分類と本書での記載             | グラフの分類 |
| -------------------- | ----------------------- | --------------------------------------- | ---------------------------- | ----------------------------- | ------ |
| 棒グラフ                 | go.Bar                  | px.bar                                  | df.plot.bar<br>df.plot.barth | 変数内の値を比較するグラフ                 | 比較     |
| ヒートマップ<br>(タイルマップ)   | go.Heatmap              | px.imshow                               |                              | 変数内の値を比較するグラフ                 | 比較     |
| レーダーチャート             | go.Scatterpolar         | px.line_polar                           |                              | 変数内の値を比較するグラフ                 | 比較     |
| ポーラーチャート（鶏卵図）        | go.Barpolar             | px.bar_polar                            |                              | 比較                            | 比較     |
| 散布図                  | go.Scatter              | px.scatter                              | df.plot.scatter              | 変数間の関係を表現するグラフ                | 相関     |
| バブルチャート              | go.Scatter              | px.scatter                              |                              | 変数間の関係を表現するグラフ                | 相関     |
| 散布図行列                | go.Splom                | px.scatter_matrix                       |                              | 変数間の関係を表現するグラフ                | 相関     |
| 平行座標プロット             | go.Parcoords            | px.parallel_coordinates                 |                              | 変数間の関係を表現するグラフ                | 相関     |
| 平行カテゴリープロット          | go.Parcats              | px.parallel_categories                  |                              | 変数間の関係を表現するグラフ                | 相関     |
| 箱ひげ図                 | go.Box                  | px.box                                  | df.plot.box                  | 変数の分布を表現するグラフ                 | 分布     |
| ストリップチャート（バイオリンプロット） | go.Box                  | px.strip                                |                              | 変数の分布を表現するグラフ                 | 分布     |
| バイオリン図               | go.Violin               | px.violin                               |                              | 変数の分布を表現するグラフ                 | 分布     |
| ヒストグラム               | go.Histogram            | px.histogram                            | df.plot.hist                 | 変数の分布を表現するグラフ                 | 分布     |
| 二次元ヒストグラム            | go.Histogram2d          | px.density_heatmap                      |                              | 変数の分布を表現するグラフ                 | 分布     |
| 密度等高線図               | go.Histogram2dContour   | px.density_contour                      |                              | 変数の分布を表現するグラフ                 | 分布     |
| 折れ線グラフ               | go.Scatter              | px.line                                 | df.plot.line                 | 変数の傾向や構成を表現するグラフ / 時間を表現するグラフ | 傾向     |
| ウォーターフォールチャート        | go.Waterfall            |                                         |                              | 変数の傾向や構成を表現するグラフ              | 比較     |
| 円グラフ                 | go.Pie                  | px.pie                                  | df.plot.pie                  | 変数の傾向や構成を表現するグラフ              | 部分全体   |
| ドーナツグラフ              | go.Pie                  | px.pie                                  |                              | 変数の傾向や構成を表現するグラフ              | 部分全体   |
| 等高線図                 | go.Contour              |                                         |                              | 空間を表現するグラフ                    | —      |
| ベクトルプロット             | —                       | — (Figure Factory の create_quiver関数を利用) |                              | 空間を表現するグラフ                    | —      |
| ドットマップ（点描図）          | go.Scattermapbox        | px.scatter_mapbox                       |                              | 空間を表現するグラフ                    | オーバーレイ |
| 比例シンボルマップ            | go.Scattermapbox        | px.scatter_mapbox                       |                              | 空間を表現するグラフ                    | オーバーレイ |
| イサリズミックマップ           | go.Densitymapbox        | px.density_mapbox                       |                              | 空間を表現するグラフ                    | オーバーレイ |
| コロプレスマップ（階級区分図）      | go.Choropleth           | px.choropleth_mapbox                    |                              | 空間を表現するグラフ                    | —      |
| 三次元散布図               | go.Scatter3d            | px.scatter_3d                           |                              | 空間を表現するグラフ                    | —      |
| 三次元バブルチャート           | go.Scatter3d            | px.scatter_3d                           |                              | 空間を表現するグラフ                    | —      |
| コーンプロット              | go.Cone                 |                                         |                              | 空間を表現するグラフ                    | —      |
| 等値面図                 | go.Isosurface           |                                         |                              | 空間を表現するグラフ                    | —      |
| ボリュームプロット            | go.Volume               |                                         |                              | 空間を表現するグラフ                    | —      |
| サーフェスプロット            | go.Surface              |                                         |                              | 空間を表現するグラフ                    | —      |
| メッシュプロット             | go.Mesh3d               |                                         |                              | 空間を表現するグラフ                    | —      |
| リッジラインプロット           | — (go.Violin で代用)       | — (px.violin で代用)                       |                              | 時間を表現するグラフ                    | 分布     |
| ローソク足チャート            | go.Candlestick          |                                         |                              | 時間を表現するグラフ                    | —      |
| 連結散布図（トレリスチャート）      | go.Scatter で代用          | — (px.scatter で代用)                      |                              | 時間を表現するグラフ                    | 傾向     |
