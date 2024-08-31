#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import warnings

import pandas as pd

warnings.filterwarnings("ignore")


def process(quarter_source_data_files, result_data_dir, cache_dir, quarter):


    path_dc = os.path.join(cache_dir, 'DataCleaning_quarterTwo_1.csv')
    dc = pd.read_csv(path_dc, index_col=[0])
    print(dc.info(show_counts=True))
    dc[:2]

    # > 表中`jyzt`为1的是存量企业
    #
    # > 需要在代码一中加入
    #     - `tslx(C|2)`来标明注吊销迁入迁出数据
    #     >> 注销（07）、吊销（11）、迁入（09）、迁出（13）
    #     - `new`来标明新设企业
    #     >> *half = ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06']* 这些设置为`1`，其他的设置为`0`

    # In[5]:


    new_month = quarter
    for i in new_month:
        dc.loc[dc['new'] == i, 'new'] = 1

    dc.loc[dc['new'] != 1, 'new'] = 0
    print(dc['new'].value_counts())


    # # unit_df

    # In[6]:


    def series2df(series_name, col_name1, col_name2):
        df_temp = {col_name1: series_name.index, col_name2: series_name.values}
        df_temp = pd.DataFrame(df_temp)
        df_temp.set_index(col_name1, inplace=True)
        return df_temp


    # In[7]:


    def df_combine(df_name, series_name, col_name1, col_name2):
        df_temp = series2df(series_name, col_name1, col_name2)
        combine_result = pd.concat([df_name, df_temp], axis=1)
        return combine_result


    # # 不同行业下

    # ## 新设企业

    # In[8]:


    industry_new = dc[dc['new'] == 1].groupby(['hydm']).size()
    industry_temp = series2df(industry_new, 'hydm', '新设企业')
    industry_all = industry_temp
    industry_all

    # ## 存量企业
    # 存量企业包括了在这半年中注吊销和迁出的企业

    # In[9]:


    industry_live = dc.groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_live, 'hydm', '存量企业(包含期间内的注吊销&迁出)')
    industry_all

    # In[10]:


    industry_live = dc[dc['jyzt'] == 1].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_live, 'hydm', '存量企业(不包含期间内的注吊销&迁出)')
    industry_all

    # ## 注吊销企业

    # In[11]:


    industry_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_zdx, 'hydm', '注吊销企业')
    industry_all

    # ### 注销

    # In[12]:


    industry_zx = dc[dc['tslx'] == 7].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_zx, 'hydm', '注销企业')
    industry_all

    # ### 吊销

    # In[13]:


    industry_dx = dc[dc['tslx'] == 11].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_dx, 'hydm', '吊销企业')
    industry_all

    # ## 迁入迁出企业

    # In[14]:


    industry_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_qrc, 'hydm', '迁入迁出企业')
    industry_all

    # ### 迁入

    # In[15]:


    industry_qr = dc[dc['tslx'] == 9].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_qr, 'hydm', '迁入企业')
    industry_all

    # ### 迁出

    # In[16]:


    industry_qc = dc[dc['tslx'] == 13].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_qc, 'hydm', '迁出企业')
    industry_all

    # ## 保存

    # In[17]:


    industry_all.fillna(value=0).to_excel(os.path.join(result_data_dir, '不同行业下细分.xlsx'))

    # # 不同地区下细分

    # ## 新设企业

    # In[18]:


    city_new = dc[dc['new'] == 1].groupby(['city']).size()
    city_temp = series2df(city_new, 'city', '新设企业')
    city_all = city_temp
    city_all

    # ## 存量企业
    # 存量企业包括了在这半年中注吊销和迁出的企业

    # In[19]:


    city_live = dc.groupby(['city']).size()
    city_all = df_combine(city_all, city_live, 'city', '存量企业(包含此期间内的注吊销&迁出)')
    city_all

    # In[20]:


    city_live = dc[dc['jyzt'] == 1].groupby(['city']).size()
    city_all = df_combine(city_all, city_live, 'city', '存量企业(不包含此期间内的注吊销&迁出)')
    city_all

    # ## 注吊销企业

    # In[21]:


    city_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['city']).size()
    city_all = df_combine(city_all, city_zdx, 'city', '注吊销企业')
    city_all

    # ### 注销

    # In[22]:


    city_zx = dc[dc['tslx'] == 7].groupby(['city']).size()
    city_all = df_combine(city_all, city_zx, 'city', '注销企业')
    city_all

    # ### 吊销

    # In[23]:


    city_dx = dc[dc['tslx'] == 11].groupby(['city']).size()
    city_all = df_combine(city_all, city_dx, 'city', '吊销企业')
    city_all

    # ## 迁入迁出企业

    # In[24]:


    city_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['city']).size()
    city_all = df_combine(city_all, city_qrc, 'city', '迁入迁出企业')
    city_all

    # ### 迁入

    # In[25]:


    city_qr = dc[dc['tslx'] == 9].groupby(['city']).size()
    city_all = df_combine(city_all, city_qr, 'hydm', '迁入企业')
    city_all

    # ### 迁出

    # In[26]:


    city_qc = dc[dc['tslx'] == 13].groupby(['city']).size()
    city_all = df_combine(city_all, city_qc, 'hydm', '迁出企业')
    city_all

    # ## 保存

    # In[27]:


    city_all.fillna(value=0).to_excel(os.path.join(result_data_dir, '不同地区下细分.xlsx'))

    # # 不同产业下

    # ## 新设企业

    # In[28]:


    three_new = dc[dc['new'] == 1].groupby(['three']).size()
    three_temp = series2df(three_new, 'three', '新设企业')
    three_all = three_temp
    three_all

    # ## 存量企业
    # 存量企业包括了在这半年中注吊销和迁出的企业

    # In[29]:


    three_live = dc.groupby(['three']).size()
    three_all = df_combine(three_all, three_live, 'three', '存量企业(包含此期间内的注吊销&迁出)')
    three_all

    # In[30]:


    three_live = dc[dc['jyzt'] == 1].groupby(['three']).size()
    three_all = df_combine(three_all, three_live, 'three', '存量企业(不包含此期间内的注吊销&迁出)')
    three_all

    # ## 注吊销企业

    # In[31]:


    three_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['three']).size()
    three_all = df_combine(three_all, three_zdx, 'three', '注吊销企业')
    three_all

    # ### 注销

    # In[32]:


    three_zx = dc[dc['tslx'] == 7].groupby(['three']).size()
    three_all = df_combine(three_all, three_zx, 'three', '注销企业')
    three_all

    # ### 吊销

    # In[33]:


    three_dx = dc[dc['tslx'] == 11].groupby(['three']).size()
    three_all = df_combine(three_all, three_dx, 'three', '吊销企业')
    three_all

    # ## 迁入迁出企业

    # In[34]:


    three_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['three']).size()
    three_all = df_combine(three_all, three_qrc, 'three', '迁入迁出企业')
    three_all

    # ### 迁入

    # In[35]:


    three_qr = dc[dc['tslx'] == 9].groupby(['three']).size()
    three_all = df_combine(three_all, three_qr, 'hydm', '迁入企业')
    three_all

    # ### 迁出

    # In[36]:


    three_qc = dc[dc['tslx'] == 13].groupby(['three']).size()
    three_all = df_combine(three_all, three_qc, 'hydm', '迁出企业')
    three_all

    # ## 保存

    # In[37]:


    three_all.fillna(value=0).to_excel(os.path.join(result_data_dir, '不同产业下细分.xlsx'))

    # # 注册资金规模

    # ## 不同行业注册资金规模

    # In[38]:


    temp_sum = pd.DataFrame(dc.groupby(['hydm', 'scale'])['zczb'].sum())
    df_industry_scale_sum = temp_sum.sum(axis=0)
    industry_scale = dc.groupby(['hydm', 'scale']).size()
    df_industry_scale = pd.DataFrame(industry_scale)
    df_industry_scale.rename(columns={0: 'count'}, inplace=True)
    df_industry_scale = df_industry_scale.join(temp_sum)
    df_industry_scale

    # In[39]:


    df_industry_scale_sum

    # ### 保存

    # In[40]:


    write = pd.ExcelWriter(os.path.join(result_data_dir, '不同行业注册资金规模.xlsx'))
    df_industry_scale.fillna(value=0).to_excel(write, sheet_name='细分')
    df_industry_scale_sum.to_excel(write, sheet_name='求和')
    write.close()

    # ## 不同产业注册资金规模

    # In[41]:


    temp_sum = pd.DataFrame(dc.groupby(['three', 'scale'])['zczb'].sum())
    df_three_scale_sum = temp_sum.sum(axis=0)
    three_scale = dc.groupby(['three', 'scale']).size()
    df_three_scale = pd.DataFrame(three_scale)
    df_three_scale.rename(columns={0: 'count'}, inplace=True)
    df_three_scale = df_three_scale.join(temp_sum)
    df_three_scale

    # In[42]:


    df_three_scale_sum

    # ### 保存

    # In[43]:


    write = pd.ExcelWriter(os.path.join(result_data_dir, '不同产业注册资金规模.xlsx'))
    df_three_scale.fillna(value=0).to_excel(write, sheet_name='细分')
    df_three_scale_sum.to_excel(write, sheet_name='求和')
    write.close()

    # ## 不同地区注册资金规模

    # In[44]:


    temp_sum = pd.DataFrame(dc.groupby(['city', 'scale'])['zczb'].sum())
    df_city_scale_sum = temp_sum.sum(axis=0)
    city_scale = dc.groupby(['city', 'scale']).size()
    df_city_scale = pd.DataFrame(city_scale)
    df_city_scale.rename(columns={0: 'count'}, inplace=True)
    df_city_scale = df_city_scale.join(temp_sum)
    df_city_scale

    # In[45]:


    df_city_scale_sum

    # ### 保存

    # In[46]:


    write = pd.ExcelWriter(os.path.join(result_data_dir, '不同地区注册资金规模.xlsx'))
    df_city_scale.fillna(value=0).to_excel(write, sheet_name='细分')
    df_city_scale_sum.to_excel(write, sheet_name='求和')
    write.close()

    # # 各地区不同行业下市场主体数

    # ## 新设企业

    # In[47]:


    c_i_new = dc[dc['new'] == 1].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_new)
    c_i_temp.rename(columns={0: '新设企业'}, inplace=True)
    c_i_all = c_i_temp
    c_i_all

    # ## 存量企业
    # 存量企业包括了在这半年中注吊销和迁出的企业

    # In[48]:


    c_i_live = dc.groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_live)
    c_i_temp.rename(columns={0: '存量企业(包含此期间内的注吊销&迁出)'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # In[49]:


    c_i_live = dc[dc['jyzt'] == 0].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_live)
    c_i_temp.rename(columns={0: '存量企业(不包含此期间内的注吊销&迁出)'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ## 注吊销企业

    # In[50]:


    c_i_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_zdx)
    c_i_temp.rename(columns={0: '注吊销企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ### 注销企业

    # In[51]:


    c_i_zx = dc[dc['tslx'] == 7].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_zx)
    c_i_temp.rename(columns={0: '注销企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ### 吊销企业

    # In[52]:


    c_i_dx = dc[dc['tslx'] == 11].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_dx)
    c_i_temp.rename(columns={0: '吊销企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ## 迁入迁出企业

    # In[53]:


    c_i_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_qrc)
    c_i_temp.rename(columns={0: '迁入迁出企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ### 迁入企业

    # In[54]:


    c_i_qr = dc[dc['tslx'] == 9].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_qr)
    c_i_temp.rename(columns={0: '迁入企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ### 迁出企业

    # In[55]:


    c_i_qc = dc[dc['tslx'] == 13].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_qc)
    c_i_temp.rename(columns={0: '迁出企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    # ## 保存

    # In[56]:


    c_i_all.fillna(value=0).to_excel(os.path.join(result_data_dir, '各地区不同行业下市场主体数量.xlsx'))

