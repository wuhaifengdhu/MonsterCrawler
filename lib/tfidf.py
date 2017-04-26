#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from dict_helper import DictHelper


class TFIDF(object):
    def __init__(self, blob_dict_list):
        self.blob_dict_list = blob_dict_list
        self.total_blobs = len(blob_dict_list)
        self.total_words_dict = self._collect_words_dict()
        self.current_blob_dict = None
        self.current_blob_dict_total_words = 1

    def _collect_words_dict(self):
        result_dict = {}
        for _dict in self.blob_dict_list:
            for key in _dict.keys():
                DictHelper.increase_dic_key(result_dict, key)
        return result_dict

    def get_tf_idf(self, blob_dict):
        self.current_blob_dict = blob_dict
        self.current_blob_dict_total_words = sum([value for value in blob_dict.values()])
        return {key: self._tf_idf(key) for key in blob_dict.keys()}

    def _tf(self, word):
        return self.current_blob_dict[word] * 1.0 / self.current_blob_dict_total_words

    def _idf(self, word):
        return math.log(self.total_blobs * 1.0 / self.total_words_dict[word] + 0.001)

    def _tf_idf(self, word):
        return self._tf(word) * self._idf(word)
