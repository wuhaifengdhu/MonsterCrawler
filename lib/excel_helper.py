#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
import pandas as pd
import xlwt as excel
from store_helper import StoreHelper
from segment_helper import SegmentHelper


class ExcelHelper(object):
    @staticmethod
    def convert_excel_to_dict(excel_file, dict_file, threshold=5):
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
    def get_probability_dict(excel_file, dict_file):
        probability_dict = {}
        header, raw_data = ExcelHelper.read_excel(excel_file)
        row_number, column_number = raw_data.shape
        if column_number != 2:
            print("Attention! Excel file more than two column, please have a check! Use the first two column as dict")
        for i in range(row_number):
            word_list = SegmentHelper.segment_text(raw_data[i][0])
            word_list = SegmentHelper.lemmatization(word_list)
            if len(word_list) <= 1:  # ignore single word
                continue
            for j in range(len(word_list) - 1):
                probability_dict["%s %s" % (word_list[j], word_list[j + 1])] = raw_data[i][1]
        StoreHelper.store_data(probability_dict, dict_file)
        print("Generalized successfully and store dict to data file %s!" % dict_file)

    @staticmethod
    def read_excel(excel_file):
        excel_data = pd.read_excel(excel_file)
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


if __name__ == '__main__':
    # ExcelHelper.get_probability_dict("../resource/discipline.xlsx", "../resource/discipline_2.dat")
    ExcelHelper.get_probability_dict("../resource/skills.xlsx", "../resource/skills_2.dat")
    # ExcelHelper.get_probability_dict("../resource/education.xlsx", "../resource/education_2.dat")
    # ExcelHelper.convert_excel_to_dict("../resource/features.xlsx", "../resource/feature.dat", 0)
    # _header, _data = ExcelHelper.read_excel('test.xls')
    # _row, _col = _data.shape
    # _mask = [[] for i in range(_col)]
    # for i in range(_col):
    #     _mask[i].extend([1 if _data[r, i] < 0 else 0 for r in range(_row)])
    # _color_dic = {1: "red"}
    # ExcelHelper.write_excel("test_render.xls", _data, "data", _header, _mask, _color_dic)