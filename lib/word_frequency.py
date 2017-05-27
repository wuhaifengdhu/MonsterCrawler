#!/usr/bin/python
# -*- coding: utf-8 -*-
from segment_helper import SegmentHelper
from store_helper import StoreHelper
from dict_helper import DictHelper
from html_helper import HTMLHelper
import operator

#  http://www.english-grammar-revolution.com/list-of-conjunctions.html
conjunctions = "for and nor but or yet so after although as if also though because before by even when whenever where \
wherever while lest once since that unless until till than only in to the with * - &amp . you our &# other from of will\
 more people we support are is it continuing you agree to monster's continuing etc. this &# 8217 into out and/or any \
please (e.g. not have"


class WordFrequency(object):
    @staticmethod
    def get_frequency_dict(content):
        words_list = []
        for line in content.splitlines():
            words_list.extend(SegmentHelper.lemmatization(SegmentHelper.segment_text(line)))
        return DictHelper.dict_from_count_list(words_list)

    @staticmethod
    def calculate_full_frequency():
        html_list = StoreHelper.load_data("../data/post/Delaware.dat", [])
        words_frequency_list = []
        for _url, _web_source in html_list:
            clean_content = HTMLHelper.get_text(_web_source)
            text_dict = WordFrequency.get_frequency_dict(clean_content)
            text_dict = sorted(text_dict.items(), key=operator.itemgetter(1), reverse=True)
            words_frequency_list.append(text_dict)
        for text_dict in words_frequency_list:
            print (text_dict)


if __name__ == '__main__':
    WordFrequency.calculate_full_frequency()
