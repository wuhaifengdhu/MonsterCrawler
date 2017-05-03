#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import copy
import operator


class DictHelper(object):
    @staticmethod
    def increase_dic_key(_dict, key):
        _dict[key] = 1 if key not in _dict else _dict[key] + 1

    @staticmethod
    def decrease_dic_key(_dict, key):
        if key in _dict and _dict[key] > 1:
            _dict[key] -= 1
        else:
            _dict.pop(key, None)

    @staticmethod
    def append_dic_key(_dict, key, value):
        if key in _dict.keys():
            _dict[key].append(value)
        else:
            _dict[key] = [value]

    @staticmethod
    def merge_dict(total_dict, dict_to_add):
        for key, value in dict_to_add.items():
            if key in total_dict.keys():
                total_dict[key] += value
            else:
                total_dict[key] = value

    @staticmethod
    def get_sorted_list(_dict, sorted_by_key=False):
        """
        Default sorted by value. 
        :param _dict: The dict to be sorted
        :param sorted_by_key: True sorted by key, else sorted by value
        :return: A list with sorted value pair
        """
        if sorted_by_key:
            return sorted(_dict.items(), key=operator.itemgetter(0), reverse=True)
        else:
            return sorted(_dict.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def dict_from_count_list(_list):
        result_dict = {}
        for item in _list:
            DictHelper.increase_dic_key(result_dict, item)
        return result_dict

if __name__ == '__main__':
    # print (DictHelper.merge_dict({"wu": 1, "hai": 2}, {"wu": 3, "hai": 4}))
    some_dict = {"wu": 1, "hai": 2}
    DictHelper.decrease_dic_key(some_dict, 'haif')
    print (some_dict)