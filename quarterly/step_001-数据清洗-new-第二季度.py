#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#读取主体登记信息" data-toc-modified-id="读取主体登记信息-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>读取主体登记信息</a></span><ul class="toc-item"><li><span><a href="#读取" data-toc-modified-id="读取-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>读取</a></span><ul class="toc-item"><li><span><a href="#读取主体登记" data-toc-modified-id="读取主体登记-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>读取主体登记</a></span></li><li><span><a href="#查看当月成立的企业数量" data-toc-modified-id="查看当月成立的企业数量-1.1.2"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>查看当月成立的企业数量</a></span></li><li><span><a href="#提取本月注吊销及迁出数据" data-toc-modified-id="提取本月注吊销及迁出数据-1.1.3"><span class="toc-item-num">1.1.3&nbsp;&nbsp;</span>提取本月注吊销及迁出数据</a></span></li><li><span><a href="#删除注吊销及迁出数据" data-toc-modified-id="删除注吊销及迁出数据-1.1.4"><span class="toc-item-num">1.1.4&nbsp;&nbsp;</span>删除注吊销及迁出数据</a></span></li></ul></li><li><span><a href="#提取需要特征" data-toc-modified-id="提取需要特征-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>提取需要特征</a></span><ul class="toc-item"><li><span><a href="#提取主体登记表" data-toc-modified-id="提取主体登记表-1.2.1"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>提取主体登记表</a></span></li><li><span><a href="#提取注吊销表" data-toc-modified-id="提取注吊销表-1.2.2"><span class="toc-item-num">1.2.2&nbsp;&nbsp;</span>提取注吊销表</a></span></li></ul></li><li><span><a href="#更改经营状态" data-toc-modified-id="更改经营状态-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>更改经营状态</a></span></li><li><span><a href="#合并两表" data-toc-modified-id="合并两表-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>合并两表</a></span></li><li><span><a href="#更改列名" data-toc-modified-id="更改列名-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>更改列名</a></span></li><li><span><a href="#缺失值填补" data-toc-modified-id="缺失值填补-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>缺失值填补</a></span></li><li><span><a href="#类型转换" data-toc-modified-id="类型转换-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>类型转换</a></span></li><li><span><a href="#行业代码只提取第一个" data-toc-modified-id="行业代码只提取第一个-1.8"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>行业代码只提取第一个</a></span></li><li><span><a href="#设置nbxh为索引" data-toc-modified-id="设置nbxh为索引-1.9"><span class="toc-item-num">1.9&nbsp;&nbsp;</span>设置nbxh为索引</a></span></li></ul></li><li><span><a href="#分类" data-toc-modified-id="分类-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>分类</a></span><ul class="toc-item"><li><span><a href="#划分企业年限" data-toc-modified-id="划分企业年限-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>划分企业年限</a></span></li><li><span><a href="#地区分类" data-toc-modified-id="地区分类-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>地区分类</a></span></li><li><span><a href="#三次产业分类" data-toc-modified-id="三次产业分类-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>三次产业分类</a></span></li><li><span><a href="#规模分类" data-toc-modified-id="规模分类-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>规模分类</a></span></li><li><span><a href="#是否为外商投资" data-toc-modified-id="是否为外商投资-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>是否为外商投资</a></span></li></ul></li><li><span><a href="#添加特征" data-toc-modified-id="添加特征-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>添加特征</a></span><ul class="toc-item"><li><span><a href="#添加特征X1_2、X3、X4" data-toc-modified-id="添加特征X1_2、X3、X4-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>添加特征X1_2、X3、X4</a></span></li><li><span><a href="#将固定企业类型的公积金赋值为0" data-toc-modified-id="将固定企业类型的公积金赋值为0-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>将固定企业类型的公积金赋值为0</a></span></li><li><span><a href="#添加特征X5、X6、X12、X13、X15（来自企业变更表）" data-toc-modified-id="添加特征X5、X6、X12、X13、X15（来自企业变更表）-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>添加特征X5、X6、X12、X13、X15（来自企业变更表）</a></span><ul class="toc-item"><li><span><a href="#读取企业变更表" data-toc-modified-id="读取企业变更表-3.3.1"><span class="toc-item-num">3.3.1&nbsp;&nbsp;</span>读取企业变更表</a></span></li><li><span><a href="#提取特征X5" data-toc-modified-id="提取特征X5-3.3.2"><span class="toc-item-num">3.3.2&nbsp;&nbsp;</span>提取特征X5</a></span><ul class="toc-item"><li><span><a href="#nums为series,将其变为dataframes" data-toc-modified-id="nums为series,将其变为dataframes-3.3.2.1"><span class="toc-item-num">3.3.2.1&nbsp;&nbsp;</span>nums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.3.2.2"><span class="toc-item-num">3.3.2.2&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#提取特征X6" data-toc-modified-id="提取特征X6-3.3.3"><span class="toc-item-num">3.3.3&nbsp;&nbsp;</span>提取特征X6</a></span><ul class="toc-item"><li><span><a href="#统计每个nbxh的每个变更事项出现次数" data-toc-modified-id="统计每个nbxh的每个变更事项出现次数-3.3.3.1"><span class="toc-item-num">3.3.3.1&nbsp;&nbsp;</span>统计每个nbxh的每个变更事项出现次数</a></span></li><li><span><a href="#nums为series,将其变为dataframes" data-toc-modified-id="nums为series,将其变为dataframes-3.3.3.2"><span class="toc-item-num">3.3.3.2&nbsp;&nbsp;</span>nums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.3.3.3"><span class="toc-item-num">3.3.3.3&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#X12、X13（保留变更事项与投资资本相关列）" data-toc-modified-id="X12、X13（保留变更事项与投资资本相关列）-3.3.4"><span class="toc-item-num">3.3.4&nbsp;&nbsp;</span>X12、X13（保留变更事项与投资资本相关列）</a></span></li><li><span><a href="#提取特征X12" data-toc-modified-id="提取特征X12-3.3.5"><span class="toc-item-num">3.3.5&nbsp;&nbsp;</span>提取特征X12</a></span><ul class="toc-item"><li><span><a href="#统计每个nbxh的每个变更事项出现次数" data-toc-modified-id="统计每个nbxh的每个变更事项出现次数-3.3.5.1"><span class="toc-item-num">3.3.5.1&nbsp;&nbsp;</span>统计每个nbxh的每个变更事项出现次数</a></span></li><li><span><a href="#nums为series,将其变为dataframes" data-toc-modified-id="nums为series,将其变为dataframes-3.3.5.2"><span class="toc-item-num">3.3.5.2&nbsp;&nbsp;</span>nums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.3.5.3"><span class="toc-item-num">3.3.5.3&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#提取特征X13" data-toc-modified-id="提取特征X13-3.3.6"><span class="toc-item-num">3.3.6&nbsp;&nbsp;</span>提取特征X13</a></span><ul class="toc-item"><li><span><a href="#nums为series,将其变为dataframes" data-toc-modified-id="nums为series,将其变为dataframes-3.3.6.1"><span class="toc-item-num">3.3.6.1&nbsp;&nbsp;</span>nums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.3.6.2"><span class="toc-item-num">3.3.6.2&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#提取特征X15（本月没有）" data-toc-modified-id="提取特征X15（本月没有）-3.3.7"><span class="toc-item-num">3.3.7&nbsp;&nbsp;</span>提取特征X15（本月没有）</a></span><ul class="toc-item"><li><span><a href="#将X15列赋值为0" data-toc-modified-id="将X15列赋值为0-3.3.7.1"><span class="toc-item-num">3.3.7.1&nbsp;&nbsp;</span>将X15列赋值为0</a></span></li></ul></li></ul></li><li><span><a href="#添加特征X7(分支机构开设数量，来自分支机构表)" data-toc-modified-id="添加特征X7(分支机构开设数量，来自分支机构表)-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>添加特征X7(分支机构开设数量，来自分支机构表)</a></span><ul class="toc-item"><li><span><a href="#读取文件" data-toc-modified-id="读取文件-3.4.1"><span class="toc-item-num">3.4.1&nbsp;&nbsp;</span>读取文件</a></span></li><li><span><a href="#fzjg_nums为series,将其变为dataframes" data-toc-modified-id="fzjg_nums为series,将其变为dataframes-3.4.2"><span class="toc-item-num">3.4.2&nbsp;&nbsp;</span>fzjg_nums为series,将其变为dataframes</a></span></li><li><span><a href="#找到对应的nbxh" data-toc-modified-id="找到对应的nbxh-3.4.3"><span class="toc-item-num">3.4.3&nbsp;&nbsp;</span>找到对应的nbxh</a></span></li><li><span><a href="#删除空值" data-toc-modified-id="删除空值-3.4.4"><span class="toc-item-num">3.4.4&nbsp;&nbsp;</span>删除空值</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.4.5"><span class="toc-item-num">3.4.5&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#添加特征X10、-X11（来自企业关系人表）" data-toc-modified-id="添加特征X10、-X11（来自企业关系人表）-3.5"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>添加特征X10、 X11（来自企业关系人表）</a></span><ul class="toc-item"><li><span><a href="#提取特征X10" data-toc-modified-id="提取特征X10-3.5.1"><span class="toc-item-num">3.5.1&nbsp;&nbsp;</span>提取特征X10</a></span><ul class="toc-item"><li><span><a href="#nums为series,将其变为dataframes" data-toc-modified-id="nums为series,将其变为dataframes-3.5.1.1"><span class="toc-item-num">3.5.1.1&nbsp;&nbsp;</span>nums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.5.1.2"><span class="toc-item-num">3.5.1.2&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#提取特征X11" data-toc-modified-id="提取特征X11-3.5.2"><span class="toc-item-num">3.5.2&nbsp;&nbsp;</span>提取特征X11</a></span><ul class="toc-item"><li><span><a href="#sums为series,将其变为dataframes" data-toc-modified-id="sums为series,将其变为dataframes-3.5.2.1"><span class="toc-item-num">3.5.2.1&nbsp;&nbsp;</span>sums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.5.2.2"><span class="toc-item-num">3.5.2.2&nbsp;&nbsp;</span>join</a></span></li></ul></li></ul></li><li><span><a href="#添加特征X14（迁移申请次数，来自迁移表）" data-toc-modified-id="添加特征X14（迁移申请次数，来自迁移表）-3.6"><span class="toc-item-num">3.6&nbsp;&nbsp;</span>添加特征X14（迁移申请次数，来自迁移表）</a></span><ul class="toc-item"><li><span><a href="#读取并查看" data-toc-modified-id="读取并查看-3.6.1"><span class="toc-item-num">3.6.1&nbsp;&nbsp;</span>读取并查看</a></span></li><li><span><a href="#sums为series,将其变为dataframes" data-toc-modified-id="sums为series,将其变为dataframes-3.6.2"><span class="toc-item-num">3.6.2&nbsp;&nbsp;</span>sums为series,将其变为dataframes</a></span></li><li><span><a href="#join" data-toc-modified-id="join-3.6.3"><span class="toc-item-num">3.6.3&nbsp;&nbsp;</span>join</a></span></li></ul></li><li><span><a href="#添加特征X8、X9、X16、X17、X18" data-toc-modified-id="添加特征X8、X9、X16、X17、X18-3.7"><span class="toc-item-num">3.7&nbsp;&nbsp;</span>添加特征X8、X9、X16、X17、X18</a></span></li></ul></li><li><span><a href="#调整顺序" data-toc-modified-id="调整顺序-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>调整顺序</a></span></li><li><span><a href="#去除重复值" data-toc-modified-id="去除重复值-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>去除重复值</a></span><ul class="toc-item"><li><span><a href="#重设索引" data-toc-modified-id="重设索引-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>重设索引</a></span></li><li><span><a href="#统计重复" data-toc-modified-id="统计重复-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>统计重复</a></span></li><li><span><a href="#删除重复" data-toc-modified-id="删除重复-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>删除重复</a></span></li></ul></li><li><span><a href="#保存" data-toc-modified-id="保存-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>保存</a></span></li></ul></div>

# In[1]:


import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm
import gc
warnings.filterwarnings("ignore")


# # 读取主体登记信息

# ## 读取

# ### 读取主体登记

# In[2]:


file = pd.read_csv('./三月份活跃度涉及表/主体登记20240326/exportsql.20240326095102.gbk.csv',encoding='gb18030')
print(file.info(null_counts = True))
file[:2]


# In[3]:


file['year-month'] = file['hzrq(D)'].str[:7]
print(file['year-month'].value_counts())


# In[4]:


file['new'] = file['clrq(D)'].str[:7]
print(file['new'].value_counts())


# ### 查看当月成立的企业数量

# In[5]:


quarter = ['2024-01', '2024-02', '2024-03']
new_company = pd.DataFrame()
for month in quarter:
    new_company = new_company.append(file[file['new'] == month])

new_company.info(null_counts = True)


# ### 提取本月注吊销及迁出数据

# In[6]:


# 注销（07）、吊销（11）、迁入（09）、迁出（13）
revoke = pd.DataFrame()
for month in quarter:
    revoke = revoke.append(file[((file['year-month'] == month) & (file['tslx(C|2)'] == 7)) | ((file['year-month'] == month) & (file['tslx(C|2)'] == 11)) | ((file['year-month'] == month) & (file['tslx(C|2)'] == 13))])
print(revoke.info(null_counts = True))
print('注销：', len(revoke[revoke['tslx(C|2)'] == 7]))
print('吊销：', len(revoke[revoke['tslx(C|2)'] == 11]))
print('迁出：', len(revoke[revoke['tslx(C|2)'] == 13]))


# ### 删除注吊销及迁出数据

# In[7]:


# 删除所有注吊销数据
file.drop(file[file['tslx(C|2)'] == 7].index, inplace=True)
file.drop(file[file['tslx(C|2)'] == 11].index, inplace=True)
file.drop(file[file['tslx(C|2)'] == 13].index, inplace=True)
file.info(null_counts = True)


# ## 提取需要特征

# 提取
# > `jjhklb`经济户口类别：用于经济户口**分类**     
#     `nbxh`内部序号：索引    
#     `hydm`行业代码：用于行业**分类**    
#     `djjg`登记机关：用于地区**分类**    
#     `zczb`注册资本：用于规模**分类**    
#     `jyzt`经营状态：0， 1    
#     `clrq`成立日期：用于存续时间**分类**   
#     `qylx(C|6)` 用于决定哪些企业公积金为0

# ### 提取主体登记表

# In[8]:


new_file = file[['jjhklb(C|2)', '#nbxh(C|50)', 'hydm(C|8)', 'djjg(C|20)', 'zczb(N|21|6)', 'jyzt(C|4)', 'clrq(D)', 'qylx(C|6)', 'tslx(C|2)', 'new']]
new_file.info(null_counts = True)


# ### 提取注吊销表

# In[9]:


new_revoke = revoke[['jjhklb(C|2)', '#nbxh(C|50)', 'hydm(C|8)', 'djjg(C|20)', 'zczb(N|21|6)', 'jyzt(C|4)', 'clrq(D)', 'qylx(C|6)', 'tslx(C|2)', 'new']]
new_revoke.info(null_counts = True)


# ## 更改经营状态

# In[10]:


new_file[:2]


# In[11]:


# 主体登记表的经营状态填补为1
new_file['jyzt(C|4)'].fillna(value=1.0, inplace=True)

# 注吊销表的经营状态为0
new_revoke['jyzt(C|4)'] = 0.0

# jyzt大于1的全部调整为1
new_file['jyzt(C|4)'] = new_file['jyzt(C|4)'].astype(np.float)
new_file.loc[new_file['jyzt(C|4)'] > 0, 'jyzt(C|4)'] = 1
new_file.loc[new_file['jyzt(C|4)'] == 0, 'jyzt(C|4)'] = 0
new_file['jyzt(C|4)'] = new_file['jyzt(C|4)'].astype(np.int64)
print(new_file['jyzt(C|4)'].value_counts())
print(new_revoke['jyzt(C|4)'].value_counts())


# In[12]:


new_file[:2]


# In[13]:


new_revoke[:2]


# ## 合并两表

# In[14]:


new_file = pd.concat([new_file, new_revoke])
print(new_file.info(null_counts = True))


# ## 更改列名

# In[15]:


new_file.rename(
    columns={'jjhklb(C|2)': 'jjhklb', '#nbxh(C|50)': 'nbxh', 'hydm(C|8)':'hydm', 'djjg(C|20)':'djjg', 
             'zczb(N|21|6)':'zczb', 'jyzt(C|4)':'jyzt', 'clrq(D)':'clrq', 'qylx(C|6)':'qylx', 'tslx(C|2)':'tslx'}, 
    inplace=True)
print(new_file.info(null_counts = True))
new_file[:2]


# ## 缺失值填补

# `jjhklb`填补为众数

# In[16]:


new_file['jjhklb'].fillna(new_file['jjhklb'].mode()[0], inplace=True)


# `hydm`填补为众数

# In[17]:


new_file['hydm'].fillna(new_file['hydm'].mode()[0], inplace=True)


# `djjg`填补为临近值

# In[18]:


# 用前值填补
new_file['djjg'].fillna(method = 'ffill', inplace = True)


# `zczb`填补为众数

# In[19]:


new_file['zczb'].fillna(new_file['zczb'].mode()[0], inplace=True)


# `jyzt`填补为***0***

# In[20]:


new_file['jyzt'].fillna(value = '0', inplace=True)


# `clrq`填补为众数

# In[21]:


new_file['clrq'].fillna(new_file['clrq'].mode()[0], inplace=True)


# In[22]:


new_file.info(null_counts = True)


# ## 类型转换

# 登记机关转换为int后再转为str

# In[23]:


new_file['djjg'] = new_file['djjg'].astype(np.int64)


# In[24]:


new_file.info(null_counts = True)


# ## 行业代码只提取第一个

# In[25]:


new_file['hydm'] = new_file['hydm'].str[0]
new_file[:2]


# In[26]:


# new_file['nbxh'] = new_file['nbxh'].astype(np.int64)


# ## 设置nbxh为索引

# In[27]:


new_file.set_index('nbxh', inplace=True)
new_file[:2]


# # 分类

# In[28]:


new_file.info(verbose = True, null_counts = True)


# ## 划分企业年限

# 总会有些特殊情况

# In[29]:


new_file['time'] = 2024 - new_file['clrq'].str[:4].astype(np.int64)


# ```python
# new_file['time_scale'] = None
# new_file.loc[new_file['time'] <= 1, 'time_scale'] = '1'
# new_file.loc[((new_file['time'] > 1) & (new_file['time'] <= 2)), 'time_scale'] = '2'
# new_file.loc[((new_file['time'] > 2) & (new_file['time'] <= 3)), 'time_scale'] = '3'
# new_file.loc[((new_file['time'] > 3) & (new_file['time'] <= 4)), 'time_scale'] = '4'
# new_file.loc[((new_file['time'] > 4) & (new_file['time'] <= 5)), 'time_scale'] = '5'
# new_file.loc[((new_file['time'] > 5) & (new_file['time'] <= 6)), 'time_scale'] = '6'
# new_file.loc[((new_file['time'] > 6) & (new_file['time'] <= 7)), 'time_scale'] = '7'
# new_file.loc[((new_file['time'] > 7) & (new_file['time'] <= 8)), 'time_scale'] = '8'
# new_file.loc[((new_file['time'] > 8) & (new_file['time'] <= 9)), 'time_scale'] = '9'
# new_file.loc[((new_file['time'] > 9) & (new_file['time'] <= 10)), 'time_scale'] = '10'
# new_file.loc[new_file['time'] > 10, 'time_scale'] = '11'
# ```
# 采用新的划分
# > 1年以内/1-5年/5年以上/10年以上

# In[30]:


new_file['time_scale'] = None
new_file.loc[new_file['time'] <= 1, 'time_scale'] = '1'
new_file.loc[((new_file['time'] > 1) & (new_file['time'] <= 5)), 'time_scale'] = '2'
new_file.loc[((new_file['time'] > 5) & (new_file['time'] <= 10)), 'time_scale'] = '3'
new_file.loc[new_file['time'] > 10, 'time_scale'] = '4'


# In[31]:


new_file.drop(['clrq', 'time'], axis=1, inplace=True)


# In[32]:


new_file[:2]


# ## 地区分类

# In[33]:


new_file['city'] = None
new_file['djjg'] = new_file['djjg'].astype(str)
new_file.info()


# In[34]:


new_file.loc[(new_file['djjg'].str[:4] == '4201'), 'city'] = '武汉市'
new_file.loc[(new_file['djjg'].str[:4] == '4202'), 'city'] = '黄石市'
new_file.loc[(new_file['djjg'].str[:4] == '4203'), 'city'] = '十堰市'
new_file.loc[(new_file['djjg'].str[:4] == '4205'), 'city'] = '宜昌市'
new_file.loc[(new_file['djjg'].str[:4] == '4206'), 'city'] = '襄阳市'
new_file.loc[(new_file['djjg'].str[:4] == '4207'), 'city'] = '鄂州市'
new_file.loc[(new_file['djjg'].str[:4] == '4208'), 'city'] = '荆门市'
new_file.loc[(new_file['djjg'].str[:4] == '4209'), 'city'] = '孝感市'
new_file.loc[(new_file['djjg'].str[:4] == '4210'), 'city'] = '荆州市'
new_file.loc[(new_file['djjg'].str[:4] == '4211'), 'city'] = '黄冈市'

new_file.loc[(new_file['djjg'].str[:4] == '4212'), 'city'] = '咸宁市'
new_file.loc[(new_file['djjg'].str[:4] == '4223'), 'city'] = '咸宁市'

new_file.loc[(new_file['djjg'].str[:4] == '4213'), 'city'] = '随州市'
new_file.loc[(new_file['djjg'].str[:4] == '4228'), 'city'] = '恩施州'
new_file.loc[(new_file['djjg'].str[:6] == '429004'), 'city'] = '仙桃市'
new_file.loc[(new_file['djjg'].str[:6] == '429005'), 'city'] = '潜江市'
new_file.loc[(new_file['djjg'].str[:6] == '429006'), 'city'] = '天门市'
new_file.loc[(new_file['djjg'].str[:6] == '429021'), 'city'] = '神农架林区'

new_file.loc[(new_file['djjg'] == '429900'), 'city'] = '武汉市'


# In[35]:


new_file.info(null_counts = True)


# In[36]:


new_file.drop(['djjg'], axis=1, inplace=True)


# In[37]:


new_file.info(null_counts = True)


# ## 三次产业分类

# In[38]:


new_file['three'] = None
new_file.loc[new_file['hydm'] == 'A', 'three'] = '1'
second = ['B', 'C', 'D', 'E']
for i in second:
    new_file.loc[new_file['hydm'] == i, 'three'] = '2'
third = ['F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'Z']
for i in third:
    new_file.loc[new_file['hydm'] == i, 'three'] = '3'


# In[39]:


new_file.info(null_counts = True)


# ## 规模分类

# In[40]:


new_file['scale'] = None
new_file.loc[new_file['zczb'] <= 100, 'scale'] = '1'
new_file.loc[((new_file['zczb'] > 100) & (new_file['zczb'] <= 1_000)), 'scale'] = '2'
new_file.loc[((new_file['zczb'] > 1_000) & (new_file['zczb'] <= 10_000)), 'scale'] = '3'
new_file.loc[((new_file['zczb'] > 10_000) & (new_file['zczb'] <= 20_000)), 'scale'] = '4'
new_file.loc[new_file['zczb'] > 20_000, 'scale'] = '5'


# In[41]:


new_file.info(null_counts = True)


# In[42]:


new_file[:2]


# In[43]:


# new_file.drop(['zczb'], axis=1, inplace=True)
print(new_file.info(null_counts = True))
new_file[:2]


# ## 是否为外商投资

# In[44]:


foreign_investment = [1122, 1123, 1211, 2123, 2211, 5000, 5320, 1121, 5310, 1120, 
                      2221, 5180, 5260, 5820, 5840, 1221, 2120, 5400, 5800, 2121, 
                      2122, 5250]
new_file['foreign'] = None
for i in foreign_investment:
    new_file.loc[new_file['qylx'] == i, 'foreign'] = 1
new_file['foreign'].fillna(value=0, inplace=True)
print(new_file['foreign'].value_counts())
print(new_file.info(null_counts = True))
new_file[:2]


# # 添加特征

# ## 添加特征X1_2、X3、X4

# 这三个特征赋值为1

# In[45]:


new_file['X1_2'] = 1
new_file['X3'] = 1
new_file['X4'] = 1


# In[46]:


new_file.info(null_counts = True)


# ## 将固定企业类型的公积金赋值为0

# 让企业类型为1151 4540 2151的公积金那里给0

# In[47]:


new_file['X4'].value_counts()


# In[48]:


for i in tqdm([1151, 4540, 2125]):
    new_file.loc[new_file[(new_file['qylx'] == i)].index, 'X4'] = 0
new_file['X4'].value_counts()


# In[49]:


new_file['X4'].value_counts()[1] / (new_file['X4'].value_counts()[1] + new_file['X4'].value_counts()[0])


# In[50]:


new_file[:2]


# ## 添加特征X5、X6、X12、X13、X15（来自企业变更表）

# - X5：企业变更备案次数
# - X6：企业变更备案类别数 
# - X12：投资资本类变更类型数 
# - X13：投资资本类变更次数
# - X15：分支机构注吊销数量 

# ### 读取企业变更表

# In[51]:


qybg_file = pd.read_csv('./第二季度活跃度涉及表/企业变更.csv')
print(qybg_file.info(null_counts = True))
qybg_file[:2]


# ### 提取特征X5

# In[52]:


nums = qybg_file['#NBXH(C|36)'].value_counts()
nums


# #### nums为series,将其变为dataframes

# In[53]:


dict_nums = {'nbxh':nums.index, 'X5':nums.values}
df_nums = pd.DataFrame(dict_nums)
print(df_nums[:2])
df_nums.set_index('nbxh', inplace=True)
print(df_nums[:2])
print(df_nums.info(null_counts = True))


# #### join

# In[54]:


new_file = new_file.join(df_nums)
new_file.info(null_counts = True)


# In[55]:


# 缺失值填补
new_file['X5'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ### 提取特征X6

# In[56]:


qybg_file.drop(['CQRQ(P)'], axis=1, inplace=True)
qybg_grouped = qybg_file.groupby('#NBXH(C|36)')
qybg_grouped.size()


# #### 统计每个nbxh的每个变更事项出现次数

# In[57]:


cate = qybg_grouped['BGSX(C|64)'].value_counts()
list_cate = list(cate.index)
print(len(list_cate))
res_cate = [list(ele) for ele in list_cate]
res_cate[:5]


# In[58]:


indexs = [i[0] for i in res_cate] 
print(indexs[:5])
df_indexs = pd.DataFrame(indexs)
df_indexs[:5]


# In[59]:


nums = df_indexs[0].value_counts()


# ####  nums为series,将其变为dataframes

# In[60]:


dict_nums = {'nbxh':nums.index, 'X6':nums.values}
df_nums = pd.DataFrame(dict_nums)
print(df_nums[:2])
df_nums.set_index('nbxh', inplace=True)
print(df_nums[:2])
df_nums.info(null_counts = True)


# #### join

# In[61]:


new_file = new_file.join(df_nums)
new_file.info(null_counts = True)


# In[62]:


# 缺失值填补
new_file['X6'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ### X12、X13（保留变更事项与投资资本相关列）

#   也就是保存bgsx(C|10) ==120, 170, 700, 134, 118, 155, 117, 127, 136, 154, 914, 131, 923的列

# In[63]:


bgsx_M = [120, 170, 700, 134, 118, 155, 117, 127, 136, 154, 914, 131, 923]
for i in bgsx_M:
    if i == 120:
        qybg_file_M = qybg_file[qybg_file['BGSX(C|64)'] == i]
    else:
        qybg_file_M = pd.concat([qybg_file_M, qybg_file[qybg_file['BGSX(C|64)'] == i]])
        
print(qybg_file_M[:5])
qybg_file_M.info(null_counts = True)


# ### 提取特征X12

# In[64]:


qybg_grouped = qybg_file_M.groupby('#NBXH(C|36)')
qybg_grouped.size()


# #### 统计每个nbxh的每个变更事项出现次数

# In[65]:


cate = qybg_grouped['BGSX(C|64)'].value_counts()
# 层次化索引cate.index变列表
list_cate = list(cate.index)
print(len(list_cate))
res_cate = [list(ele) for ele in list_cate]
res_cate[:5]


# 现在获取nbxh的重复次数，就是该nbxh变更事项的类别数

# In[66]:


indexs = [i[0] for i in res_cate] 
print(indexs[:5])
df_indexs = pd.DataFrame(indexs)
df_indexs[:5]


# In[67]:


nums = df_indexs[0].value_counts()
nums[:5]


# #### nums为series,将其变为dataframes

# In[68]:


dict_nums = {'nbxh':nums.index, 'X12':nums.values}
df_nums = pd.DataFrame(dict_nums)
df_nums.set_index('nbxh', inplace=True)
print(df_nums[:2])
df_nums.info(null_counts = True)


# ####  join

# In[69]:


new_file = new_file.join(df_nums)
new_file.info(null_counts = True)


# In[70]:


# 缺失值填补
new_file['X12'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ### 提取特征X13

# In[71]:


nums = qybg_file_M['#NBXH(C|36)'].value_counts()
nums[:5]


# #### nums为series,将其变为dataframes

# In[72]:


dict_nums = {'nbxh':nums.index, 'X13':nums.values}
df_nums = pd.DataFrame(dict_nums)
print(df_nums[:2])
df_nums.set_index('nbxh', inplace=True)
print(df_nums[:2])
print(df_nums.info(null_counts = True))


# #### join

# In[73]:


new_file = new_file.join(df_nums)
new_file.info(null_counts = True)


# In[74]:


# 缺失值填补
new_file['X13'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ### 提取特征X15（本月没有）

# `企业变更表`中`bgsx(C|10)`变更事项`165`为撤销分支机构，可提取`X15`

# In[75]:


qybg_file[qybg_file['BGSX(C|64)'] == 165]


# #### 将X15列赋值为0

# In[76]:


new_file['X15'] = 0
new_file.info(null_counts = True)


# ## 添加特征X7(分支机构开设数量，来自分支机构表)

# ### 读取文件

# In[77]:


fzjg_file = pd.read_csv('./第二季度活跃度涉及表/分支机构.csv')
print(fzjg_file.info(null_counts = True))
fzjg_file[:2]


# In[78]:


nums_fzjg = fzjg_file['ENTNAME(C|301)'].value_counts()
nums_fzjg[:5]


# ### fzjg_nums为series,将其变为dataframes

# In[79]:


dict_nums_fzjg = {'ENTNAME':nums_fzjg.index, 'X7':nums_fzjg.values}
df_nums_fzjg = pd.DataFrame(dict_nums_fzjg)
print(df_nums_fzjg[:5])
df_nums_fzjg.info(null_counts = True)


# ### 找到对应的nbxh

# In[80]:


print(df_nums_fzjg.info(null_counts = True))

df_nums_fzjg.set_index('ENTNAME', inplace=True)# 以企业名称为索引进行join操作
temp_name = file[['#nbxh(C|50)', 'qymc(C|300)']]# 提取内部序号和企业名称
temp_name.set_index('qymc(C|300)', inplace=True)# 企业名称为索引
df_nums_fzjg = df_nums_fzjg.join(temp_name)
print(df_nums_fzjg.info(null_counts = True))

df_nums_fzjg = df_nums_fzjg.reset_index()# 重设索引，且不替换掉企业名称
print(df_nums_fzjg.info(null_counts = True))

df_nums_fzjg.drop_duplicates(subset=['index'], keep='first', inplace=True)# 去除重复，join带来的重复，需要思考
print(df_nums_fzjg.info(null_counts = True))


# ### 删除空值

# In[81]:


df_nums_fzjg.dropna(inplace=True)
# df_nums_fzjg['#nbxh(C|50)'] = df_nums_fzjg['#nbxh(C|50)'].astype(np.int64)
df_nums_fzjg.set_index('#nbxh(C|50)', inplace=True)
df_nums_fzjg.drop(['index'], axis=1, inplace=True)
print(df_nums_fzjg.info(null_counts = True))
df_nums_fzjg[:5]


# ### join

# In[82]:


new_file = new_file.join(df_nums_fzjg)
new_file.info(null_counts = True)


# In[83]:


# 缺失值填补
new_file['X7'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ## 添加特征X10、 X11（来自企业关系人表）

# - X10 投资次数     
# - X11 投资总额 

# In[84]:


invest = pd.read_csv('./第二季度活跃度涉及表/企业关系人.csv')
invest.rename(columns = {'#tznbxh(C|250)':'nbxh', 'tze(N|18|6)':'tze'}, inplace=True)
invest.info(null_counts = True)
invest[:10]


# In[85]:


# 不显示科学计数法
pd.set_option('display.float_format', lambda x: '%.3f' % x)
invest = invest.dropna()
invest['nbxh'] = invest['nbxh'].astype(np.int64)
invest


# ### 提取特征X10

# In[86]:


nums = invest['nbxh'].value_counts()
nums


# #### nums为series,将其变为dataframes

# In[87]:


dict_nums = {'nbxh':nums.index, 'X10':nums.values}
df_nums = pd.DataFrame(dict_nums)
print(df_nums[:2])
df_nums.set_index('nbxh', inplace=True)
print(df_nums[:2])
print(df_nums.info(null_counts = True))


# #### join

# In[88]:


new_file = new_file.join(df_nums)
new_file.info(null_counts = True)


# In[89]:


# 缺失值填补
new_file['X10'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ### 提取特征X11

# In[90]:


sums = invest.groupby('nbxh')['tze'].agg('sum')
sums


# #### sums为series,将其变为dataframes

# In[91]:


dict_sums = {'nbxh':sums.index, 'X11':sums.values}
df_sums = pd.DataFrame(dict_sums)
print(df_sums[:2])
df_sums.set_index('nbxh', inplace=True)
print(df_sums[:2])
print(df_sums.info(null_counts = True))


# #### join

# In[92]:


new_file = new_file.join(df_sums)
new_file.info(null_counts = True)


# In[93]:


# 缺失值填补
new_file['X11'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ## 添加特征X14（迁移申请次数，来自迁移表）

# ### 读取并查看

# In[94]:


qycs_file = pd.read_csv('./第二季度活跃度涉及表/迁移.csv')
print(qycs_file.info(null_counts = True))
qycs_file[:3]


# `MARPRID(C|75)`为 主体标识，查看在file中是否存在相应的内部序号

# In[95]:


nbxh_list =   file['#nbxh(C|50)'].values
temp_sum = 0
for i in tqdm(qycs_file['MARPRID(C|75)']):
    if i in nbxh_list:
        temp_sum = temp_sum + 1
temp_sum


# 可以看出绝大多数企业还是可以在主体登记表中找到的

# In[96]:


nums = qycs_file['MARPRID(C|75)'].value_counts()
nums


# ### sums为series,将其变为dataframes

# In[97]:


dict_nums = {'nbxh':nums.index, 'X14':nums.values}
df_nums = pd.DataFrame(dict_nums)
print(df_nums[:2])
df_nums.set_index('nbxh', inplace=True)
print(df_nums[:2])
print(df_nums.info(null_counts = True))


# ### join

# In[98]:


new_file = new_file.join(df_nums)
new_file.info(null_counts = True)


# In[99]:


# 缺失值填补
new_file['X14'].fillna(value=0, inplace=True)
new_file.info(null_counts = True)


# ## 添加特征X8、X9、X16、X17、X18

# 这些特征无来源，都赋值为0

# In[100]:


new_file['X8'] = 0
new_file['X9'] = 0
new_file['X16'] = 0
new_file['X17'] = 0
new_file['X18'] = 0
new_file.info(null_counts = True)


# # 调整顺序

# In[101]:


col_num = new_file.shape[1]
new_file.insert(col_num-12, 'X7', new_file.pop('X7'))
new_file.insert(col_num-11, 'X8', new_file.pop('X8'))
new_file.insert(col_num-10, 'X9', new_file.pop('X9'))
new_file.insert(col_num-9, 'X10', new_file.pop('X10'))
new_file.insert(col_num-8, 'X11', new_file.pop('X11'))
new_file.insert(col_num-7, 'X12', new_file.pop('X12'))
new_file.insert(col_num-6, 'X13', new_file.pop('X13'))
new_file.insert(col_num-5, 'X14', new_file.pop('X14'))
new_file.insert(col_num-4, 'X15', new_file.pop('X15'))
new_file.insert(col_num-3, 'X16', new_file.pop('X16'))
new_file.insert(col_num-2, 'X17', new_file.pop('X17'))
new_file.insert(col_num-1, 'X18', new_file.pop('X18'))
new_file.info(null_counts = True)


# In[102]:


new_file[:10]


# # 去除重复值

# ## 重设索引

# In[103]:


del file
gc.collect()


# In[104]:


new_file = new_file.reset_index()
print(new_file.info(null_counts = True))
new_file[:2]


# ## 统计重复

# In[105]:


new_file.rename(
    columns={'index': 'nbxh' }, 
    inplace=True)
re_nums = new_file['nbxh'].value_counts()
re_nums


# ## 删除重复

# In[106]:


new_file.drop_duplicates(subset=['nbxh'], keep='first', inplace=True)
new_file.info(null_counts = True)


# # 保存

# In[107]:


path = './DataCleaning_quarterTwo_1.csv'
new_file.to_csv(path, index=False)

