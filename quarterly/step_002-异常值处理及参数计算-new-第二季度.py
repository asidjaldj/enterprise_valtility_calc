#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#读取" data-toc-modified-id="读取-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>读取</a></span><ul class="toc-item"><li><span><a href="#调整参数X18(临时更改)" data-toc-modified-id="调整参数X18(临时更改)-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>调整参数X18(临时更改)</a></span></li></ul></li><li><span><a href="#划分行业" data-toc-modified-id="划分行业-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>划分行业</a></span></li><li><span><a href="#异常值处理" data-toc-modified-id="异常值处理-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>异常值处理</a></span><ul class="toc-item"><li><span><a href="#计算均值和标准差" data-toc-modified-id="计算均值和标准差-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>计算均值和标准差</a></span></li><li><span><a href="#空值填充" data-toc-modified-id="空值填充-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>空值填充</a></span></li><li><span><a href="#计算取值范围" data-toc-modified-id="计算取值范围-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>计算取值范围</a></span></li><li><span><a href="#将非0的数据标准化" data-toc-modified-id="将非0的数据标准化-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>将非0的数据标准化</a></span></li><li><span><a href="#重新计算平均值" data-toc-modified-id="重新计算平均值-3.5"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>重新计算平均值</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.6"><span class="toc-item-num">3.6&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#行业指标调节参数计算" data-toc-modified-id="行业指标调节参数计算-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>行业指标调节参数计算</a></span><ul class="toc-item"><li><span><a href="#调节参数计算" data-toc-modified-id="调节参数计算-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>调节参数计算</a></span></li><li><span><a href="#调节参数存储" data-toc-modified-id="调节参数存储-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>调节参数存储</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-4.2.1"><span class="toc-item-num">4.2.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li></ul></li><li><span><a href="#企业规模调节参数" data-toc-modified-id="企业规模调节参数-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>企业规模调节参数</a></span><ul class="toc-item"><li><span><a href="#划分规模" data-toc-modified-id="划分规模-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>划分规模</a></span></li><li><span><a href="#按规模计算平均值" data-toc-modified-id="按规模计算平均值-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>按规模计算平均值</a></span></li><li><span><a href="#调节参数计算" data-toc-modified-id="调节参数计算-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>调节参数计算</a></span></li><li><span><a href="#调节参数存储" data-toc-modified-id="调节参数存储-5.4"><span class="toc-item-num">5.4&nbsp;&nbsp;</span>调节参数存储</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-5.4.1"><span class="toc-item-num">5.4.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li></ul></li><li><span><a href="#归一化处理(min-max标准化)" data-toc-modified-id="归一化处理(min-max标准化)-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>归一化处理(min-max标准化)</a></span></li><li><span><a href="#保存" data-toc-modified-id="保存-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>保存</a></span></li></ul></div>

# In[1]:


import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")


# # 读取

# In[2]:


path_dc = './DataCleaning_quarterTwo_1.csv'
dc = pd.read_csv(path_dc, index_col=[0])
print(dc.info(null_counts = True))
dc[:2]


# ## 调整参数X18(临时更改)

# In[3]:


dc['X18'] = np.random.randint(0, 10, len(dc))
print(dc['X18'].value_counts())


# # 划分行业

# In[4]:


grouped = dc.groupby('hydm')
grouped.size()


# In[5]:


group_A = grouped.get_group('A').reset_index()
group_B = grouped.get_group('B').reset_index()
group_C = grouped.get_group('C').reset_index()
group_D = grouped.get_group('D').reset_index()
group_E = grouped.get_group('E').reset_index()
group_F = grouped.get_group('F').reset_index()
group_G = grouped.get_group('G').reset_index()
group_H = grouped.get_group('H').reset_index()
group_I = grouped.get_group('I').reset_index()
group_J = grouped.get_group('J').reset_index()
group_K = grouped.get_group('K').reset_index()
group_L = grouped.get_group('L').reset_index()
group_M = grouped.get_group('M').reset_index()
group_N = grouped.get_group('N').reset_index()
group_O = grouped.get_group('O').reset_index()
group_P = grouped.get_group('P').reset_index()
group_Q = grouped.get_group('Q').reset_index()
group_R = grouped.get_group('R').reset_index()
group_S = grouped.get_group('S').reset_index()
group_T = grouped.get_group('T').reset_index()
group_Z = grouped.get_group('Z').reset_index()


# # 异常值处理

# 定义超出 1.5 倍标准差范围的指标值为`异常值`     
# 对于这些企业的指标取值，令其`等于` ***1.5 倍标准差***    
# 为避免不同行业中各指标的取值差异比较大导致误判，**分行业**进行异常处理。
# 
# > 由于存在大量的缺失值并填充为0，故只挑选!=0的值进行异常值计算
# >> 最后处理异常值的时候也只处理有值的位置

# 共有8个特征包含真实值
# - X5
# - X6
# - X7
# - X10
# - X11
# - X12
# - X13
# - X14
# > 临时使X18包含随机数

# ## 计算均值和标准差

# In[6]:


feature_list = ['X5', 'X6', 'X7', 'X10', 'X11', 'X12', 'X13', 'X14', 'X18']
alphabet = [chr(i) for i in range(65, 85)] # 'B' - 'T'
alphabet.append(chr(90)) # "Z"
print(alphabet)


# In[7]:


X5_mean, X5_std = [], []
X6_mean, X6_std = [], []
X7_mean, X7_std = [], []
X10_mean, X10_std = [], []
X11_mean, X11_std = [], []
X12_mean, X12_std = [], []
X13_mean, X13_std = [], []
X14_mean, X14_std = [], []

X18_mean, X18_std = [], []


# In[8]:


for i in tqdm(feature_list):
    # 一下语句把固定的string改为变量名
    temp_mean = np.str(i) + '_mean'
    temp_std = np.str(i) + '_std'
    for j in alphabet:
        temp_alpha = 'group_' + np.str(j)
        eval(temp_mean).append(eval(temp_alpha)[eval(temp_alpha)[i] > 0][i].mean())
        # eval(temp_alpha)[eval(temp_alpha)[i] > 0][i]
        '''
        举例
        group_A[group_A['X5'] > 0]
        # dataframe
        group_A[group_A['X5'] > 0]['X5']
        # series
        '''
        eval(temp_std).append(eval(temp_alpha)[eval(temp_alpha)[i] > 0][i].std())


# ## 空值填充

# In[9]:


def fill_nan(temp_list):
    temp_list_nan = np.isnan(temp_list)
    for i in range(len(temp_list)):
        if temp_list_nan[i] == True:
            temp_list[i] = 0


# In[10]:


for i in feature_list:
    # 一下语句把固定的string改为变量名
    temp_mean = np.str(i) + '_mean'
    temp_std = np.str(i) + '_std'
    fill_nan(eval(temp_mean))
    fill_nan(eval(temp_std))


# ## 计算取值范围

# In[11]:


X5_min = np.array(X5_mean) - 1.5 * np.array(X5_std)
X5_max = np.array(X5_mean) + 1.5 * np.array(X5_std)
X6_min = np.array(X6_mean) - 1.5 * np.array(X6_std)
X6_max = np.array(X6_mean) + 1.5 * np.array(X6_std)
X7_min = np.array(X7_mean) - 1.5 * np.array(X7_std)
X7_max = np.array(X7_mean) + 1.5 * np.array(X7_std)
X10_min = np.array(X10_mean) - 1.5 * np.array(X10_std)
X10_max = np.array(X10_mean) + 1.5 * np.array(X10_std)
X11_min = np.array(X11_mean) - 1.5 * np.array(X11_std)
X11_max = np.array(X11_mean) + 1.5 * np.array(X11_std)
X12_min = np.array(X12_mean) - 1.5 * np.array(X12_std)
X12_max = np.array(X12_mean) + 1.5 * np.array(X12_std)
X13_min = np.array(X13_mean) - 1.5 * np.array(X13_std)
X13_max = np.array(X13_mean) + 1.5 * np.array(X13_std)
X14_min = np.array(X14_mean) - 1.5 * np.array(X14_std)
X14_max = np.array(X14_mean) + 1.5 * np.array(X14_std)

X18_min = np.array(X18_mean) - 1.5 * np.array(X18_std)
X18_max = np.array(X18_mean) + 1.5 * np.array(X18_std)


# ## 将非0的数据标准化

# In[12]:


for i in tqdm(feature_list):
    for j in range(len(alphabet)):
        temp_max = np.str(i) + '_max'
        temp_min = np.str(i) + '_min'
        temp_alpha = 'group_' + np.str(alphabet[j])
        eval(temp_alpha).loc[(eval(temp_alpha)[i] > 0) & (eval(temp_alpha)[i] < eval(temp_min)[j]), i] = eval(temp_min)[j]
        eval(temp_alpha).loc[eval(temp_alpha)[i] > eval(temp_max)[j], i] = eval(temp_max)[j]


# ## 重新计算平均值
# 
# > 计算调节指标时需要用到，由于这一步更改了列名称，固放到前面

# In[13]:


X5_mean = []
X6_mean = []
X7_mean = []
X10_mean = []
X11_mean = []
X12_mean = []
X13_mean = []
X14_mean = []

X18_mean = []

for i in tqdm(feature_list):
    # 一下语句把固定的string改为变量名
    temp_mean = np.str(i) + '_mean'
    for j in alphabet:
        temp_alpha = 'group_' + np.str(j)
        eval(temp_mean).append(eval(temp_alpha)[i].mean())


# ## join

# 按行业分类的数据已经经过了异常值处理，现在要将此数据放入到原文件`dc`中

# In[14]:


# 由于要使用join函数，先将蓄更改的同名的列置为空值
for i in feature_list:
    dc[i] = None


# In[15]:


for i in tqdm(alphabet):
    temp_alpha = 'group_' + np.str(i)
    eval(temp_alpha).set_index('nbxh', inplace=True)
    globals()[temp_alpha] = eval(temp_alpha)[feature_list]# 提取出需要更改的列
    # 更改列名
    eval(temp_alpha).rename(
        columns={'X5': 'X5_fill', 'X6': 'X6_fill', 'X7':'X7_fill', 'X10':'X10_fill', 
                 'X11': 'X11_fill', 'X12': 'X12_fill', 'X13':'X13_fill', 'X14':'X14_fill', 'X18':'X18_fill'}, 
        inplace=True)
    dc = dc.join(eval(temp_alpha))
    dc['X5'].fillna(dc['X5_fill'], inplace=True)
    dc.drop(['X5_fill'], axis=1, inplace=True)
    dc['X6'].fillna(dc['X6_fill'], inplace=True)
    dc.drop(['X6_fill'], axis=1, inplace=True)
    dc['X7'].fillna(dc['X7_fill'], inplace=True)
    dc.drop(['X7_fill'], axis=1, inplace=True)
    dc['X10'].fillna(dc['X10_fill'], inplace=True)
    dc.drop(['X10_fill'], axis=1, inplace=True)
    dc['X11'].fillna(dc['X11_fill'], inplace=True)
    dc.drop(['X11_fill'], axis=1, inplace=True)
    dc['X12'].fillna(dc['X12_fill'], inplace=True)
    dc.drop(['X12_fill'], axis=1, inplace=True)
    dc['X13'].fillna(dc['X13_fill'], inplace=True)
    dc.drop(['X13_fill'], axis=1, inplace=True)
    dc['X14'].fillna(dc['X14_fill'], inplace=True)
    dc.drop(['X14_fill'], axis=1, inplace=True)
    
    dc['X18'].fillna(dc['X18_fill'], inplace=True)
    dc.drop(['X18_fill'], axis=1, inplace=True)


# # 行业指标调节参数计算

# In[16]:


X5_mean_all = dc['X5'].mean()
X6_mean_all = dc['X6'].mean()
X7_mean_all = dc['X7'].mean()
X10_mean_all = dc['X10'].mean()
X11_mean_all = dc['X11'].mean()
X12_mean_all = dc['X12'].mean()
X13_mean_all = dc['X13'].mean()
X14_mean_all = dc['X14'].mean()

X18_mean_all = dc['X18'].mean()


# ## 调节参数计算

# In[17]:


# 定义列表用来存储行业调节参数
a_5 = []
a_6 = []
a_7 = []
a_10 = []
a_11 = []
a_12 = []
a_13 = []
a_14 = []

a_18 = []


# In[18]:


industry_num = 21
def industry_parameter(temp_mean_all, temp_mean, temp_list):
    for i in range(industry_num):
        if temp_mean[i] != 0:
            temp_list.append(temp_mean_all / temp_mean[i])
        else:
            temp_list.append(1) 


# In[19]:


industry_parameter(X5_mean_all, X5_mean, a_5)
industry_parameter(X6_mean_all, X6_mean, a_6)
industry_parameter(X7_mean_all, X7_mean, a_7)
industry_parameter(X10_mean_all, X10_mean, a_10)
industry_parameter(X11_mean_all, X11_mean, a_11)
industry_parameter(X12_mean_all, X12_mean, a_12)
industry_parameter(X13_mean_all, X13_mean, a_13)
industry_parameter(X14_mean_all, X14_mean, a_14)
industry_parameter(X18_mean_all, X18_mean, a_18)


# ## 调节参数存储

# In[20]:


para_1 = pd.DataFrame(data=None, 
                      columns=['I_1_2', 'I_3', 'I_4', 'I_5', 'I_6', 'I_7', 'I_8', 'I_9', 'I_10', 'I_11', 'I_12', 'I_13', 'I_14', 'I_15', 'I_16', 'I_17', 'I_18'],
                      index=alphabet)


# In[21]:


para_1


# In[22]:


para_1['I_5'] = a_5
para_1['I_6'] = a_6
para_1['I_7'] = a_7
para_1['I_6'] = a_10
para_1['I_11'] = a_11
para_1['I_12'] = a_12
para_1['I_13'] = a_13
para_1['I_14'] = a_14

para_1['I_18'] = a_18


# In[23]:


para_1.fillna(value=1, inplace=True)


# In[24]:


para_1


# ### 保存

# In[25]:


path_para = './para_half_1.csv'
para_1.to_csv(path_para)


# # 企业规模调节参数

# ## 划分规模

# In[26]:


grouped_scale = dc.groupby('scale')
grouped_scale.size()


# In[27]:


group_1 = grouped_scale.get_group(1).reset_index()
group_2 = grouped_scale.get_group(2).reset_index()
group_3 = grouped_scale.get_group(3).reset_index()
group_4 = grouped_scale.get_group(4).reset_index()
group_5 = grouped_scale.get_group(5).reset_index()


# ## 按规模计算平均值

# In[28]:


group_list = [1, 2, 3, 4, 5]

X5_mean_S = []
X6_mean_S = []
X7_mean_S = []
X10_mean_S = []
X11_mean_S = []
X12_mean_S = []
X13_mean_S = []
X14_mean_S = []

X18_mean_S = []

for i in tqdm(feature_list):
    # 一下语句把固定的string改为变量名
    temp_mean = np.str(i) + '_mean_S'
    for j in group_list:
        temp_alpha = 'group_' + np.str(j)
        eval(temp_mean).append(eval(temp_alpha)[i].mean())


# ## 调节参数计算

# In[29]:


# 定义列表用来存储行业调节参数
a_5_s = []
a_6_s = []
a_7_s = []
a_10_s = []
a_11_s = []
a_12_s = []
a_13_s = []
a_14_s = []

a_18_s = []


# In[30]:


scale_num = 5
def scale_parameter(temp_mean_all, temp_mean, temp_list):
    for i in range(scale_num):
        if temp_mean[i] != 0:
            temp_list.append(temp_mean_all / temp_mean[i])
        else:
            temp_list.append(1) 


# In[31]:


scale_parameter(X5_mean_all, X5_mean_S, a_5_s)
scale_parameter(X6_mean_all, X6_mean_S, a_6_s)
scale_parameter(X7_mean_all, X7_mean_S, a_7_s)
scale_parameter(X10_mean_all, X10_mean_S, a_10_s)
scale_parameter(X11_mean_all, X11_mean_S, a_11_s)
scale_parameter(X12_mean_all, X12_mean_S, a_12_s)
scale_parameter(X13_mean_all, X13_mean_S, a_13_s)
scale_parameter(X14_mean_all, X14_mean_S, a_14_s)

scale_parameter(X18_mean_all, X18_mean_S, a_18_s)


# ## 调节参数存储

# In[32]:


lis = ['N1', 'N2', 'N3', 'N4', 'N5']
para_2 = pd.DataFrame(data=None, 
                      columns=['S_1_2', 'S_3', 'S_4', 'S_5', 'S_6', 'S_7', 'S_8', 'S_9', 'S_10', 'S_11', 'S_12', 'S_13', 'S_14', 'S_15', 'S_16', 'S_17', 'S_18'],
                      index=lis)


# In[33]:


para_2


# In[34]:


para_2['S_5'] = a_5_s
para_2['S_6'] = a_6_s
para_2['S_7'] = a_7_s
para_2['S_10'] = a_10_s
para_2['S_11'] = a_11_s
para_2['S_12'] = a_12_s
para_2['S_13'] = a_13_s
para_2['S_14'] = a_14_s

para_2['S_18'] = a_18_s

para_2.fillna(value=1, inplace=True)
para_2


# ### 保存

# In[35]:


path_para = './para_half_2.csv'
para_2.to_csv(path_para)


# # 归一化处理(min-max标准化)

# In[36]:


for i in tqdm(feature_list):
    dc[i] = (dc[i] - dc[i].min())/ (dc[i].max() - dc[i].min())


# In[37]:


dc.info(null_counts = True)


# In[38]:


dc.fillna(value = 0.0, inplace=True)


# # 保存

# In[39]:


path_dataclean_2 = './DataCleaning_quarterTwo_2.csv'
dc.to_csv(path_dataclean_2)

