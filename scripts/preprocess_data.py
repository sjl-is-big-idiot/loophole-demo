
# _*_ coding: utf-8 _*_
# @FileName : clean_raw_data.py
# @Author   : sjl
# @CreatedAt     :  2021/03/10 16:25:46
# @UpdatedAt     :  2021/03/16 16:25:46
# @description: 数据预处理
# @Software : VSCode

import csv
import os
from logger import SimpleLogger

sp_logger = SimpleLogger(__name__, "./log/preprocess_data.log").get_logger()

class DataCleanerInterface(object):
    """数据清洗器接口类"""
    def __init__(self):
        raise Exception("Interface class could't instantiate!")

    def read_raw_data(self):
        """read raw data"""
        raise Exception("This methos must be implemented!")

    def keep_fields(self, fields=[]):
        """
        :param fields: list. It indicated that need reserved fileds, other fields will be delete.
        """
        raise Exception("This methos must be implemented!")



class LoopHolesDataCleaner(DataCleanerInterface):
    """漏洞数据清洗器"""
    def __init__(self):
        pass

    def handle(self, old_files_path, fields=[]):
        """xxx"""
        sp_logger.info("Starting clean {}".format(old_files_path))
        for old_file_name in os.listdir(old_files_path):
            old_file_path = os.path.join( old_files_path,old_file_name)
            result = self.read_csv(os.path.join( old_files_path,old_file_name))
            cleaned_data= [self.keep_fields(row, fields) for row in result]
            new_file_path = self.get_new_filename(old_file_path)
            self.write_csv(cleaned_data, new_file_path, fields)
        sp_logger.info("Completed clean {}".format(old_files_path))
            

    def read_csv(self, filepath):
        """
        读取csv数据
        :param filename: data file path
        """
        sp_logger.info("Reading {}".format(filepath))
        with open(filepath, 'r', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            result = [row for row in reader]
        return result

    def write_csv(self, data, filepath, fields):
        """xxx"""
        sp_logger.info("Writing cleaned data to {}".format(filepath))
        with open(filepath, 'w', newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

    def keep_fields(self, row, fields=[]):
        """
        :param row: csv data per line. dict type.
        :param fields: need keeped fields. list type.
        """
        reserved = {}
        for field in fields:
            reserved[field] = row.get(field)
        return reserved
            
    @staticmethod
    def get_new_filename(old_file_name):
        """
        """
        prefix, subfix = old_file_name.split(".")
        return prefix + "-cleaned" + "." + subfix
        
        