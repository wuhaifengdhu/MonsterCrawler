#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import operator


class DictHelper(object):
    @staticmethod
    def increase_dic_key(_dict, key_or_list, increase_value=1):
        if type(key_or_list) == list:
            for k in key_or_list:
                _dict[k] = increase_value if k not in _dict else _dict[k] + increase_value
        else:
            _dict[key_or_list] = increase_value if key_or_list not in _dict else _dict[key_or_list] + increase_value

    @staticmethod
    def decrease_dic_key(_dict, key, decrease_value=1):
        if key in _dict and _dict[key] > decrease_value:
            _dict[key] -= decrease_value
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
    def update_dict(total_dict, dict_to_update):
        for key, value in dict_to_update.items():
            total_dict[key] = value

    @staticmethod
    def get_sorted_list(_dict, sorted_by_key=False, reverse=True):
        """
        Default sorted by value. 
        :param reverse: if reverse the result output
        :param _dict: The dict to be sorted
        :param sorted_by_key: True sorted by key, else sorted by value
        :return: A list with sorted value pair
        """
        if sorted_by_key:
            return sorted(_dict.items(), key=operator.itemgetter(0), reverse=reverse)
        else:
            return sorted(_dict.items(), key=operator.itemgetter(1), reverse=reverse)

    @staticmethod
    def dict_from_count_list(_list):
        result_dict = {}
        for item in _list:
            DictHelper.increase_dic_key(result_dict, item)
        return result_dict

    @staticmethod
    def get_key(_dict, search_key, not_found_return_default=True):
        if search_key in _dict:
            return _dict[search_key]
        else:
            if not_found_return_default:
                return search_key
            else:
                return None

    @staticmethod
    def rebuild_dict(origin_dict, convert_dict):
        new_dict = {}
        for key, count in origin_dict.items():
            new_key = DictHelper.get_key(convert_dict, key, False)
            if new_key is None:
                continue
            DictHelper.increase_dic_key(new_dict, new_key, count)
        return new_dict


if __name__ == '__main__':
    # print (DictHelper.merge_dict({"wu": 1, "hai": 2}, {"wu": 3, "hai": 4}))

    # some_dict = {"wu": 1, "hai": 2}
    # DictHelper.decrease_dic_key(some_dict, 'haif')
    # print (some_dict)

    some_dict = {'two': 12, 'one': 2, '2': 6}
    _convert_dict = {'2': 'two'}
    print (DictHelper.rebuild_dict(some_dict, _convert_dict))
