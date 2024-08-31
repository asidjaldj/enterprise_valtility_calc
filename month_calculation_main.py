import json
import logging
import os
import sys
import time
import zipfile
import datetime
import numpy as np
import pandas
from monthly import step_1_data_clean, step_2_abnormal_params_handle, step_3_vitality

DIR_NAME = ["变更情况表", "分支机构表", "企业关系人表", "迁移信息表", "异常名录", "主体登记"]


def setup_io():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    print("设置标准输出流编码为utf-8")


if sys.stdout.encoding != 'utf-8':
    setup_io()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def check_data(data_dir):
    """检查数据源是否完整"""
    logger.info("开始检查数据文件是否完整")
    data_files = {}
    for root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            item_name = is_data_dir(dir_name)
            if not item_name:
                continue
            file_name = get_dir_file(os.path.join(root, dir_name))
            if not file_name:
                logger.error(f"缺少【{dir_name} 】数据文件")
                raise ValueError("缺少文件")
            logger.info(f"项目:{item_name} 文件：{file_name}")
            data_files[item_name] = file_name
    if len(data_files.keys()) != len(DIR_NAME):
        diff_name = set(DIR_NAME) - set(data_files.keys())
        raise RuntimeError("缺少文件: " + ",".join(diff_name))
    else:
        logger.info(f"数据完整, 数据文件如下：{json.dumps(data_files, ensure_ascii=False)}")
        return data_files


def create_zip_file(dir_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, _, files in os.walk(dir_path):
            for file in files:
                path = os.path.join(root, file)
                arc_name = os.path.relpath(path, dir_path)
                zip_ref.write(path, arc_name)


def is_data_dir(dir_name):
    """
    判断是否数据目录 文件夹名称等于 DIR_NAME 任意一个名称，或者 包含以上任意一个名称
    :param dir_name:
    :return:
    """
    if dir_name in DIR_NAME:
        return dir_name
    else:
        for name in DIR_NAME:
            if name in dir_name:
                return name
    return None


def get_dir_file(path):
    files = os.listdir(path)
    if not len(files):
        return
    for file in files:
        # 只读取csv格式的数据
        if not file.endswith(".csv"):
            continue
        return os.path.join(path, file)


def main(data_dir, month):

    data_files = check_data(data_dir)  #将个数据的地址转换为字典存储
    cache_dir = os.path.join(data_dir, f"cache{int(time.time())}")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    logger.info(f"计算临时存储目录为: {cache_dir}")
    result_data_dir = os.path.join(data_dir, f"data{int(time.time())}")
    if not os.path.exists(result_data_dir):
        os.makedirs(result_data_dir)
    logger.info(f"计算结果存储目录未：{result_data_dir}")
    logger.info("【开始执行】01-数据清洗步骤")
    st = time.time() * 1000
    step_1_data_clean.process(data_files, result_data_dir, cache_dir, month)
    logger.info(f"【执行结束】01-数据清洗步骤, 耗时: {(time.time() * 1000 - st) / 1000} s")
    logger.info("【开始执行】02-异常值处理及参数计算")
    st = time.time() * 1000
    step_2_abnormal_params_handle.process(cache_dir)
    logger.info(f"【执行结束】02-异常值处理及参数计算, 耗时: {(time.time() * 1000 - st) / 1000} s")
    logger.info("【开始执行】03-活跃度计算")

    logger.info(f"计算结果存储目录为: {cache_dir}")
    step_3_vitality.process(cache_dir, result_data_dir)
    t = datetime.datetime.now().strftime("%Y%m%d%H%M")
    logger.info(f"【执行结束】03-活跃度计算, 耗时: {(time.time() * 1000 - st) / 1000} s")
    data_zip_path = os.path.join(data_dir, f"{os.path.basename(data_dir)}_month_{t}.zip")
    create_zip_file(result_data_dir, data_zip_path)
    logger.info("生成结果zip文件, 文件路径为：" + data_zip_path)
    logger.info("SUCCESS_ZIP_FILE_PATH=" + data_zip_path)


if __name__ == '__main__':
    # main(r"D:\codes\bigdata\2023第一季\2023-01", "2023-01")
    try:
        print("stdout encoding=" + sys.stdout.encoding)
        print(sys.argv)
        file_path = sys.argv[1]
        date_time = sys.argv[2]
        main(sys.argv[1], month=date_time)
    except KeyboardInterrupt:
         print("interrupted by user, killing all threads...")
