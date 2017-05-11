#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from nltk.stem.wordnet import WordNetLemmatizer
from dict_helper import DictHelper
from store_helper import StoreHelper
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
lmtzr = WordNetLemmatizer()


class SegmentHelper(object):
    @staticmethod
    def update_probability_dict(dict_file, new_dict_file_list):
        probability_dict = StoreHelper.load_data(dict_file, {})
        for dict_file in new_dict_file_list:
            new_dict = StoreHelper.load_data(dict_file, {})
            print ("Get %s with records: %i" % (dict_file, len(new_dict)))
            DictHelper.update_dict(probability_dict, new_dict)
        StoreHelper.store_data(probability_dict, dict_file)

    @staticmethod
    def segment_text(text):
        """Return a list of words that is the best segmentation of `text`."""
        # remove characters \ and .
        text = re.sub(r'\\|\.', '', text)
        # remove unicode characters
        text = text.decode('unicode_escape').encode('ascii', 'ignore')

        # split words
        return re.split(r'[^a-zA-Z0-9-+\']', text)

    @staticmethod
    def lemmatization(word_list):
        print "Before lemmatization", word_list
        new_list = []
        for word in word_list:
            word = word.strip()
            if len(word) > 0 and word != '*':
                new_list.append(lmtzr.lemmatize(word).lower())
        print "After lemmatization", new_list
        return new_list

    @staticmethod
    def generate_probability_dict(file_content_list):
        # statistics single word and continue two words
        single_word_dict = {}
        two_word_dict = {}
        for file_content in file_content_list:
            for line in file_content.splitlines():
                word_list = SegmentHelper.segment_text(line)
                if len(word_list) == 1:
                    DictHelper.increase_dic_key(single_word_dict, word_list[0])
                else:
                    for i in range(len(word_list) - 1):
                        DictHelper.increase_dic_key(single_word_dict, word_list[i])
                        DictHelper.increase_dic_key(two_word_dict, "%s %s" % (word_list[i], word_list[i + 1]))
                    DictHelper.increase_dic_key(single_word_dict, word_list[-1])
        # compute two word probability
        prob_a_b_dict = {}
        for words, count in two_word_dict.items():
            word_a, word_b = words.split(' ')
            pro_a_b = two_word_dict[words] * 1.0 / single_word_dict[word_b];
            pro_b_a = two_word_dict[words] * 1.0 / single_word_dict[word_a];
            prob_a_b_dict[words] = max(pro_a_b, pro_b_a)
        return prob_a_b_dict

    @staticmethod
    def phase_segment(probability_dict, sentence, threshold):
        word_list = SegmentHelper.segment_text(sentence)
        if len(word_list) <= 1:
            return word_list
        word_list.append('')
        phrase_list = []
        phrase = ''
        for i in range(len(word_list) - 1):
            pair = '{0} {1}'.format(word_list[i], word_list[i + 1])
            phrase += word_list[i] if len(phrase) == 0 else ' ' + word_list[i]
            if pair not in probability_dict or probability_dict[pair] < threshold:
                phrase_list.append(phrase)
                phrase = ''
        if len(phrase) > 0:
            phrase_list.append(phrase)
        return phrase_list


if __name__ == '__main__':
    # print SegmentHelper.segment_text("w\tu;hai\nhello")
    # print SegmentHelper.segment_text("wu-hai;feng,df%33+5")
    insert_dict_list = ["../resource/%s_2.dat" % name for name in ('discipline', 'education', 'skills')]
    SegmentHelper.update_probability_dict('../data/probability.dic', insert_dict_list)
    # sentence = "I loves China, it's Beautiful!"
    # word_list = SegmentHelper.segment_text(sentence)
    # print (word_list)
    # word_list = SegmentHelper.lemmatization(word_list)
    # print (word_list)