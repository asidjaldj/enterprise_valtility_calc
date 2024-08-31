#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")


# # 读取企业变更

# In[2]:


# qybg_4 = pd.read_excel('./yi月份活跃度涉及表/F_BGQK企业变更.xlsx')
qybg_4 = pd.read_csv('./一月份活跃度涉及表/变更情况表20240126/exportsql.20240126101619.gbk.csv', encoding='gb18030')
# qybg_5 = pd.read_excel('./五月份活跃度涉及表/F_BGQK企业变更.xlsx')
qybg_5 = pd.read_csv('./二月份活跃度涉及表/变更情况表20240226/exportsql.20240226095428.gbk.csv', encoding='gb18030')
# qybg_6 = pd.read_excel('./六月份活跃度涉及表/F_BGQK企业变更.xlsx')
qybg_6 = pd.read_csv('./三月份活跃度涉及表/变更情况表20240326/exportsql.20240326100115.gbk.csv', encoding='gb18030')

print(qybg_4.info(null_counts = True))
print(qybg_5.info(null_counts = True))
print(qybg_6.info(null_counts = True))


# ## 更改列名

# In[3]:


print(qybg_4.info(null_counts = True))
print(qybg_5.info(null_counts = True))
print(qybg_6.info(null_counts = True))


# ## 合并

# In[4]:


qybg = pd.concat([qybg_4, qybg_5, qybg_6])
print(qybg.info(null_counts = True))
qybg[:2]


# ## 存储

# In[5]:


path_qybg = './第二季度活跃度涉及表/企业变更.csv'
qybg.to_csv(path_qybg, index=False)


# # 读取分支机构

# In[6]:


# fzjg_4 = pd.read_excel('./一月份活跃度涉及表/F_FZJG 分支机构表.xlsx')
fzjg_4 = pd.read_csv('./一月份活跃度涉及表/分支机构表20240126/exportsql.20240126101941.gbk.csv', encoding='gb18030')
# fzjg_5 = pd.read_excel('./五月份活跃度涉及表/F_FZJG 分支机构表.xlsx')
fzjg_5 = pd.read_csv('./二月份活跃度涉及表/分支机构表20240226/exportsql.20240226095836.gbk.csv', encoding='gb18030')
# fzjg_6 = pd.read_excel('./六月份活跃度涉及表/F_FZJG 分支机构表.xlsx')

print(fzjg_4.info(null_counts = True))
print(fzjg_5.info(null_counts = True))
# print(fzjg_6.info(null_counts = True))


# ## 更改列名

# In[8]:


print(fzjg_4.info(null_counts = True))
print(fzjg_5.info(null_counts = True))
# print(fzjg_6.info(null_counts = True))


# ## 合并

# In[9]:


fzjg = pd.concat([fzjg_4, fzjg_5])
# fzjg = pd.concat([fzjg_1, fzjg_2, fzjg_3, fzjg_4, fzjg_5, fzjg_6])
print(fzjg.info(null_counts = True))
fzjg[:2]


# ## 存储

# In[10]:


path_fzjg = './第二季度活跃度涉及表/分支机构.csv'
fzjg.to_csv(path_fzjg, index=False)


# # 读取企业关系人表

# In[11]:


# qygx_4 = pd.read_excel('./四月份活跃度涉及表/F_TZJYZRR企业关系人表.xlsx')
qygx_4 = pd.read_csv('./一月份活跃度涉及表/企业关系人表20240126/exportsql.20240126101312.gbk.csv', encoding='gb18030')
# qygx_5 = pd.read_excel('./五月份活跃度涉及表/F_TZJYZRR企业关系人表.xlsx')
qygx_5 = pd.read_csv('./二月份活跃度涉及表/企业关系人表20240226/exportsql.20240226095002.gbk.csv', encoding='gb18030')
# qygx_6 = pd.read_excel('./六月份活跃度涉及表/F_TZJYZRR企业关系人表.xlsx')
qygx_6 = pd.read_csv('./三月份活跃度涉及表/企业关系人表20240326/exportsql.20240326095939.gbk.csv', encoding='gb18030')

print(qygx_4.info(null_counts = True))
print(qygx_5.info(null_counts = True))
print(qygx_6.info(null_counts = True))


# ## 更改列名

# In[12]:


print(qygx_4.info(null_counts = True))
print(qygx_5.info(null_counts = True))
print(qygx_6.info(null_counts = True))


# ## 合并

# In[13]:


qygx = pd.concat([qygx_4, qygx_5, qygx_6])
print(qygx.info(null_counts = True))
qygx[:2]


# ## 存储

# In[14]:


path_qygx = './第二季度活跃度涉及表/企业关系人.csv'
qygx.to_csv(path_qygx, index=False)


# # 读取迁移表

# In[15]:


# qyb_4 = pd.read_excel('./四月份活跃度涉及表/ODS_pREG_PARENTENT 迁移表.xlsx')
qyb_4 = pd.read_csv('./一月份活跃度涉及表/迁移信息表20240126/exportsql.20240126101748.gbk.csv', encoding='gb18030')
# qyb_5 = pd.read_excel('./五月份活跃度涉及表/ODS_REG_PARENTENT 迁移表.xlsx')
qyb_5 = pd.read_csv('./二月份活跃度涉及表/迁移信息表20240226/exportsql.20240226095641.gbk.csv', encoding='gb18030')
# qyb_6 = pd.read_excel('./六月份活跃度涉及表/ODS_REG_PARENTENT 迁移表.xlsx')
qyb_6 = pd.read_csv('./三月份活跃度涉及表/迁移信息表20240326/exportsql.20240326100217.gbk.csv', encoding='gb18030')

print(qyb_4.info(null_counts = True))
print(qyb_5.info(null_counts = True))
print(qyb_6.info(null_counts = True))


# ## 更改列名

# In[16]:


print(qyb_4.info(null_counts = True))
print(qyb_5.info(null_counts = True))
print(qyb_6.info(null_counts = True))


# ## 合并

# In[17]:


qyb = pd.concat([qyb_4, qyb_5, qyb_6])
print(qyb.info(null_counts = True))
qyb[:2]


# ## 存储

# In[18]:


path_qyb = './第二季度活跃度涉及表/迁移.csv'
qyb.to_csv(path_qyb, index=False)

