
# coding: utf-8

# # Python時系列データ分析入門（解説用）

# ## データの読み込み
# * read_csv: CSVファイルをDataFrameオブジェクトとして読み込む
# * CSV: Comma-Separated Values
# * DataFrame: 二次元行列データの格納、加工に適している  
# CSV -> DataFrame -> numpy
# * head: 最初の5行を表示
# * tail: 最後の5行を表示

# In[1]:


import pandas as pd

df = pd.read_csv("pv_ver00.csv") 
df.head()


# * info: Dataframeの**データ数**、データの型などの情報を表示

# In[47]:


df.info()


# * index_col: 行番号以外をインデックスとして指定
# * parse_dates: True ⇒ 日付を分割する  
# e.g. '1988/06/11' (False) -> '1988-06-11' (True): '1988-06'など月単位で指定できるようになる
# * dropna: nanなどの欠損値をdrop(除去)
# * nan: Not A Number

# In[3]:


df = pd.read_csv('pv_ver00.csv', index_col='date',
                 parse_dates=True, dtype=float)
df = df.dropna()
df.info()


# * loc: LOCation  
# 列（や行）を文字列によって範囲を指定し抽出  
# ※列のみであれば
# * iloc: Integer LOCation  
# 列（や行）を整数によって範囲を指定して抽出

# In[67]:


train = df.loc[:'2018-06-30', ['user']] # 2018-06-30より前のuser列を抽出
test = df.loc[:, ['user']] # 全期間のuser列を抽出
test.head()


# ## データの可視化

# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))
plt.plot(train)
plt.show()


# ## 前処理

# ### 階差

# In[6]:


train.head()


# In[7]:


train.shift().head() # shift(): 1つずらした値


# In[8]:


train_dif = train - train.shift() # 訓練データの階差
test_dif = test - test.shift() # テストデータの階差

train_dif, test_dif = train_dif.dropna(), test_dif.dropna()
train_dif.head()


# In[9]:


plt.figure(figsize=(12, 4))
plt.plot(train_dif)
plt.show()


# ### 対数変換

# In[71]:


import numpy as np

train_log = np.log(train)

plt.figure(figsize=(12, 4))
plt.plot(train_log)
plt.show()


# ### 対数差分

# In[11]:


train_log_dif = train_log - train_log.shift()
train_log_dif = train_log_dif.dropna()
plt.figure(figsize=(12, 4))
plt.plot(train_log_dif)
plt.show()


# In[12]:


test_log = np.log(test)
test_log_dif = test_log - test_log.shift()
plt.figure(figsize=(12, 4))
plt.plot(test_log_dif)
plt.show()


# ***
# ## 自己相関  
# * tsa: Time Series Analysis  
# * acf: AutoCorrelation Function
# * nlags: 自己相関の次数

# In[13]:


import statsmodels.api as sm

train_acf = sm.tsa.stattools.acf(train_log_dif, nlags=40)
fig = plt.figure(figsize=(12, 4))
plt.plot(train_acf)
plt.show()


# ## 偏自己相関  
# * pacf: Partial AutoCorrelation Function（偏自己相関）
# * ols: Ordinary Least Squares regression（最小二乗回帰）
# * 他にもywunbiased: yule walker法など

# In[14]:


train_pacf = sm.tsa.stattools.pacf(train_log_dif, nlags=40,
                                   method='ols')
fig = plt.figure(figsize=(12, 4))
plt.plot(train_pacf)
plt.show()


# * lags: （偏）自己相関の次数

# ### 信頼区間付き

# In[15]:


fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(211) # 2行1列の1つ目
fig = sm.graphics.tsa.plot_acf(train_log_dif, lags=40, ax=ax1) # 自己相関係数
ax2 = fig.add_subplot(212) # 2行1列の2つ目
fig = sm.graphics.tsa.plot_pacf(train_log_dif, lags=40, ax=ax2) # 偏自己相関係数


# ***
# ## ARモデル
# * AR: AutoRegressive（自己回帰）
# 
# ### ARモデルの生成と学習
# * maxlag: ARモデルの次数
# * ic: Information Criterion（情報量規準）  
# aic: 赤池情報量規準
# * trend: 定数を含めるかどうか  
# c: 含める、nc: 含めない

# In[16]:


from statsmodels.tsa.ar_model import AR

ar = AR(train_log_dif, freq='D').fit(maxlag=5, ic='aic', trend='nc')
ar.params # 各パラメータを確認


# ### ARモデルで予測

# In[17]:


predict = ar.predict('2018-7', '2018-10')
plt.figure(figsize=(12, 4))
plt.plot(test_log_dif[test_log_dif.index.year > 2017])
plt.plot(predict, 'r')
plt.show()


# ## MAモデル
# * MA: Moving Average
# 
# ### MAモデルの生成と学習
# * order: ARMAモデルの次数
# * mle: Maximum Likelihood Estimation（最尤法）

# In[18]:


from statsmodels.tsa.arima_model import ARMA

ma = ARMA(train_log_dif, order=(0, 2), freq='D').fit(method='mle', trend='nc')
ma.params


# ### MAモデルで予測

# In[19]:


predict = ma.predict('2018-7', '2018-10')
plt.figure(figsize=(12, 4))
plt.plot(test_log_dif[test_log_dif.index.year > 2017])
plt.plot(predict, 'r')
plt.show()


# ## ARMAモデル
# * ARMA: AutoRegressive Moving Average（自己回帰移動平均）
# ### AIC（赤池情報量規準）によるモデル選択

# In[20]:


import warnings
warnings.filterwarnings('ignore')

res = sm.tsa.arma_order_select_ic(train_log_dif, ic='aic', trend='nc',
                                 model_kw={'freq': 'D'})


# In[21]:


res['aic']


# In[22]:


res['aic_min_order']


# ### ARMAモデル生成と学習

# In[23]:


import warnings
warnings.filterwarnings('ignore')
arma = ARMA(train_log_dif, freq='D', order=(4, 2)).fit()
arma.params


# ### ARMAモデルで予測
# * plot_predict: 信頼区間付きで結果を描画

# In[24]:


fig, ax = plt.subplots(figsize=(12,6))
ax = test_log_dif.loc['2018':].plot(ax=ax)
fig = arma.plot_predict('2018-7', '2018-10', ax=ax, plot_insample=False)
plt.show()


# ### 残差（ホワイトノイズ）$\varepsilon_t$の確認
# * resid: RESIDual error（残差）
# * 残差（ホワイトノイズ）は定常性を満たすので自己相関、偏自己相関からデータの性質を読み取ることができる

# In[25]:


resid = arma.resid
fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)


# ## ARIMAモデル
# * ARIMA: AutoRegressive Integrated Moving Average（自己回帰和分移動平均）
# * 階差 $\Delta y_t:=y_t-y_{t-1}$ がARMA過程であると仮定->あとで足し合わせる
# 
# ### ARIMAモデルの生成と学習
# * order: ARIMAモデルの次数 $(p, d, q)$

# In[26]:


from statsmodels.tsa.arima_model import ARIMA

arima = ARIMA(train, freq='D', order=(2, 1, 2)).fit()
arima.params


# In[27]:


fig, ax = plt.subplots(figsize=(12,6))
ax = test.loc['2018':].plot(ax=ax)
fig = arima.plot_predict('2018-6', '2018-10', ax=ax, plot_insample=False)
plt.show()


# ## SARIMAモデル
# * SARIMA: Seasonal ARIMA（季節ARIMAモデル）
# 
# ### SARIMAモデルの生成と学習
# * seasonal_order: 季節パラメータの次数 $(sp, sd, sq, s)$  
# $s$: 期間の長さ

# In[28]:


from statsmodels.tsa.statespace.sarimax import SARIMAX

sarima = SARIMAX(train, freq='D', order=(2, 1, 2), 
                 seasonal_order=(1, 1, 1, 7)).fit()
sarima.params


# ### 残差（ホワイトノイズ）$\varepsilon_t$の確認

# In[29]:


resid = sarima.resid
fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)


# ### SARIMAモデルで予測

# In[30]:


predict = sarima.predict('2018-6','2018-10')
predict_dy = sarima.get_prediction('2018-6','2018-10')
predict_dy_ci = predict_dy.conf_int(alpha=0.05)

plt.figure(figsize=(12,6))
plt.plot(test[test.index.year > 2017])
plt.plot(predict, 'r')
plt.fill_between(predict_dy_ci.index, predict_dy_ci.iloc[:, 0], 
                 predict_dy_ci.iloc[:, 1], color='g', alpha=0.2)
plt.show()


# ***
# ## AICを用いたモデル選択
# ### 総当たり法でARIMAモデルの最適な次数を選択

# In[31]:


p_max, d_max, q_max = 2, 1, 2
pattern = p_max * (d_max + 1) * (q_max + 1)

result = pd.DataFrame(index=range(pattern), columns=['model', 'aic'])
num = 0
for p in range(1, p_max + 1):
    for d in range(d_max + 1):
        for q in range(q_max + 1):
            arima = ARIMA(
                train, order=(p, d, q), freq='D'
            ).fit(method='css', maxiter=300, dist=False)
            result.iloc[num]['model'] = 'order=({}, {}, {})'.format(p, d, q)
            result.iloc[num]['aic'] = arima.aic
            num += 1
            
result[result.aic == min(result.aic)]


# In[32]:


p_max, q_max, d_max = 2, 2, 2
max_sp, max_sq, max_sd = 1, 1, 1

pattern = p_max * (q_max + 1) * (d_max + 1)             * (max_sp + 1) * (max_sq + 1) * (max_sd + 1)

result = pd.DataFrame(index=range(pattern), columns=["model", "aic"])
num = 0
for p in range(1, p_max + 1):
    for d in range(d_max + 1):
        for q in range(q_max + 1):
            for sp in range(max_sp + 1):
                for sd in range(max_sd + 1):
                    for sq in range(max_sq + 1):
                        try:
                            sarima = SARIMAX(
                                train_log_dif, order=(p, d, q), 
                                seasonal_order=(sp, sd, sq, 7), 
                                enforce_stationarity = False, 
                                enforce_invertibility = False,
                                freq='D'
                            ).fit(method='bfgs', maxiter=300, disp=False)
                            result.iloc[num]['model'] = 'order=({},{},{}), season=({},{},{})'.format(p, d, q, sp, sd, sq)
                            result.iloc[num]['aic'] = sarima.aic
                            num += 1
                        except:
                            pass
                        
result[result.aic == min(result.aic)]


# *** 
# ## 予測精度
# ### RMSE (scikit-learnを利用)

# In[42]:


from sklearn.metrics import mean_squared_error

arima_predict = arima.predict('2018-6','2018-10')
print(arima_prediction.head())
print()
print(arima_predict.tail())
np.sqrt(mean_squared_error(arima_predict, test.loc['2018-06-01':'2018-10-01']))


# In[43]:


sarima = SARIMAX(train, freq='D', order=(1, 0, 2), 
                 seasonal_order=(0, 1, 1, 7)).fit()
sarima_predict = sarima.predict('2018-6','2018-10')
print(sarima_predict.head())
print()
print(sarima_predict.tail())
np.sqrt(mean_squared_error(sarima_predict, test.loc['2018-06-01':'2018-10-01']))


# In[44]:


predict_dy = sarima.get_prediction('2018-6','2018-10')
predict_dy_ci = predict_dy.conf_int(alpha=0.05)

plt.figure(figsize=(12,6))
plt.plot(test[test.index.year > 2017])
plt.plot(predict, 'r')
plt.fill_between(predict_dy_ci.index, predict_dy_ci.iloc[:, 0], 
                 predict_dy_ci.iloc[:, 1], color='g', alpha=0.2)
plt.show()

