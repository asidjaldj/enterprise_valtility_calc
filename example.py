import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm
import gc
from _datetime import datetime

warnings.filterwarnings("ignore")

import sys
import datetime
import time
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta


def s_1(ztdj_path, qybg_paths, fzjg_paths, qygx_paths, qyb_paths, start_month):
    file = pd.read_csv(ztdj_path, encoding='gb18030')

    #####################
    # 去掉注册资本为10位数以上的企业
    file.drop(file[file['zczb(N|21|6)'] > 1e9].index, inplace=True)
    # --------------------
    #####################

    file['year-month'] = file['hzrq(D)'].str[:7]
    file['new'] = file['clrq(D)'].str[:7]
    quarter = []
    for i in range(len(qybg_paths)):
        quarter.append((datetime.strptime(start_month, '%Y-%m') + relativedelta(months=i)).strftime("%Y-%m"))

    new_company = pd.DataFrame()
    for month in quarter:
        new_company = new_company._append(file[file['new'] == month])

    revoke = pd.DataFrame()
    for month in quarter:
        revoke = revoke._append(file[((file['year-month'] == month) & (file['tslx(C|2)'] == 7)) | (
                    (file['year-month'] == month) & (file['tslx(C|2)'] == 11)) | (
                                                (file['year-month'] == month) & (file['tslx(C|2)'] == 13))])

    # 删除所有注吊销数据
    file.drop(file[file['tslx(C|2)'] == 7].index, inplace=True)
    file.drop(file[file['tslx(C|2)'] == 11].index, inplace=True)
    file.drop(file[file['tslx(C|2)'] == 13].index, inplace=True)
    # file.info(show_counts = True)

    new_file = file[
        ['jjhklb(C|2)', '#nbxh(C|50)', 'hydm(C|8)', 'djjg(C|20)', 'zczb(N|21|6)', 'jyzt(C|4)', 'clrq(D)', 'qylx(C|6)',
         'tslx(C|2)', 'new']]

    new_revoke = revoke[
        ['jjhklb(C|2)', '#nbxh(C|50)', 'hydm(C|8)', 'djjg(C|20)', 'zczb(N|21|6)', 'jyzt(C|4)', 'clrq(D)', 'qylx(C|6)',
         'tslx(C|2)', 'new']]

    new_file['jyzt(C|4)'].fillna(value=1.0, inplace=True)
    new_revoke['jyzt(C|4)'] = 0.0
    new_file['jyzt(C|4)'] = new_file['jyzt(C|4)'].astype(np.float32)
    new_file.loc[new_file['jyzt(C|4)'] > 0, 'jyzt(C|4)'] = 1
    new_file.loc[new_file['jyzt(C|4)'] == 0, 'jyzt(C|4)'] = 0
    new_file['jyzt(C|4)'] = new_file['jyzt(C|4)'].astype(np.int64)

    new_file = pd.concat([new_file, new_revoke])

    new_file.rename(
        columns={'jjhklb(C|2)': 'jjhklb', '#nbxh(C|50)': 'nbxh', 'hydm(C|8)': 'hydm', 'djjg(C|20)': 'djjg',
                 'zczb(N|21|6)': 'zczb', 'jyzt(C|4)': 'jyzt', 'clrq(D)': 'clrq', 'qylx(C|6)': 'qylx',
                 'tslx(C|2)': 'tslx'},
        inplace=True)

    new_file['jjhklb'].fillna(new_file['jjhklb'].mode()[0], inplace=True)
    new_file['hydm'].fillna(new_file['hydm'].mode()[0], inplace=True)
    new_file['djjg'].fillna(method='ffill', inplace=True)
    new_file['zczb'].fillna(new_file['zczb'].mode()[0], inplace=True)
    new_file['jyzt'].fillna(value='0', inplace=True)
    new_file['clrq'].fillna(new_file['clrq'].mode()[0], inplace=True)
    new_file['djjg'] = new_file['djjg'].astype(np.int64)
    new_file['hydm'] = new_file['hydm'].str[0]

    new_file.set_index('nbxh', inplace=True)

    new_file['time'] = datetime.now().year - new_file['clrq'].str[:4].astype(np.int64)

    new_file['time_scale'] = None
    new_file.loc[new_file['time'] <= 1, 'time_scale'] = '1'
    new_file.loc[((new_file['time'] > 1) & (new_file['time'] <= 5)), 'time_scale'] = '2'
    new_file.loc[((new_file['time'] > 5) & (new_file['time'] <= 10)), 'time_scale'] = '3'
    new_file.loc[new_file['time'] > 10, 'time_scale'] = '4'

    new_file.drop(['clrq', 'time'], axis=1, inplace=True)

    new_file['city'] = None
    new_file['djjg'] = new_file['djjg'].astype(str)
    new_file.info()

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

    new_file.drop(['djjg'], axis=1, inplace=True)

    new_file['three'] = None
    new_file.loc[new_file['hydm'] == 'A', 'three'] = '1'
    second = ['B', 'C', 'D', 'E']
    for i in second:
        new_file.loc[new_file['hydm'] == i, 'three'] = '2'
    third = ['F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'Z']
    for i in third:
        new_file.loc[new_file['hydm'] == i, 'three'] = '3'

    new_file['scale'] = None
    new_file.loc[new_file['zczb'] <= 100, 'scale'] = '1'
    new_file.loc[((new_file['zczb'] > 100) & (new_file['zczb'] <= 1_000)), 'scale'] = '2'
    new_file.loc[((new_file['zczb'] > 1_000) & (new_file['zczb'] <= 10_000)), 'scale'] = '3'
    new_file.loc[((new_file['zczb'] > 10_000) & (new_file['zczb'] <= 20_000)), 'scale'] = '4'
    new_file.loc[new_file['zczb'] > 20_000, 'scale'] = '5'

    foreign_investment = [1122, 1123, 1211, 2123, 2211, 5000, 5320, 1121, 5310, 1120,
                          2221, 5180, 5260, 5820, 5840, 1221, 2120, 5400, 5800, 2121,
                          2122, 5250]
    new_file['foreign'] = None
    for i in foreign_investment:
        new_file.loc[new_file['qylx'] == i, 'foreign'] = 1
    new_file['foreign'].fillna(value=0, inplace=True)

    new_file['X1_2'] = 1
    new_file['X3'] = 1
    new_file['X4'] = 1

    new_file['X4'].value_counts()

    # In[48]:

    for i in tqdm([1151, 4540, 2125]):
        new_file.loc[new_file[(new_file['qylx'] == i)].index, 'X4'] = 0
    new_file['X4'].value_counts()

    new_file['X4'].value_counts()[1] / (new_file['X4'].value_counts()[1] + new_file['X4'].value_counts()[0])

    qybg_file = pd.concat([pd.read_csv(path) for path in qybg_paths])
    # -----------------------------------------
    #     qybg_file = pd.read_csv('./第二季度活跃度涉及表/企业变更.csv')

    qybg_file.rename(columns={'#NBXH(C|36)': 'nbxh(C|50)', 'BGSX(C|64)': 'bgsx(C|10)', 'CQRQ(P)': 'cqrq(D)'},
                     inplace=True)

    nums = qybg_file['nbxh(C|50)'].value_counts()

    dict_nums = {'nbxh': nums.index, 'X5': nums.values}
    df_nums = pd.DataFrame(dict_nums)
    df_nums.set_index('nbxh', inplace=True)

    new_file = new_file.join(df_nums)

    new_file['X5'].fillna(value=0, inplace=True)

    qybg_file.drop(['cqrq(D)'], axis=1, inplace=True)
    qybg_grouped = qybg_file.groupby('nbxh(C|50)')
    qybg_grouped.size()

    cate = qybg_grouped['bgsx(C|10)'].value_counts()
    list_cate = list(cate.index)
    res_cate = [list(ele) for ele in list_cate]
    res_cate[:5]

    indexs = [i[0] for i in res_cate]
    df_indexs = pd.DataFrame(indexs)

    nums = df_indexs[0].value_counts()

    dict_nums = {'nbxh': nums.index, 'X6': nums.values}
    df_nums = pd.DataFrame(dict_nums)

    df_nums.set_index('nbxh', inplace=True)

    new_file = new_file.join(df_nums)
    new_file['X6'].fillna(value=0, inplace=True)

    bgsx_M = [120, 170, 700, 134, 118, 155, 117, 127, 136, 154, 914, 131, 923]
    for i in bgsx_M:
        if i == 120:
            qybg_file_M = qybg_file[qybg_file['bgsx(C|10)'] == i]
        else:
            qybg_file_M = pd.concat([qybg_file_M, qybg_file[qybg_file['bgsx(C|10)'] == i]])

    qybg_grouped = qybg_file_M.groupby('nbxh(C|50)')
    qybg_grouped.size()

    cate = qybg_grouped['bgsx(C|10)'].value_counts()
    # 层次化索引cate.index变列表
    list_cate = list(cate.index)
    res_cate = [list(ele) for ele in list_cate]

    indexs = [i[0] for i in res_cate]
    df_indexs = pd.DataFrame(indexs)

    if not res_cate:
        new_file['X12'] = None
    else:
        nums = df_indexs[0].value_counts()

        dict_nums = {'nbxh': nums.index, 'X12': nums.values}
        df_nums = pd.DataFrame(dict_nums)
        df_nums.set_index('nbxh', inplace=True)

        new_file = new_file.join(df_nums)
        new_file.info(show_counts=True)

    new_file['X12'].fillna(value=0, inplace=True)

    nums = qybg_file_M['nbxh(C|50)'].value_counts()

    dict_nums = {'nbxh': nums.index, 'X13': nums.values}
    df_nums = pd.DataFrame(dict_nums)
    # print(df_nums[:2])
    df_nums.set_index('nbxh', inplace=True)

    new_file = new_file.join(df_nums)

    new_file['X13'].fillna(value=0, inplace=True)

    qybg_file[qybg_file['bgsx(C|10)'] == 165]

    new_file['X15'] = 0
    new_file.info(show_counts=True)

    fzjg_file = pd.concat([pd.read_csv(path, encoding='gb18030') for path in fzjg_paths])

    nums_fzjg = fzjg_file['ENTNAME(C|301)'].value_counts()

    dict_nums_fzjg = {'ENTNAME': nums_fzjg.index, 'X7': nums_fzjg.values}
    df_nums_fzjg = pd.DataFrame(dict_nums_fzjg)

    df_nums_fzjg.set_index('ENTNAME', inplace=True)  # 以企业名称为索引进行join操作
    temp_name = file[['#nbxh(C|50)', 'qymc(C|300)']]  # 提取内部序号和企业名称
    temp_name.set_index('qymc(C|300)', inplace=True)  # 企业名称为索引
    df_nums_fzjg = df_nums_fzjg.join(temp_name)

    df_nums_fzjg = df_nums_fzjg.reset_index()  # 重设索引，且不替换掉企业名称

    df_nums_fzjg.drop_duplicates(subset=['ENTNAME'], keep='first', inplace=True)  # 去除重复，join带来的重复，需要思考

    df_nums_fzjg.dropna(inplace=True)
    df_nums_fzjg['#nbxh(C|50)'] = df_nums_fzjg['#nbxh(C|50)']  # .astype(np.int64)
    df_nums_fzjg.set_index('#nbxh(C|50)', inplace=True)
    df_nums_fzjg.drop(['ENTNAME'], axis=1, inplace=True)

    new_file = new_file.join(df_nums_fzjg)

    new_file['X7'].fillna(value=0, inplace=True)

    invest = pd.concat([pd.read_csv(path) for path in qygx_paths])
    # ----------------------------------
    #     invest = pd.read_csv('./第二季度活跃度涉及表/企业关系人.csv')
    invest.rename(columns={'#tznbxh(C|250)': 'nbxh', 'tze(N|18|6)': 'tze'}, inplace=True)

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    invest = invest.dropna()
    invest['nbxh'] = invest['nbxh'].astype(np.int64)

    nums = invest['nbxh'].value_counts()

    dict_nums = {'nbxh': nums.index, 'X10': nums.values}
    df_nums = pd.DataFrame(dict_nums)
    df_nums.set_index('nbxh', inplace=True)

    new_file = new_file.join(df_nums)

    new_file['X10'].fillna(value=0, inplace=True)

    sums = invest.groupby('nbxh')['tze'].agg('sum')

    dict_sums = {'nbxh': sums.index, 'X11': sums.values}
    df_sums = pd.DataFrame(dict_sums)
    df_sums.set_index('nbxh', inplace=True)

    new_file = new_file.join(df_sums)

    new_file['X11'].fillna(value=0, inplace=True)

    qycs_file = pd.concat([pd.read_csv(path, encoding='gb18030') for path in qyb_paths])

    nums = qycs_file['MARPRID(C|75)'].value_counts()

    dict_nums = {'nbxh': nums.index, 'X14': nums.values}
    df_nums = pd.DataFrame(dict_nums)
    df_nums.set_index('nbxh', inplace=True)

    new_file = new_file.join(df_nums)

    new_file['X14'].fillna(value=0, inplace=True)

    new_file['X8'] = 0
    new_file['X9'] = 0
    new_file['X16'] = 0
    new_file['X17'] = 0
    new_file['X18'] = 0
    new_file.info(show_counts=True)

    col_num = new_file.shape[1]
    new_file.insert(col_num - 12, 'X7', new_file.pop('X7'))
    new_file.insert(col_num - 11, 'X8', new_file.pop('X8'))
    new_file.insert(col_num - 10, 'X9', new_file.pop('X9'))
    new_file.insert(col_num - 9, 'X10', new_file.pop('X10'))
    new_file.insert(col_num - 8, 'X11', new_file.pop('X11'))
    new_file.insert(col_num - 7, 'X12', new_file.pop('X12'))
    new_file.insert(col_num - 6, 'X13', new_file.pop('X13'))
    new_file.insert(col_num - 5, 'X14', new_file.pop('X14'))
    new_file.insert(col_num - 4, 'X15', new_file.pop('X15'))
    new_file.insert(col_num - 3, 'X16', new_file.pop('X16'))
    new_file.insert(col_num - 2, 'X17', new_file.pop('X17'))
    new_file.insert(col_num - 1, 'X18', new_file.pop('X18'))

    del file
    gc.collect()

    new_file = new_file.reset_index()

    new_file.rename(columns={'index': 'nbxh'}, inplace=True)
    re_nums = new_file['nbxh'].value_counts()
    re_nums

    new_file.drop_duplicates(subset=['nbxh'], keep='first', inplace=True)
    new_file.info(show_counts=True)

    path = './DataCleaning_quarterTwo_1.csv'
    new_file.to_csv(path, index=False)
    # new_file.set_index("nbxh", inplace = True)
    return quarter, new_file


def s_2(new_month, output_path, dc):
    # path_dc = './DataCleaning_quarterTwo_1.csv'
    # dc = pd.read_csv(path_dc, index_col=[0])

    for i in new_month:
        dc.loc[dc['new'] == i, 'new'] = 1

    dc.loc[dc['new'] != 1, 'new'] = 0

    def series2df(series_name, col_name1, col_name2):
        df_temp = {col_name1: series_name.index, col_name2: series_name.values}
        df_temp = pd.DataFrame(df_temp)
        df_temp.set_index(col_name1, inplace=True)
        return df_temp

    def df_combine(df_name, series_name, col_name1, col_name2):
        df_temp = series2df(series_name, col_name1, col_name2)
        combine_result = pd.concat([df_name, df_temp], axis=1)
        return combine_result

    industry_new = dc[dc['new'] == 1].groupby(['hydm']).size()
    industry_temp = series2df(industry_new, 'hydm', '新设企业')
    industry_all = industry_temp
    industry_all

    industry_live = dc.groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_live, 'hydm', '存量企业(包含期间内的注吊销&迁出)')
    industry_all

    industry_live = dc[dc['jyzt'] == 1].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_live, 'hydm', '存量企业(不包含期间内的注吊销&迁出)')
    industry_all

    industry_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_zdx, 'hydm', '注吊销企业')
    industry_all

    industry_zx = dc[dc['tslx'] == 7].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_zx, 'hydm', '注销企业')

    industry_dx = dc[dc['tslx'] == 11].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_dx, 'hydm', '吊销企业')

    industry_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_qrc, 'hydm', '迁入迁出企业')

    industry_qr = dc[dc['tslx'] == 9].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_qr, 'hydm', '迁入企业')

    industry_qc = dc[dc['tslx'] == 13].groupby(['hydm']).size()
    industry_all = df_combine(industry_all, industry_qc, 'hydm', '迁出企业')

    # -------------------------
    industry_all.fillna(value=0).to_excel(output_path + '/不同行业下细分.xlsx')

    city_new = dc[dc['new'] == 1].groupby(['city']).size()
    city_temp = series2df(city_new, 'city', '新设企业')
    city_all = city_temp

    city_live = dc.groupby(['city']).size()
    city_all = df_combine(city_all, city_live, 'city', '存量企业(包含此期间内的注吊销&迁出)')

    city_live = dc[dc['jyzt'] == 1].groupby(['city']).size()
    city_all = df_combine(city_all, city_live, 'city', '存量企业(不包含此期间内的注吊销&迁出)')

    city_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['city']).size()
    city_all = df_combine(city_all, city_zdx, 'city', '注吊销企业')

    city_zx = dc[dc['tslx'] == 7].groupby(['city']).size()
    city_all = df_combine(city_all, city_zx, 'city', '注销企业')

    city_dx = dc[dc['tslx'] == 11].groupby(['city']).size()
    city_all = df_combine(city_all, city_dx, 'city', '吊销企业')

    city_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['city']).size()
    city_all = df_combine(city_all, city_qrc, 'city', '迁入迁出企业')

    city_qr = dc[dc['tslx'] == 9].groupby(['city']).size()
    city_all = df_combine(city_all, city_qr, 'hydm', '迁入企业')

    city_qc = dc[dc['tslx'] == 13].groupby(['city']).size()
    city_all = df_combine(city_all, city_qc, 'hydm', '迁出企业')
    # ---------------------------------
    city_all.fillna(value=0).to_excel(output_path + '/不同地区下细分.xlsx')

    three_new = dc[dc['new'] == 1].groupby(['three']).size()
    three_temp = series2df(three_new, 'three', '新设企业')
    three_all = three_temp

    three_live = dc.groupby(['three']).size()
    three_all = df_combine(three_all, three_live, 'three', '存量企业(包含此期间内的注吊销&迁出)')

    three_live = dc[dc['jyzt'] == 1].groupby(['three']).size()
    three_all = df_combine(three_all, three_live, 'three', '存量企业(不包含此期间内的注吊销&迁出)')

    three_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['three']).size()
    three_all = df_combine(three_all, three_zdx, 'three', '注吊销企业')

    three_zx = dc[dc['tslx'] == 7].groupby(['three']).size()
    three_all = df_combine(three_all, three_zx, 'three', '注销企业')

    three_dx = dc[dc['tslx'] == 11].groupby(['three']).size()
    three_all = df_combine(three_all, three_dx, 'three', '吊销企业')

    three_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['three']).size()
    three_all = df_combine(three_all, three_qrc, 'three', '迁入迁出企业')

    three_qr = dc[dc['tslx'] == 9].groupby(['three']).size()
    three_all = df_combine(three_all, three_qr, 'hydm', '迁入企业')

    three_qc = dc[dc['tslx'] == 13].groupby(['three']).size()
    three_all = df_combine(three_all, three_qc, 'hydm', '迁出企业')
    # ---------------------------
    three_all.fillna(value=0).to_excel(output_path + '/不同产业下细分.xlsx')

    temp_sum = pd.DataFrame(dc.groupby(['hydm', 'scale'])['zczb'].sum())
    df_industry_scale_sum = temp_sum.sum(axis=0)
    industry_scale = dc.groupby(['hydm', 'scale']).size()
    df_industry_scale = pd.DataFrame(industry_scale)
    df_industry_scale.rename(columns={0: 'count'}, inplace=True)
    df_industry_scale = df_industry_scale.join(temp_sum)

    # ---------------------------
    write = pd.ExcelWriter(output_path + '/不同行业注册资金规模.xlsx')
    df_industry_scale.fillna(value=0).to_excel(write, sheet_name='细分')
    df_industry_scale_sum.to_excel(write, sheet_name='求和')
    write.close()

    temp_sum = pd.DataFrame(dc.groupby(['three', 'scale'])['zczb'].sum())
    df_three_scale_sum = temp_sum.sum(axis=0)
    three_scale = dc.groupby(['three', 'scale']).size()
    df_three_scale = pd.DataFrame(three_scale)
    df_three_scale.rename(columns={0: 'count'}, inplace=True)
    df_three_scale = df_three_scale.join(temp_sum)
    df_three_scale

    # -------------------------------
    write = pd.ExcelWriter(output_path + '/不同产业注册资金规模.xlsx')
    df_three_scale.fillna(value=0).to_excel(write, sheet_name='细分')
    df_three_scale_sum.to_excel(write, sheet_name='求和')
    write.close()

    temp_sum = pd.DataFrame(dc.groupby(['city', 'scale'])['zczb'].sum())
    df_city_scale_sum = temp_sum.sum(axis=0)
    city_scale = dc.groupby(['city', 'scale']).size()
    df_city_scale = pd.DataFrame(city_scale)
    df_city_scale.rename(columns={0: 'count'}, inplace=True)
    df_city_scale = df_city_scale.join(temp_sum)
    df_city_scale

    write = pd.ExcelWriter(output_path + '/不同地区注册资金规模.xlsx')
    df_city_scale.fillna(value=0).to_excel(write, sheet_name='细分')
    df_city_scale_sum.to_excel(write, sheet_name='求和')
    write.close()

    c_i_new = dc[dc['new'] == 1].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_new)
    c_i_temp.rename(columns={0: '新设企业'}, inplace=True)
    c_i_all = c_i_temp

    c_i_live = dc.groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_live)
    c_i_temp.rename(columns={0: '存量企业(包含此期间内的注吊销&迁出)'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_live = dc[dc['jyzt'] == 0].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_live)
    c_i_temp.rename(columns={0: '存量企业(不包含此期间内的注吊销&迁出)'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_zdx = dc[(dc['tslx'] == 7) | (dc['tslx'] == 11)].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_zdx)
    c_i_temp.rename(columns={0: '注吊销企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)
    c_i_all

    c_i_zx = dc[dc['tslx'] == 7].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_zx)
    c_i_temp.rename(columns={0: '注销企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_dx = dc[dc['tslx'] == 11].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_dx)
    c_i_temp.rename(columns={0: '吊销企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_qrc = dc[(dc['tslx'] == 9) | (dc['tslx'] == 13)].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_qrc)
    c_i_temp.rename(columns={0: '迁入迁出企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_qr = dc[dc['tslx'] == 9].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_qr)
    c_i_temp.rename(columns={0: '迁入企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_qc = dc[dc['tslx'] == 13].groupby(['city', 'hydm']).size()
    c_i_temp = pd.DataFrame(c_i_qc)
    c_i_temp.rename(columns={0: '迁出企业'}, inplace=True)
    c_i_all = pd.concat([c_i_all, c_i_temp], axis=1)

    c_i_all.fillna(value=0).to_excel(output_path + '/各地区不同行业下市场主体数量.xlsx')


def s_3(dc):
    #
    path_dc = './DataCleaning_quarterTwo_1.csv'
    dc = pd.read_csv(path_dc, index_col=[0])

    dc['X18'] = np.random.randint(0, 10, len(dc))

    grouped = dc.groupby('hydm')

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

    feature_list = ['X5', 'X6', 'X7', 'X10', 'X11', 'X12', 'X13', 'X14', 'X18']
    alphabet = [chr(i) for i in range(65, 85)]  # 'B' - 'T'
    alphabet.append(chr(90))  # "Z"

    X5_mean, X5_std = [], []
    X6_mean, X6_std = [], []
    X7_mean, X7_std = [], []
    X10_mean, X10_std = [], []
    X11_mean, X11_std = [], []
    X12_mean, X12_std = [], []
    X13_mean, X13_std = [], []
    X14_mean, X14_std = [], []

    X18_mean, X18_std = [], []

    for i in tqdm(feature_list):
        # 一下语句把固定的string改为变量名
        temp_mean = np.str_(i) + '_mean'
        temp_std = np.str_(i) + '_std'
        for j in alphabet:
            temp_alpha = 'group_' + np.str_(j)
            eval(temp_mean).append(eval(temp_alpha)[eval(temp_alpha)[i] > 0][i].mean())

            eval(temp_std).append(eval(temp_alpha)[eval(temp_alpha)[i] > 0][i].std())

    def fill_nan(temp_list):
        temp_list_nan = np.isnan(temp_list)
        for i in range(len(temp_list)):
            if temp_list_nan[i] == True:
                temp_list[i] = 0

    for i in feature_list:
        # 一下语句把固定的string改为变量名
        temp_mean = np.str_(i) + '_mean'
        temp_std = np.str_(i) + '_std'
        fill_nan(eval(temp_mean))
        fill_nan(eval(temp_std))

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

    for i in tqdm(feature_list):
        for j in range(len(alphabet)):
            temp_max = np.str_(i) + '_max'
            temp_min = np.str_(i) + '_min'
            temp_alpha = 'group_' + np.str_(alphabet[j])
            eval(temp_alpha).loc[(eval(temp_alpha)[i] > 0) & (eval(temp_alpha)[i] < eval(temp_min)[j]), i] = \
            eval(temp_min)[j]
            eval(temp_alpha).loc[eval(temp_alpha)[i] > eval(temp_max)[j], i] = eval(temp_max)[j]

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
        temp_mean = np.str_(i) + '_mean'
        for j in alphabet:
            temp_alpha = 'group_' + np.str_(j)
            eval(temp_mean).append(eval(temp_alpha)[i].mean())

    for i in feature_list:
        dc[i] = None

    # In[15]:

    for i in tqdm(alphabet):
        temp_alpha = 'group_' + np.str_(i)
        eval(temp_alpha).set_index('nbxh', inplace=True)

        globals()[temp_alpha] = eval(temp_alpha)[feature_list]  # 提取出需要更改的列
        # 更改列名
        globals()[temp_alpha].rename(
            columns={'X5': 'X5_fill', 'X6': 'X6_fill', 'X7': 'X7_fill', 'X10': 'X10_fill',
                     'X11': 'X11_fill', 'X12': 'X12_fill', 'X13': 'X13_fill', 'X14': 'X14_fill', 'X18': 'X18_fill'},
            inplace=True)

        dc = dc.join(globals()[temp_alpha])
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

    X5_mean_all = dc['X5'].mean()
    X6_mean_all = dc['X6'].mean()
    X7_mean_all = dc['X7'].mean()
    X10_mean_all = dc['X10'].mean()
    X11_mean_all = dc['X11'].mean()
    X12_mean_all = dc['X12'].mean()
    X13_mean_all = dc['X13'].mean()
    X14_mean_all = dc['X14'].mean()

    X18_mean_all = dc['X18'].mean()

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

    para_1 = pd.DataFrame(data=None,
                          columns=['I_1_2', 'I_3', 'I_4', 'I_5', 'I_6', 'I_7', 'I_8', 'I_9', 'I_10', 'I_11', 'I_12',
                                   'I_13', 'I_14', 'I_15', 'I_16', 'I_17', 'I_18'],
                          index=alphabet)

    para_1['I_5'] = a_5
    para_1['I_6'] = a_6
    para_1['I_7'] = a_7
    para_1['I_10'] = a_10
    para_1['I_11'] = a_11
    para_1['I_12'] = a_12
    para_1['I_13'] = a_13
    para_1['I_14'] = a_14

    para_1['I_18'] = a_18

    para_1.fillna(value=1, inplace=True)

    # path_para = './para_half_1.csv'
    # para_1.to_csv(path_para)

    grouped_scale = dc.groupby('scale')
    grouped_scale.size()

    # print(dc['scale'][:5])
    group_1 = grouped_scale.get_group(1).reset_index()
    group_2 = grouped_scale.get_group(2).reset_index()
    group_3 = grouped_scale.get_group(3).reset_index()
    group_4 = grouped_scale.get_group(4).reset_index()
    group_5 = grouped_scale.get_group(5).reset_index()

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

    for i in feature_list:
        # 一下语句把固定的string改为变量名
        temp_mean = np.str_(i) + '_mean_S'
        for j in group_list:
            temp_alpha = 'group_' + np.str_(j)
            eval(temp_mean).append(eval(temp_alpha)[i].mean())

    a_5_s = []
    a_6_s = []
    a_7_s = []
    a_10_s = []
    a_11_s = []
    a_12_s = []
    a_13_s = []
    a_14_s = []

    a_18_s = []

    scale_num = 5

    def scale_parameter(temp_mean_all, temp_mean, temp_list):
        for i in range(scale_num):
            if temp_mean[i] != 0:
                temp_list.append(temp_mean_all / temp_mean[i])
            else:
                temp_list.append(1)

    scale_parameter(X5_mean_all, X5_mean_S, a_5_s)
    scale_parameter(X6_mean_all, X6_mean_S, a_6_s)
    scale_parameter(X7_mean_all, X7_mean_S, a_7_s)
    scale_parameter(X10_mean_all, X10_mean_S, a_10_s)
    scale_parameter(X11_mean_all, X11_mean_S, a_11_s)
    scale_parameter(X12_mean_all, X12_mean_S, a_12_s)
    scale_parameter(X13_mean_all, X13_mean_S, a_13_s)
    scale_parameter(X14_mean_all, X14_mean_S, a_14_s)

    scale_parameter(X18_mean_all, X18_mean_S, a_18_s)

    lis = ['N1', 'N2', 'N3', 'N4', 'N5']
    para_2 = pd.DataFrame(data=None,
                          columns=['S_1_2', 'S_3', 'S_4', 'S_5', 'S_6', 'S_7', 'S_8', 'S_9', 'S_10', 'S_11', 'S_12',
                                   'S_13', 'S_14', 'S_15', 'S_16', 'S_17', 'S_18'],
                          index=lis)

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

    # path_para = './para_half_2.csv'
    # para_2.to_csv(path_para)

    for i in tqdm(feature_list):
        dc[i] = (dc[i] - dc[i].min()) / (dc[i].max() - dc[i].min())

    dc.fillna(value=0.0, inplace=True)

    return para_1, para_2, dc


def s_4(output_path, industry, scale, dc):
    # dc.set_index('nbxh', inplace=True)
    # path_para_1 = './para_half_1.csv'
    # industry = pd.read_csv(path_para_1, index_col=[0])
    #
    # path_para_2 = './para_half_2.csv'
    # scale = pd.read_csv(path_para_2, index_col=[0])

    # 给定权重
    weight = [0.4, 0.15, 0.15, 0.05, 0.05, 0.05, 0.02, 0.02, 0.025, 0.025, 0.01, 0.01, 0.04, -0.03, -0.01, -0.01, 0.05]

    alphabet_all = [chr(i) for i in range(65, 85)]
    alphabet_all.append(chr(90))

    industry_matrix = industry.values
    scale_matrix = scale.values

    IS_matrix = industry_matrix * scale_matrix[0]
    for i in tqdm(range(1, 5)):
        IS_matrix = np.concatenate((IS_matrix, (industry_matrix * scale_matrix[i])))

    ISW_matrix = IS_matrix * np.array(weight)

    ISW_matrix_df = pd.DataFrame(ISW_matrix)

    reindex = ['A_1', 'B_1', 'C_1', 'D_1', 'E_1', 'F_1', 'G_1', 'H_1', 'I_1', 'J_1', 'K_1', 'L_1', 'M_1', 'N_1', 'O_1',
               'P_1', 'Q_1', 'R_1', 'S_1', 'T_1', 'Z_1', 'A_2', 'B_2', 'C_2', 'D_2', 'E_2', 'F_2', 'G_2', 'H_2', 'I_2',
               'J_2', 'K_2', 'L_2', 'M_2', 'N_2', 'O_2', 'P_2', 'Q_2', 'R_2', 'S_2', 'T_2', 'Z_2', 'A_3', 'B_3', 'C_3',
               'D_3', 'E_3', 'F_3', 'G_3', 'H_3', 'I_3', 'J_3', 'K_3', 'L_3', 'M_3', 'N_3', 'O_3', 'P_3', 'Q_3', 'R_3',
               'S_3', 'T_3', 'Z_3', 'A_4', 'B_4', 'C_4', 'D_4', 'E_4', 'F_4', 'G_4', 'H_4', 'I_4', 'J_4', 'K_4', 'L_4',
               'M_4', 'N_4', 'O_4', 'P_4', 'Q_4', 'R_4', 'S_4', 'T_4', 'Z_4', 'A_5', 'B_5', 'C_5', 'D_5', 'E_5', 'F_5',
               'G_5', 'H_5', 'I_5', 'J_5', 'K_5', 'L_5', 'M_5', 'N_5', 'O_5', 'P_5', 'Q_5', 'R_5', 'S_5', 'T_5', 'Z_5']

    recolumns = ['a_1_2', 'a_3', 'a_4', 'a_5', 'a_6', 'a_7', 'a_8', 'a_9', 'a_10', 'a_11', 'a_12', 'a_13', 'a_14',
                 'a_15', 'a_16', 'a_17', 'a_18']

    ISW_matrix_df.index = reindex
    ISW_matrix_df.columns = recolumns

    k = 0
    dc_2 = dc
    dc_2['EA'] = None
    for i in range(5):
        for j in alphabet_all:
            k = k + 1
            start = time.perf_counter()
            dc_T = dc[((dc['hydm'] == j) & (dc['scale'] == i + 1))]
            # 选择需要的17个特征
            dc_T_feature = dc_T.loc[:, 'X1_2':'X18']
            col = j + '_' + str(i + 1)
            # 显示进度
            print(k, '/105:  ', end='')
            EA_T = dc_T_feature.values * ISW_matrix_df.loc[col].values
            EA_T = EA_T.sum(axis=1) * dc_T['jyzt'].values
            dc_T_feature['EA'] = EA_T
            dc_T_feature = dc_T_feature['EA']
            dc_T_feature = pd.DataFrame({'nbxh': dc_T_feature.index, 'EA_fill': dc_T_feature.values})
            dc_T_feature.set_index('nbxh', inplace=True)
            # 使用join和fillna方法
            dc_2 = dc_2.join(dc_T_feature)
            dc_2["EA"].fillna(dc_2["EA_fill"], inplace=True)
            dc_2.drop(['EA_fill'], axis=1, inplace=True)
            end = time.perf_counter()
            print('Running time: %.4f Seconds' % (end - start))

    temp_EA75 = dc_2['EA'].describe()['25%']

    dc = dc_2

    dc['EA_temp'] = None
    dc.loc[dc['EA'] >= temp_EA75, 'EA_temp'] = 1
    dc.loc[dc['EA'] < temp_EA75, 'EA_temp'] = 0

    EA_all = dc['EA_temp'].value_counts()[1] / (dc['EA_temp'].value_counts()[1] + dc['EA_temp'].value_counts()[0])

    # -----------------------
    with open(output_path + '\整体活跃度.txt', 'w') as f:
        f.write(str(EA_all))

    industry_grouped = dc.groupby('hydm')['EA_temp']
    scale_grouped = dc.groupby('scale')['EA_temp']
    city_grouped = dc.groupby('city')['EA_temp']
    three_grouped = dc.groupby('three')['EA_temp']
    economic_grouped = dc.groupby('jjhklb')['EA_temp']
    time_grouped = dc.groupby('time_scale')['EA_temp']
    foreign_grouped = dc.groupby('foreign')['EA_temp']

    def class_EA(grouped):
        name_value = grouped.value_counts()
        name_all = []  # 0,1两类，会有重复的name
        for i in list(name_value.index):
            name_all.append(i[0])
            name_clean = []
        # 列表推导式，去除列表重复值
        [name_clean.append(i) for i in name_all if not i in name_clean]
        df_name = pd.DataFrame(index=name_clean, columns=['proportion', 'sum'])

        for n in name_clean:
            temp_sum = 0
            for j in list(name_value[n]):
                # 每个类别的value一般都有1， 0两类
                temp_sum = temp_sum + j
            temp_num = name_value[n, 1] / temp_sum
            df_name.loc[n, 'proportion'] = temp_num
            df_name.loc[n, 'sum'] = temp_sum
        return df_name

    # -------------------
    df_industry = class_EA(industry_grouped)
    df_industry.to_excel(output_path + '/行业活跃度.xlsx')

    df_scale = class_EA(scale_grouped)
    df_scale.to_excel(output_path + '/规模活跃度.xlsx')

    df_city = class_EA(city_grouped)
    df_city.to_excel(output_path + '/地区活跃度.xlsx')

    df_three = class_EA(three_grouped)
    df_three.to_excel(output_path + '/三次产业活跃度.xlsx')

    df_economic = class_EA(economic_grouped)

    df_economic.to_excel(output_path + '/经济户口活跃度.xlsx')

    df_time = class_EA(time_grouped)
    df_time.to_excel(output_path + '/企业存续时间活跃度.xlsx')

    df_foreign = class_EA(foreign_grouped)
    df_foreign.to_excel(output_path + '/是否外商投资活跃度.xlsx')

    first = dc[dc['three'] == 1]['hydm'].value_counts()
    second = dc[dc['three'] == 2]['hydm'].value_counts()
    third = dc[dc['three'] == 3]['hydm'].value_counts()

    def industry_num(value):
        df_name = pd.DataFrame(index=value.index, columns=['num', 'proportion'])
        df_name['num'] = value
        df_name['proportion'] = value / value.sum()
        return df_name

    df_first = industry_num(first)
    df_second = industry_num(second)
    df_third = industry_num(third)

    df_first.to_excel(output_path + '/分行业：一产行业数量及占比.xlsx')
    df_second.to_excel(output_path + '/分行业：二产行业数量及占比.xlsx')
    df_third.to_excel(output_path + '/分行业：三产行业数量及占比.xlsx')


def multi_month(ztdj_path, qybg_paths, fzjg_paths, qygx_paths, qyb_paths, start_month, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    quarter, dc = s_1(ztdj_path, qybg_paths, fzjg_paths, qygx_paths, qyb_paths, start_month)
    s_2(quarter, output_path, dc)
    para_1, para2, dc_1 = s_3(dc)
    s_4(output_path, para_1, para2, dc_1)

    # 删除临时文件
    if (os.path.isfile("./DataCleaning_quarterTwo_1.csv")):
        os.remove("./DataCleaning_quarterTwo_1.csv")
    if (os.path.isfile("./DataCleaning_quarterTwo_2.csv")):
        os.remove("./DataCleaning_quarterTwo_2.csv")
    if (os.path.isfile("./para_half_1.csv")):
        os.remove("./para_half_1.csv")
    if (os.path.isfile("./para_half_2.csv")):
        os.remove("./para_half_2.csv")


def Get_file_list(file_path ,qybg_paths ,fzjg_paths ,qygx_paths ,qyb_paths):
    for root , dir , files in os.walk(file_path):
        if len(dir) == 0:

            if "变更情况表" in root :
                    qybg_paths.append(os.path.join(root ,files[0]))
            if "分支机构表" in root :
                    fzjg_paths.append(os.path.join(root ,files[0]))
            if "企业关系人表" in root:
                qygx_paths.append(os.path.join(root, files[0]))
            if "迁移信息表" in root:
                qyb_paths.append(os.path.join(root, files[0]))

if __name__ == '__main__':
    print('当前 Python 解释器路径：')
    print(sys.executable)

    qybg_paths = []
    fzjg_paths = []
    qygx_paths = []
    qyb_paths = []

    print('当前 Python 解释器路径：')
    print(sys.executable)

    data_path = sys.argv[1]
    ztdj_path = sys.argv[2] #末月主体等级表
    start_month = sys.argv[3] #开始年月
    output_path = sys.argv[4] #输出文件夹
    Get_file_list(data_path ,qybg_paths ,fzjg_paths ,qygx_paths ,qyb_paths)
    #
    # ztdj_path = 'quarterly_2_data/月底统计202406/主体登记20240626/exportsql.20240626105306.gbk.csv'
    # qybg_paths = [
    #     'quarterly_1_data/月底统计20240126/变更情况表20240126/exportsql.20240126101619.gbk.csv',
    #     'quarterly_1_data/月底统计20240226/变更情况表20240226/exportsql.20240226095428.gbk.csv',
    #     'quarterly_1_data/月底统计20240326/变更情况表20240326/exportsql.20240326100115.gbk.csv',
    #     'quarterly_2_data/月底统计202404/变更情况表20240426/exportsql.20240426092343.gbk.csv',
    #     'quarterly_2_data/月底统计202405/变更情况表20240529/exportsql.20240529163614.gbk.csv',
    #     'quarterly_2_data/月底统计202406/变更情况表20240626/exportsql.20240626110359.gbk.csv',
    # ]
    # fzjg_paths = [
    #     'quarterly_1_data/月底统计20240126/分支机构表20240126/exportsql.20240126101941.gbk.csv',
    #     'quarterly_1_data/月底统计20240226/分支机构表20240226/exportsql.20240226095836.gbk.csv',
    #     'quarterly_1_data/月底统计20240326/分支机构表20240326/exportsql.20240326100245.gbk.csv',
    #     'quarterly_2_data/月底统计202404/分支机构表20240426/exportsql.20240426092547.gbk.csv',
    #     'quarterly_2_data/月底统计202405/分支机构表20240529/exportsql.20240529163751.gbk.csv',
    #     'quarterly_2_data/月底统计202406/分支机构表20240626/exportsql.20240626110548.gbk.csv',
    # ]
    # qygx_paths = [
    #     'quarterly_1_data/月底统计20240126/企业关系人表20240126/exportsql.20240126101312.gbk.csv',
    #     'quarterly_1_data/月底统计20240226/企业关系人表20240226/exportsql.20240226095002.gbk.csv',
    #     'quarterly_1_data/月底统计20240326/企业关系人表20240326/exportsql.20240326095939.gbk.csv',
    #     'quarterly_2_data/月底统计202404/企业关系人表20240426/exportsql.20240426092155.gbk.csv',
    #     'quarterly_2_data/月底统计202405/企业关系人表20240529/exportsql.20240529162820.gbk.csv',
    #     'quarterly_2_data/月底统计202406/企业关系人表20240626/exportsql.20240626110202.gbk.csv',
    # ]
    # qyb_paths = [
    #     'quarterly_1_data/月底统计20240126/迁移信息表20240126/exportsql.20240126101748.gbk.csv',
    #     'quarterly_1_data/月底统计20240226/迁移信息表20240226/exportsql.20240226095641.gbk.csv',
    #     'quarterly_1_data/月底统计20240326/迁移信息表20240326/exportsql.20240326100217.gbk.csv',
    #     'quarterly_2_data/月底统计202404/迁移信息表20240426/exportsql.20240426092436.gbk.csv',
    #     'quarterly_2_data/月底统计202405/迁移信息表20240529/exportsql.20240529163717.gbk.csv',
    #     'quarterly_2_data/月底统计202406/迁移信息表20240626/exportsql.20240626110512.gbk.csv',
    # ]
    #
    # start_month = '2024-01'
    # output_path = './output'

    '''
    ztdj_path:主体登记表的路径，只有一个

    qybg_paths: 所有的变更情况表路径的集合，如果是季度计算就有3条，半年有6条，年度有12条
    fzjg_paths，qygx_paths，qyb_paths同上

    start_month:数据的起始月份
    output_path：输出文件夹的路径, 预先创建

    '''

    # 根据输入数量的不同进行季度、半年度、年度活跃度计算
    multi_month(ztdj_path, qybg_paths, fzjg_paths, qygx_paths, qyb_paths, start_month, output_path)



