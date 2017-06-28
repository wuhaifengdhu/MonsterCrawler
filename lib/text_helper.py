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
        match_result = TextHelper.get_pattern_in_context(context, '\d+\s*[+]?\s*year[s]?')
        match_result.extend(TextHelper.get_pattern_in_context(context, '\d+\s*-\s*\d+\s*year[s]?'))
        match_result.extend(TextHelper.get_pattern_in_context(context, '\d+\s*to\s*\d+\s*year[s]?'))
        match_result.extend(TextHelper.get_pattern_in_context(context, pattern_string))
        return match_result

    @staticmethod
    def get_dict_pattern(context, _dict, convert=True):
        match_result = {}
        for key in _dict.keys():
            key_split = key.split(' ')
            if len(key_split) >= 3 and key_split[1] == '...':
                match_times = len(re.findall(re.escape(key_split[0]) + r'( \w+){0,5} ' + re.escape(' '.join(key_split[2:])), context))
            else:
                key = key.strip()
                match_times = len(re.findall(r'\b' + re.escape(key) + r'\b', context))
            if match_times > 0:
                if convert is True and type(_dict[key]) is not int:
                    DictHelper.increase_dic_key(match_result, _dict[key], match_times)
                else:
                    DictHelper.increase_dic_key(match_result, key, match_times)
        return match_result

    @staticmethod
    def word_in_phrase(word, phrase):
        return re.search(r'\b' + re.escape(word) + r'\b', phrase) is not None

    @staticmethod
    def contain(context, word):
        return word.lower() in context.lower()

    @staticmethod
    def unicode_to_ascii(text):
        uni2ascii = {
            ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
            ord('\xc3\xa9'.decode('utf-8')): ord('e'),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),
            ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
            ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
            ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
            ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
            ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),
            ord('\xe2\x84\xa2'.decode('utf-8')): ord(" "),  # This should be tm
            ord('\xc3\xa4'.decode('utf-8')): ord("a"),  # This should be ä
        }
        try:
            return text.decode('utf-8').translate(uni2ascii).encode('ascii')
        except UnicodeEncodeError:
            print ("can not decode %s" % text)
            return text.decode('unicode_escape').encode('ascii', 'ignore')

    @staticmethod
    def get_year(year_string):
        year_string = year_string.strip()
        if year_string == 'Present':
            return 2016.91
        try:
            year_string = int(year_string)
            return year_string
        except ValueError:
            try:
                return TextHelper.get_year_float(year_string)
            except ValueError:
                # print ("can not decode %s " % year_string)
                return None

    @staticmethod
    def get_year_float(month_year):
        month_dict = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        month_year = month_year.split(' ')
        try:
            return int(month_year[1]) + (month_dict[month_year[0]] / 12.0)
        except IndexError:
            # print ("can not decode %s " % str(month_year))
            return None




if __name__ == '__main__':
    # print (TextHelper.get_years_pattern("and 2 - 3 years of work experience "))
    # print(TextHelper.get_pattern_in_context("23 years experience 23+ years", '\d+[+]? years'))
    # print(TextHelper.get_pattern_in_context("2 - 3 years experience 2   to 3 years", '\d+\s*-\s*\d+ years'))
    # print(TextHelper.get_pattern_in_context("2 - 3 years experience 2 to 3 years", '\d+\s*to\s*\d+ years'))
    # print(TextHelper.get_pattern_in_context("one year experience two+ years", 'one[+]? year|two[+]? years|three[+]? years|four[+]? years|five[+]? years|six[+]? years|seven[+]? years|eight[+]? years|night[+]? years|ten[+]? years'))
    print (TextHelper.word_in_phrase('word', 'life word phrase'))

