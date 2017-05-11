#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
from dict_helper import DictHelper


class TextHelper(object):
    @staticmethod
    def get_pattern_in_context(context, pattern):
        return re.findall(pattern, context)

    @staticmethod
    def get_years_pattern(context):
        pattern_string = 'one[+ -]+year[s]?|two[+ -]+year[s]?|three[+ -]+year[s]?|four[+ -]+year[s]?|' \
                         'five[+ -]+year[s]?|six[+ -]+year[s]?|seven[+ -]+year[s]?|eight[+ -]+year[s]?|' \
                         'night[+ -]+year[s]?|ten[+ -]+year[s]?'
        match_result = TextHelper.get_pattern_in_context(context, '\d+\s*[+]?\s*years')
        match_result.extend(TextHelper.get_pattern_in_context(context, '\d+\s*-\s*\d+\s*years'))
        match_result.extend(TextHelper.get_pattern_in_context(context, '\d+\s*to\s*\d+\s*years'))
        match_result.extend(TextHelper.get_pattern_in_context(context, pattern_string))
        return match_result

    @staticmethod
    def get_dict_pattern(context, _dict, threshold=100):
        match_result = []
        for key, value in _dict.items():
            if value > threshold and key in context:
                match_result.append(key)
        return match_result

    @staticmethod
    def contain(context, word):
        return word.lower() in context.lower()


if __name__ == '__main__':
    print (TextHelper.get_years_pattern("one+ years one "))
    # print(TextHelper.get_pattern_in_context("23 years experience 23+ years", '\d+[+]? years'))
    # print(TextHelper.get_pattern_in_context("2 - 3 years experience 2   to 3 years", '\d+\s*-\s*\d+ years'))
    # print(TextHelper.get_pattern_in_context("2 - 3 years experience 2 to 3 years", '\d+\s*to\s*\d+ years'))
    # print(TextHelper.get_pattern_in_context("one year experience two+ years", 'one[+]? year|two[+]? years|three[+]? years|four[+]? years|five[+]? years|six[+]? years|seven[+]? years|eight[+]? years|night[+]? years|ten[+]? years'))

