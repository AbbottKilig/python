
# coding: utf-8

# In[1]:


import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense,Activation
from keras.optimizers import Adam,SGD
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# # 生成数据

# In[13]:


def getData():
    X = np.linspace(0, 2 * np.pi, 1000)
    X = X[: np.newaxis]
    y = np.sin(X)
    return X,y


# In[14]:


X,y = getData()
plt.plot(X,y)


# # 定义模型

# In[19]:


def model():
    model = Sequential()
    model.add(Dense(64,input_dim=1,activation='relu'))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(optimizer ='adam',loss = 'mse')
    return model


# In[20]:


model = model()


# # 训练

# In[21]:


model.fit(X,y,batch_size= 12,epochs=10,shuffle=True, verbose=1)


# In[22]:


y_hat = model.predict(X)


# In[23]:


plt.plot(X, y, 'b', X, y_hat, 'r--')


# ## 可以看到拟合效果并不好，增大训练次数为100次

# In[26]:


model.fit(X,y,batch_size= 12,epochs=100,shuffle=True, verbose=1)


# In[27]:


y_hat = model.predict(X)
plt.plot(X, y, 'b', X, y_hat, 'r--')


# ## 效果所有改善，增大为1000次

# In[28]:


model.fit(X,y,batch_size= 12,epochs=1000,shuffle=True, verbose=1)


# In[30]:


y_hat = model.predict(X)
plt.plot(X, y, 'b', X, y_hat, 'r--')


# ### 可以看到拟合效果比100好，但是拟合范围限于0-π，无法拟合y小于0的情况，什么原因呢？

# In[29]:


def sigmoid(z):
    return 1 / (np.exp(-z) + 1)


# In[31]:


z = np.linspace(-5, 5, 1000)
s = sigmoid(z)


# In[32]:


plt.plot(z,s)


# ### sigmoid激活函数返回值总大于0，所以神经网络输出为大于0的值，无法拟合负数

# ### 解决方法：调整目标值y的范围为0-1之间

# In[34]:


y = (y + 1)/2


# ## 重新训练

# In[35]:


model.fit(X,y,batch_size= 12,epochs=1000,shuffle=True, verbose=1)


# In[36]:


y_hat = model.predict(X)
plt.plot(X, y, 'b', X, y_hat, 'r--')


# # 训练结束，拟合相对较好。接下来可调整参数
# - 数据范围
# - 迭代次数
# - 模型神经单元个数
# - 模型神经层数

# # 模型在小样本上的表现

# In[39]:


X = np.arange(0, 100, 1)
y = (np.sin(X) + 1)/2


# In[40]:


y_hat = model.predict(X)
plt.plot(X, y, 'b', X, y_hat, 'r--')


# ## 拟合效果又不行了
# ### 原因：
# - 训练集和测试集分布应该相同
