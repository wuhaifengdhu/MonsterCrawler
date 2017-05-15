#!/usr/bin/python
# -*- coding: utf-8 -*-
from gensim.models.phrases import Phraser, Phrases
from gensim.models import word2vec
from store_helper import StoreHelper
from dict_helper import DictHelper
from segment_helper import SegmentHelper
from nltk.corpus import stopwords
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class GensimHelper(object):
    @staticmethod
    def phrase_detection(bi_gram, file_name):
        # sentence_stream = GensimHelper.generate_sentence_stream()
        # StoreHelper.store_data(sentence_stream, 'sentence_stream.dat')
        # sentence_stream = StoreHelper.load_data('sentence_stream.dat', [])
        # phrases = Phrases(sentence_stream, min_count=2, threshold=4)
        # bi_gram = Phraser(phrases)
        # sent = 'Working knowledge of Python, R, SQL, bash scripting, and the Linux operating system.'.split(' ')
        lines = [x for x in StoreHelper.read_file(file_name).splitlines()]
        result = []
        for x in lines:
            for y in SegmentHelper.segment_text(x):
                if len(y) > 0:
                    result.append(y)
        return bi_gram[result]

    @staticmethod
    def generate_sentence_stream():
        sentence_stream = []
        for i in range(8535):
            text_file = "../data/clean_post_without_header/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file):
                print ("Working on %s" % text_file)
                file_content = StoreHelper.read_file(text_file)
                for line in file_content.splitlines():
                    sentence_stream.append([word for word in unicode(line, 'utf-8').lower().split() if word not in stopwords.words('english')])
        return sentence_stream

    @staticmethod
    def generate_phrase_dict():
        phase_dict = {}
        sentence_stream = StoreHelper.load_data('sentence_stream.dat', [])
        phrases = Phrases(sentence_stream, min_count=2, threshold=4)
        bi_gram = Phraser(phrases)
        for i in range(8535):
            text_file = "../data/clean_post_without_header/%04d.dat" % i
            output_file = "../data/gensim_split/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file):
                print ("Working on %s" % text_file)
                phrase_list = GensimHelper.phrase_detection(bi_gram, text_file)
                DictHelper.increase_dic_key(phase_dict, phrase_list)
                StoreHelper.save_file(phrase_list, output_file)
        StoreHelper.store_data(phase_dict, 'phase_dict.dat')
        StoreHelper.save_file(DictHelper.get_sorted_list(phase_dict), 'phase_dict.txt')

    @staticmethod
    def split_dict():
        phase_dict = StoreHelper.load_data("phase_dict.dat", {})
        phase_dict_single = {}
        phase_dict_double = {}
        for key, value in phase_dict.items():
            if '_' in key:
                phase_dict_double[key] = value
            else:
                phase_dict_single[key] = value
        StoreHelper.save_file(DictHelper.get_sorted_list(phase_dict_single), 'phase_dict_single.txt')
        StoreHelper.save_file(DictHelper.get_sorted_list(phase_dict_double), 'phase_dict_double.txt')


if __name__ == '__main__':
    GensimHelper.split_dict()
