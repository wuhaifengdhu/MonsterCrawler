#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
import pandas as pd
import xlwt as excel
from store_helper import StoreHelper
from segment_helper import SegmentHelper
from dict_helper import DictHelper


class ExcelHelper(object):
    @staticmethod
    def convert_excel_to_dict(excel_file, dict_file, threshold=1):
        header, raw_data = ExcelHelper.read_excel(excel_file)
        row_number, column_number = raw_data.shape
        if column_number != 2:
            print("Attention! Excel file more than two column, please have a check! Use the first two column as dict")
        data_dict = {raw_data[i][0]: raw_data[i][1] for i in range(row_number)}
        # remove single words
        data_dict = {key.lower(): value for key, value in data_dict.items() if value > threshold}
        StoreHelper.store_data(data_dict, dict_file)
        print ("Generalized successfully and store dict to data file %s!" % dict_file)

    @staticmethod
    def get_normalize_dict(excel_file, dict_file):
        probability_dict = {}
        header, raw_data = ExcelHelper.read_excel(excel_file)
        row_number, column_number = raw_data.shape
        print (raw_data.shape)
        if column_number != 2:
            print("Attention! Excel file more than two column, please have a check! Use the first two column as dict")
        for i in range(row_number):
            key = SegmentHelper.normalize(raw_data[i][0])
            # key = raw_data[i][0]
            if len(key.strip()) == 0:  # ignore single word
                continue
            probability_dict[key] = raw_data[i][1]
        StoreHelper.store_data(probability_dict, dict_file)
        print("Generalized successfully and store dict(%i) to data file %s!" % (len(probability_dict), dict_file))

    @staticmethod
    def read_excel(excel_file, sheet_index=0, header=0):
        excel_data = pd.read_excel(excel_file, sheetname=sheet_index, header=header)
        excel_data.fillna('', inplace=True)
        return excel_data.columns.tolist(), excel_data.values

    @staticmethod
    def write_excel(excel_file, data_array, sheet_name="data", header=None, mask_array=None, color_dict=None):
        if color_dict is None:
            color_dict = {1: "red"}
        book = excel.Workbook()
        sheet = book.add_sheet(sheet_name)
        row, column = data_array.shape

        # Write header to the first line if header exist
        if header:
            for i in range(len(header)):
                sheet.write(0, i, header[i])

        # Write body with render color
        for i in range(row):
            for j in range(column):
                style = ExcelHelper.get_style(i, j, mask_array, color_dict)
                if style is not None:
                    sheet.write(i + 1, j, data_array[i, j], style)
                else:
                    sheet.write(i + 1, j, data_array[i, j])
        book.save(excel_file)

    @staticmethod
    def get_style(r, c, mask_array, color_dic):
        if mask_array is None or color_dic is None:
            return None
        mask_value = mask_array[c][r]
        if mask_value not in color_dic.keys():
            return None
        style = 'pattern: pattern solid, fore_colour %s' % color_dic[mask_value]
        return excel.easyxf(style)

    @staticmethod
    def get_combine_company_dict(store_data_file):
        company_dict = {}
        for tab in range(2):
            header, raw_data = ExcelHelper.read_excel('../resource/us_list_company2.xlsx', tab)
            row, column = raw_data.shape
            for i in range(row):
                company_name = SegmentHelper.normalize(str(raw_data[i][0]).strip())
                if len(company_name) > 0:
                    DictHelper.increase_dic_key(company_dict, raw_data[i][0])
        df = pd.read_csv('../resource/us_list_company_1.csv')
        name_serial = df['Name']
        for i in range(df.shape[0]):
            company_name = SegmentHelper.normalize(name_serial[i])
            if len(company_name) > 0:
                DictHelper.increase_dic_key(company_dict, name_serial[i])
        StoreHelper.store_data(company_dict, store_data_file)

    @staticmethod
    def get_discipline_dict(excel_file, dict_file):
        probability_dict = {}
        header, raw_data = ExcelHelper.read_excel(excel_file)
        row_number, column_number = raw_data.shape
        print(raw_data.shape)
        if column_number != 2:
            print("Attention! Excel file more than two column, please have a check! Use the first two column as dict")
        for i in range(row_number):
            value = raw_data[i][0]
            key_list = raw_data[i][1].split('|')
            for key in key_list:
                key = SegmentHelper.normalize(key)
                if len(key.strip()) == 0:  # ignore single word
                    continue
                probability_dict[key] = value
            probability_dict[SegmentHelper.normalize(value)] = value
        StoreHelper.store_data(probability_dict, dict_file)
        print (probability_dict)
        print("Generalized successfully and store dict(%i) to data file %s!" % (len(probability_dict), dict_file))

if __name__ == '__main__':
    ExcelHelper.get_discipline_dict("../resource/discipline.xlsx", "../resource/discipline.dat")
    ExcelHelper.get_normalize_dict("../resource/skills.xlsx", "../resource/skills.dat")
    ExcelHelper.get_normalize_dict("../resource/education.xlsx", "../resource/education.dat")
    ExcelHelper.get_normalize_dict("../resource/responsibility.xlsx", "../resource/responsibility.dat")
    ExcelHelper.get_normalize_dict("../resource/year_convert.xlsx", "../resource/year_convert.dat")
    # ExcelHelper.get_normalize_dict("../resource/fortune-500-2016.xlsx", "../resource/fortune-500.dat")
    # ExcelHelper.get_combine_company_dict('../resource/company_list.dat')
