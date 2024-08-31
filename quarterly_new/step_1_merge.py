#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
import warnings

import pandas as pd

warnings.filterwarnings("ignore")


def process(quarter_source_data_files, result_data_dir, cache_dir):
    # # 读取企业变更

    quarter_first_month_data, quarter_second_month_data, quarter_third_month_data = quarter_source_data_files

    qybg_4 = pd.read_csv(quarter_first_month_data["变更情况表"], encoding='gb18030')
    qybg_5 = pd.read_csv(quarter_second_month_data["变更情况表"], encoding='gb18030')
    qybg_6 = pd.read_csv(quarter_third_month_data["变更情况表"], encoding='gb18030')

    print(qybg_4.info(show_counts=True))
    print(qybg_5.info(show_counts=True))
    print(qybg_6.info(show_counts=True))

    # ## 更改列名

    # In[3]:

    print(qybg_4.info(show_counts=True))
    print(qybg_5.info(show_counts=True))
    print(qybg_6.info(show_counts=True))

    # ## 合并

    # In[4]:

    qybg = pd.concat([qybg_4, qybg_5, qybg_6])
    print(qybg.info(show_counts=True))

    # ## 存储

    # In[5]:

    path_qybg = os.path.join(cache_dir, '企业变更.csv')
    qybg.to_csv(path_qybg, index=False)

    # # 读取分支机构

    # In[6]:

    fzjg_4 = pd.read_csv(quarter_first_month_data["分支机构表"], encoding='gb18030')
    fzjg_5 = pd.read_csv(quarter_second_month_data["分支机构表"], encoding='gb18030')

    print(fzjg_4.info(show_counts=True))
    print(fzjg_5.info(show_counts=True))
    # print(fzjg_6.info(null_counts = True))

    # ## 更改列名

    # In[8]:

    print(fzjg_4.info(show_counts=True))
    print(fzjg_5.info(show_counts=True))
    # print(fzjg_6.info(null_counts = True))

    # ## 合并

    # In[9]:

    fzjg = pd.concat([fzjg_4, fzjg_5])
    # fzjg = pd.concat([fzjg_1, fzjg_2, fzjg_3, fzjg_4, fzjg_5, fzjg_6])
    print(fzjg.info(show_counts=True))

    # ## 存储

    # In[10]:

    path_fzjg = os.path.join(cache_dir, '分支机构.csv')
    fzjg.to_csv(path_fzjg, index=False)

    # # 读取企业关系人表

    # In[11]:

    qygx_4 = pd.read_csv(quarter_first_month_data["企业关系人表"], encoding='gb18030')
    qygx_5 = pd.read_csv(quarter_second_month_data["企业关系人表"], encoding='gb18030')
    qygx_6 = pd.read_csv(quarter_third_month_data["企业关系人表"], encoding='gb18030')

    print(qygx_4.info(show_counts=True))
    print(qygx_5.info(show_counts=True))
    print(qygx_6.info(show_counts=True))

    # ## 更改列名

    # In[12]:

    print(qygx_4.info(show_counts=True))
    print(qygx_5.info(show_counts=True))
    print(qygx_6.info(show_counts=True))

    # ## 合并

    # In[13]:

    qygx = pd.concat([qygx_4, qygx_5, qygx_6])
    print(qygx.info(show_counts=True))
    qygx[:2]

    # ## 存储

    # In[14]:

    path_qygx = os.path.join(cache_dir, '企业关系人.csv')
    qygx.to_csv(path_qygx, index=False)

    # # 读取迁移表

    # In[15]:

    qyb_4 = pd.read_csv(quarter_first_month_data["迁移信息表"], encoding='gb18030')
    qyb_5 = pd.read_csv(quarter_second_month_data["迁移信息表"], encoding='gb18030')
    qyb_6 = pd.read_csv(quarter_third_month_data["迁移信息表"], encoding='gb18030')

    print(qyb_4.info(show_counts=True))
    print(qyb_5.info(show_counts=True))
    print(qyb_6.info(show_counts=True))

    # ## 更改列名

    # In[16]:

    print(qyb_4.info(show_counts=True))
    print(qyb_5.info(show_counts=True))
    print(qyb_6.info(show_counts=True))

    # ## 合并

    # In[17]:

    qyb = pd.concat([qyb_4, qyb_5, qyb_6])
    print(qyb.info(show_counts=True))

    # ## 存储

    # In[18]:

    path_qyb = os.path.join(cache_dir, '迁移.csv')
    qyb.to_csv(path_qyb, index=False)


if __name__ == '__main__':
    pass