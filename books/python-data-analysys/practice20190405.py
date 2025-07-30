
# coding: utf-8

# # Python時系列データ分析入門（演習問題解答）

# ## 問題
# ### 配布したデータ”AirPassengers.csv”を用いて以下の 問題を実装せよ     

# ### ①csvファイルをDataFrame型の変数として読み込み、デー タの数を確認せよ

# In[1]:


import pandas as pd

df = pd.read_csv('AirPassengers.csv')
df.info()


# In[2]:


df = pd.read_csv('AirPassengers.csv', index_col='Month', parse_dates=True, dtype=float)
df = df.dropna()
df.info()


# In[3]:


df.shape


# ### A. 144

# ***
# ### ②データを可視化し、定常性があるか確認せよ

# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))
plt.plot(df)
plt.show()


# ### A. 定常性は確認できない

# ***
# ### ③データの偏自己相関係数を求め、データを可視化せよ

# In[5]:


import statsmodels.api as sm

train = df.loc[:'1958-12-1', ['#Passengers']]
test = df['#Passengers']

pacf = sm.tsa.stattools.pacf(train, nlags=40, method='ols')
fig = plt.figure(figsize=(12, 4))
plt.plot(pacf)
print(pacf)
plt.show()


# ***
# ### ④データに周期性があるか確認せよ。また、確認できる 場合はどれくらいの周期か考察せよ

# In[6]:


fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(train, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(train, lags=40, ax=ax2, method='ols')
plt.show()


# In[7]:


train_dif = train.diff()
train_dif = train_dif.dropna()


# In[8]:


fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(train_dif, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(train_dif, lags=40, ax=ax2, method='ols')
plt.show()


# ### A. 周期12

# ***
# ### ⑤今日学んだ時系列モデルの枠組みだと、どのモデルが 一番有効であるか考察せよ

# ### A. 非定常性データであること、周期性があることからSARIMAモデルが適していると考えられる

# ***
# ### ⑥講義のプログラムを参考にして、SARIMAモデルの中で当てはまりのよさそうな次数をAICを用いて求めよ

# In[9]:


from statsmodels.tsa.statespace.sarimax import SARIMAX

sarima = SARIMAX(train, freq='MS', order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)).fit()
resid = sarima.resid
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)
plt.show()


# In[10]:


p_max, d_max, q_max = 2, 2, 2
max_sp, max_sd, max_sq = 1, 1, 1
pattern = p_max
for mx in [d_max, q_max, max_sp, max_sd, max_sq]:
    pattern *= mx + 1
result = pd.DataFrame(index=range(pattern), columns=['model', 'aic'])
num = 0
for p in range(1, p_max + 1):
    for d in range(0, d_max + 1):
        for q in range(0, q_max + 1):
            for sp in range(0, max_sp + 1):
                for sd in range(0, max_sd + 1):
                    for sq in range(0, max_sq + 1):
                        try:
                            sarima = SARIMAX(
                            train, freq='MS', order=(p,d,q), 
                            seasonal_order=(sp,sd,sq,12), 
                            enforce_stationarity = False, 
                            enforce_invertibility = False
                            ).fit(method='bfgs', maxiter=300, disp=False)
                            result.iloc[num]["model"] = 'order=({},{},{}), season=({},{},{})'.format(p, d, q, sp, sd, sq)
                            result.iloc[num]["aic"] = sarima.aic
                            num = num + 1
                        except:
                            pass
result[result.aic == min(result.aic)]


# In[14]:


sarima = SARIMAX(train, freq='MS', order=(1, 2, 2), seasonal_order=(0, 1, 1, 12)).fit()
predict = sarima.predict('1958-12', '1960-12')
predict_dy = sarima.get_prediction('1958-12','1960-12')
predict_dy_ci = predict_dy.conf_int(alpha=0.05)

plt.figure(figsize=(12,6))
plt.plot(test[test.index.year > 1950])
plt.plot(predict,"r")
plt.fill_between(predict_dy_ci.index, predict_dy_ci.iloc[:, 0], 
                 predict_dy_ci.iloc[:, 1], color='g', alpha=0.2)
plt.show()


# ***
# ## おまけ: Google Trendsから取得したCSVデータを分析

# In[11]:


import pandas as pd

df = pd.read_csv('silent_siren.csv')
df.head()


# In[12]:


df = pd.read_csv('silent_siren.csv', header=1, parse_dates=True) # header=1として0行目を無視
df.columns = ['week', '#searches'] # 列名を変更
df = df.set_index('week').astype(float) # 'week'をインデックスに割り当て、データ型をfloatに
df.head()


# In[13]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 5))
plt.plot(df)
plt.show()

