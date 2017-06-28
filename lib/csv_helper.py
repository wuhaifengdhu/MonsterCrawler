#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import random
from dict_helper import DictHelper


class CsvHelper(object):
    @staticmethod
    def write_list_to_csv(csv_file, csv_columns, data_list, sort_data_row=None, escape_first=0, append_rows=[[]]):
        if sort_data_row is not None:
            csv_columns, data_list = CsvHelper.sorted_data_by_row(csv_columns, data_list, sort_data_row, escape_first)
        data_list.extend(append_rows)
        try:
            with open(csv_file, 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(csv_columns)
                for data in data_list:
                    writer.writerow(data)
        except IOError as (error_no, strerror):
            print("I/O error({0}): {1}".format(error_no, strerror))
        return

    @staticmethod
    def sorted_data_by_row(csv_columns, data_list, sort_data_row, escape_first):
        # step 1, parameters check
        if sort_data_row >= len(data_list):
            print ("Sort row large than the data row!")
            return

        # step 2, construct data structure
        new_csv_column = csv_columns[: escape_first]
        new_data_list = [row[: escape_first] for row in data_list]
        data_dict = {}
        # For each column
        for column in range(escape_first, len(csv_columns)):
            # Get the column data for each rwo
            data_column = [data_list[row][column] for row in range(len(data_list))]
            key_for_sort = float(data_list[sort_data_row][column])
            while key_for_sort in data_dict:
                key_for_sort += random.randint(0, 100) * 0.000000001
            data_dict[key_for_sort] = (csv_columns[column], data_column)

        # step 3, sorted by key
        sorted_list = DictHelper.get_sorted_list(data_dict, sorted_by_key=True)
        print (sorted_list)
        for key_for_sort, csv_data in sorted_list:
            new_csv_column.append(csv_data[0])
            for row in range(len(new_data_list)):
                new_data_list[row].append(csv_data[1][row])
        return new_csv_column, new_data_list
