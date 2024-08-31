#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#读取" data-toc-modified-id="读取-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>读取</a></span><ul class="toc-item"><li><span><a href="#读取主表" data-toc-modified-id="读取主表-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>读取主表</a></span></li><li><span><a href="#读取调节参数" data-toc-modified-id="读取调节参数-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>读取调节参数</a></span></li></ul></li><li><span><a href="#活跃度计算" data-toc-modified-id="活跃度计算-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>活跃度计算</a></span><ul class="toc-item"><li><span><a href="#添加临时列" data-toc-modified-id="添加临时列-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>添加临时列</a></span></li><li><span><a href="#计算整体活跃度" data-toc-modified-id="计算整体活跃度-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>计算整体活跃度</a></span></li><li><span><a href="#groupby" data-toc-modified-id="groupby-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>groupby</a></span></li><li><span><a href="#定义分类活跃度函数" data-toc-modified-id="定义分类活跃度函数-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>定义分类活跃度函数</a></span></li><li><span><a href="#按行业" data-toc-modified-id="按行业-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>按行业</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.5.1"><span class="toc-item-num">2.5.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#按规模" data-toc-modified-id="按规模-2.6"><span class="toc-item-num">2.6&nbsp;&nbsp;</span>按规模</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.6.1"><span class="toc-item-num">2.6.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#按城市" data-toc-modified-id="按城市-2.7"><span class="toc-item-num">2.7&nbsp;&nbsp;</span>按城市</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.7.1"><span class="toc-item-num">2.7.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#按三次产业" data-toc-modified-id="按三次产业-2.8"><span class="toc-item-num">2.8&nbsp;&nbsp;</span>按三次产业</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.8.1"><span class="toc-item-num">2.8.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#按经济户口类别" data-toc-modified-id="按经济户口类别-2.9"><span class="toc-item-num">2.9&nbsp;&nbsp;</span>按经济户口类别</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.9.1"><span class="toc-item-num">2.9.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#按企业存续时间" data-toc-modified-id="按企业存续时间-2.10"><span class="toc-item-num">2.10&nbsp;&nbsp;</span>按企业存续时间</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.10.1"><span class="toc-item-num">2.10.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#按是否外商投资" data-toc-modified-id="按是否外商投资-2.11"><span class="toc-item-num">2.11&nbsp;&nbsp;</span>按是否外商投资</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.11.1"><span class="toc-item-num">2.11.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li><li><span><a href="#三次产业的分行业占比" data-toc-modified-id="三次产业的分行业占比-2.12"><span class="toc-item-num">2.12&nbsp;&nbsp;</span>三次产业的分行业占比</a></span><ul class="toc-item"><li><span><a href="#保存" data-toc-modified-id="保存-2.12.1"><span class="toc-item-num">2.12.1&nbsp;&nbsp;</span>保存</a></span></li></ul></li></ul></li></ul></div>

# In[1]:


import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm
import datetime
import time
import os
warnings.filterwarnings("ignore")


# In[2]:


def mkdir(path):
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False


# In[3]:


i = datetime.datetime.now()
time_str = str(i.year) + '_' + str(i.month) + '_' + str(i.day) + '_hour' + str(i.hour)+ '(half)'
# 定义要创建的文件夹
mkpath = '.\\' + time_str 
# 调用函数
mkdir(mkpath)


# # 读取

# ## 读取主表

# In[4]:


path_dc = './DataCleaning_quarterTwo_2.csv'
dc = pd.read_csv(path_dc, index_col=[0])
print(dc.info(null_counts = True))
dc[:2]


# ## 读取调节参数

# In[5]:


path_para_1 = './para_half_1.csv'
industry = pd.read_csv(path_para_1, index_col=[0])
industry


# In[6]:


path_para_2 = './para_half_2.csv'
scale = pd.read_csv(path_para_2, index_col=[0])
scale


# In[7]:


# 给定权重
weight = [0.4, 0.15, 0.15, 0.05, 0.05, 0.05, 0.02, 0.02, 0.025, 0.025, 0.01, 0.01, 0.04, -0.03, -0.01, -0.01, 0.05]
print(weight)

alphabet_all = [chr(i) for i in range(65, 85)]
alphabet_all.append(chr(90))
print(alphabet_all)


# # 活跃度计算

# 接下来的操作是将`行业调节参数`&`规模调节参数`&`权重`按位相乘，得到一个 （行业类别 * 规模类别） * 特征数 大小的矩阵

# In[8]:


industry_matrix = industry.values
scale_matrix = scale.values

print(industry_matrix.shape, '\t', scale_matrix.shape)


# In[9]:


IS_matrix = industry_matrix * scale_matrix[0]
for i in tqdm(range(1, 5)):
    IS_matrix = np.concatenate((IS_matrix, (industry_matrix * scale_matrix[i])))
print(IS_matrix.shape)


# In[10]:


ISW_matrix = IS_matrix * np.array(weight)
print(ISW_matrix.shape)


# In[11]:


ISW_matrix_df = pd.DataFrame(ISW_matrix)
ISW_matrix_df[:5]


# In[12]:


reindex = ['A_1', 'B_1', 'C_1', 'D_1', 'E_1', 'F_1', 'G_1', 'H_1', 'I_1', 'J_1', 'K_1', 'L_1', 'M_1', 'N_1', 'O_1', 'P_1', 'Q_1', 'R_1', 'S_1', 'T_1', 'Z_1', 'A_2', 'B_2', 'C_2', 'D_2', 'E_2', 'F_2', 'G_2', 'H_2', 'I_2', 'J_2', 'K_2', 'L_2', 'M_2', 'N_2', 'O_2', 'P_2', 'Q_2', 'R_2', 'S_2', 'T_2', 'Z_2', 'A_3', 'B_3', 'C_3', 'D_3', 'E_3', 'F_3', 'G_3', 'H_3', 'I_3', 'J_3', 'K_3', 'L_3', 'M_3', 'N_3', 'O_3', 'P_3', 'Q_3', 'R_3', 'S_3', 'T_3', 'Z_3', 'A_4', 'B_4', 'C_4', 'D_4', 'E_4', 'F_4', 'G_4', 'H_4', 'I_4', 'J_4', 'K_4', 'L_4', 'M_4', 'N_4', 'O_4', 'P_4', 'Q_4', 'R_4', 'S_4', 'T_4', 'Z_4', 'A_5', 'B_5', 'C_5', 'D_5', 'E_5', 'F_5', 'G_5', 'H_5', 'I_5', 'J_5', 'K_5', 'L_5', 'M_5', 'N_5', 'O_5', 'P_5', 'Q_5', 'R_5', 'S_5', 'T_5', 'Z_5']
print(len(reindex))

recolumns = ['a_1_2', 'a_3', 'a_4', 'a_5', 'a_6', 'a_7', 'a_8', 'a_9', 'a_10', 'a_11', 'a_12', 'a_13', 'a_14', 'a_15', 'a_16', 'a_17', 'a_18']
print(len(recolumns))


# In[13]:


ISW_matrix_df.index = reindex
ISW_matrix_df.columns = recolumns

ISW_matrix_df[:5]


# In[14]:


k = 0
dc_2 = dc
dc_2['EA'] = None
for i in range(5):
    for j in alphabet_all:
        k = k+1
        start = time.perf_counter() 
        dc_T = dc[((dc['hydm'] == j) & (dc['scale'] == i+1))]
        # 选择需要的17个特征
        dc_T_feature = dc_T.loc[:, 'X1_2':'X18']
        col = j + '_' + str(i+1)
        # 显示进度
        print(k, '/105:  ',  end='')
        EA_T = dc_T_feature.values * ISW_matrix_df.loc[col].values
        EA_T = EA_T.sum(axis=1) * dc_T['jyzt'].values
        dc_T_feature['EA'] = EA_T
        dc_T_feature = dc_T_feature['EA']
        dc_T_feature = pd.DataFrame({'nbxh':dc_T_feature.index, 'EA_fill':dc_T_feature.values})
        dc_T_feature.set_index('nbxh', inplace=True)
        # 使用join和fillna方法
        dc_2 = dc_2.join(dc_T_feature)
        dc_2["EA"].fillna(dc_2["EA_fill"], inplace=True)
        dc_2.drop(['EA_fill'], axis=1, inplace=True)
        end = time.perf_counter()
        print('Running time: %.4f Seconds' % (end - start))


# In[15]:


temp_EA75 = dc_2['EA'].describe()['25%']
temp_EA75


# In[16]:


dc = dc_2


# ## 添加临时列 

# In[17]:


dc['EA_temp'] = None
dc.loc[dc['EA'] >= temp_EA75, 'EA_temp'] = 1
dc.loc[dc['EA'] < temp_EA75, 'EA_temp'] = 0
dc.info(null_counts = True)


# In[18]:


dc[:5]


# ## 计算整体活跃度 

# In[19]:


EA_all = dc['EA_temp'].value_counts()[1] / (dc['EA_temp'].value_counts()[1] + dc['EA_temp'].value_counts()[0])
EA_all


# In[20]:


with open('.\\'+ time_str + '\整体活跃度.txt', 'w') as f:
    f.write(str(EA_all))  


# ## groupby

# In[21]:


industry_grouped = dc.groupby('hydm')['EA_temp']
scale_grouped = dc.groupby('scale')['EA_temp']
city_grouped = dc.groupby('city')['EA_temp']
three_grouped = dc.groupby('three')['EA_temp']
economic_grouped = dc.groupby('jjhklb')['EA_temp']
time_grouped = dc.groupby('time_scale')['EA_temp']
foreign_grouped = dc.groupby('foreign')['EA_temp']


# ## 定义分类活跃度函数

# In[22]:


def class_EA(grouped):
    name_value = grouped.value_counts()
    name_all = [] # 0,1两类，会有重复的name
    for i in list(name_value.index):
        name_all.append(i[0])
    name_clean = []
    # 列表推导式，去除列表重复值
    [name_clean.append(i) for i in name_all if not i in name_clean]
    df_name =  pd.DataFrame(index=name_clean, columns=['proportion', 'sum'])
    
    for n in name_clean:
        temp_sum = 0
        for j in list(name_value[n]):
            # 每个类别的value一般都有1， 0两类
            temp_sum = temp_sum + j
        temp_num = name_value[n, 1] / temp_sum
        df_name.loc[n, 'proportion'] = temp_num
        df_name.loc[n, 'sum'] = temp_sum
    return df_name


# ## 按行业

# In[23]:


df_industry = class_EA(industry_grouped)
df_industry


# ### 保存

# In[24]:


df_industry.to_excel('./' + time_str + '/行业活跃度.xlsx')


# ## 按规模

# In[25]:


df_scale = class_EA(scale_grouped)
df_scale


# ### 保存

# In[26]:


df_scale.to_excel('./' + time_str + '/规模活跃度.xlsx')


# ## 按城市

# In[27]:


df_city = class_EA(city_grouped)
df_city


# ### 保存

# In[28]:


df_city.to_excel('./' + time_str + '/地区活跃度.xlsx')


# ## 按三次产业

# In[29]:


df_three = class_EA(three_grouped)
df_three


# ### 保存

# In[30]:


df_three.to_excel('./' + time_str + '/三次产业活跃度.xlsx')


# ## 按经济户口类别

# In[31]:


df_economic = class_EA(economic_grouped)
df_economic


# ### 保存

# In[32]:


df_economic.to_excel('./' + time_str + '/经济户口活跃度.xlsx')


# ## 按企业存续时间

# In[33]:


df_time = class_EA(time_grouped)
df_time


# ### 保存

# In[34]:


df_time.to_excel('./' + time_str + '/企业存续时间活跃度.xlsx')


# ## 按是否外商投资

# In[35]:


df_foreign = class_EA(foreign_grouped)
df_foreign


# ### 保存

# In[36]:


df_foreign.to_excel('./' + time_str + '/是否外商投资活跃度.xlsx')


# ## 三次产业的分行业占比

# In[37]:


first = dc[dc['three'] == 1]['hydm'].value_counts()
second = dc[dc['three'] == 2]['hydm'].value_counts()
third = dc[dc['three'] == 3]['hydm'].value_counts()


# In[38]:


def industry_num(value):
    df_name = pd.DataFrame(index=value.index, columns=['num', 'proportion'])
    df_name['num'] = value
    df_name['proportion'] = value / value.sum()
    return df_name


# In[39]:


df_first =  industry_num(first)
df_second = industry_num(second)
df_third = industry_num(third)


# ### 保存

# In[40]:


df_first.to_excel('./' + time_str + '/分行业：一产行业数量及占比.xlsx')
df_second.to_excel('./' + time_str + '/分行业：二产行业数量及占比.xlsx')
df_third.to_excel('./' + time_str + '/分行业：三产行业数量及占比.xlsx')

