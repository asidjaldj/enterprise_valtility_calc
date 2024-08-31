import json
import logging
import os
import sys
import time
import zipfile
import re

from quarterly_new import step_1_merge, step_2_clean, step_3_subsection, step_4_abnormal, step_5_vitality

DIR_NAME = ["变更情况表", "分支机构表", "企业关系人表", "迁移信息表", "异常名录", "主体登记"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

pattern = r"\d{6}"
def setup_io():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    print("设置标准输出流编码为utf-8")


if sys.stdout.encoding != 'utf-8':
    setup_io()


def check_data(data_dir, month):

    """检查数据源是否完整"""
    logger.info(f"开始检查数据文件是否完整, month={month}")
    data_files = {}
    for root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            item_name = is_data_dir(dir_name)
            if not item_name:
                continue
            file_name = get_dir_file(os.path.join(root, dir_name))
            if not file_name:
                logger.error(f"缺少【{dir_name} 】数据文件, month={month}")
                raise ValueError("缺少文件")
            logger.info(f"项目:{item_name} 文件：{file_name}, month={month}")
            data_files[item_name] = file_name
    if len(data_files.keys()) != len(DIR_NAME):
        diff_name = set(DIR_NAME) - set(data_files.keys())
        raise RuntimeError("缺少文件: " + ",".join(diff_name))
    else:
        logger.info(f"数据完整, 数据文件如下：{json.dumps(data_files, ensure_ascii=False)}, month={month}")
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


def main(first_month_data_dir, second_month_data_dir, third_month_data_dir):
    quarter_data_list = [] #获取月份的文件
    quarter = [] #获取月份的名字
    # 按月检查季度的数据
    first_month = os.path.basename(first_month_data_dir) #用于获取指定目录的最后一部分，即是文件名
    first_month_data_files = check_data(first_month_data_dir, first_month)
    quarter_data_list.append(first_month_data_files)
    quarter.append(first_month)


    second_month = os.path.basename(second_month_data_dir)
    second_month_data_files = check_data(second_month_data_dir, second_month)
    quarter_data_list.append(second_month_data_files)
    quarter.append(second_month)

    third_month = os.path.basename(third_month_data_dir)
    third_month_data_files = check_data(third_month_data_dir, third_month)
    quarter_data_list.append(third_month_data_files)
 
    quarter.append(third_month)


    # 月度的上级目录为data目录
    data_dir = os.path.dirname(first_month_data_dir) #获取上级目录的名字
    #quarter.append(third_month)

    cache_dir = os.path.join(data_dir, f"cache{int(time.time())}") #获取缓存文件的名字，放在 data_dir 的目录下
    os.makedirs(cache_dir, exist_ok=True) #创建一个多层缓冲文件，当文件存在则抛出警告
    logger.info(f"计算临时存储目录为: {cache_dir}")

    result_data_dir = os.path.join(data_dir, f"data{int(time.time())}")#存放结果的文件夹
    os.makedirs(result_data_dir, exist_ok=True)
    logger.info(f"计算结果存储目录未：{result_data_dir}")


    logger.info("【开始执行】01-季度数据合并")
    step_1_merge.process(quarter_data_list, result_data_dir, cache_dir)
    logger.info("【开始执行】02-数据清洗")
    step_2_clean.process(quarter_data_list, result_data_dir, cache_dir, quarter)
    logger.info("【开始执行】03-细分文件处理")
    step_3_subsection.process(quarter_data_list, result_data_dir, cache_dir, quarter)
    logger.info("【开始执行】04-异常值处理")
    step_4_abnormal.process(quarter_data_list, result_data_dir, cache_dir, quarter)
    logger.info("【开始执行】05-活跃度计算")
    step_5_vitality.process(quarter_data_list, result_data_dir, cache_dir, quarter)
    t = int(time.time())
    data_zip_path = os.path.join(data_dir, f"{os.path.basename(data_dir)}_quarter_{t}.zip")#获取压缩文件的地址
    create_zip_file(result_data_dir, data_zip_path)#创建压缩文件
    logger.info("生成结果zip文件, 文件路径为：" + data_zip_path)
    logger.info("SUCCESS_ZIP_FILE_PATH=" + data_zip_path)


if __name__ == '__main__':

    try:
        print("stdout encoding = " + sys.stdout.encoding)
        print(sys.argv[0])
        first_month = sys.argv[1]
        second_month = sys.argv[2]
        third_month = sys.argv[3]
        main(first_month, second_month, third_month)
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")
