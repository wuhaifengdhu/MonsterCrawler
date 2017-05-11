#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path as path
import os
from lib.store_helper import StoreHelper
from lib.segment_helper import SegmentHelper


class DataScientist(object):
    @staticmethod
    def run_script(src_folder, dst_folder, threshold, probability_dict_path=None, generate_dict=True):
        if probability_dict_path is None:
            probability_dict_path = path.join(dst_folder, 'probability.dict')
        if generate_dict is True:
            file_content_list = []
            for i in range(8535):
                input_file = path.join(src_folder, "%04d.dat" % i)
                if StoreHelper.is_file_exist(input_file):
                    file_content_list.append(StoreHelper.read_file(input_file))
                else:
                    print ("%s not exist!" % input_file)
            probability_dict = SegmentHelper.generate_probability_dict(file_content_list)
            StoreHelper.store_data(probability_dict, probability_dict_path)
            print("Finished generate user dict")
        else:
            probability_dict = StoreHelper.load_data(probability_dict_path, {})
            print("Load dict from file, %i records in dict" % len(probability_dict))

        for i in range(8535):
            input_file = path.join(src_folder, "%04d.dat" % i)
            if StoreHelper.is_file_exist(input_file):
                output_file = path.join(dst_folder, "%04d.dat" % i)
                file_content = StoreHelper.read_file(input_file)
                word_list = []
                for line in file_content.splitlines():
                    word_list.extend(SegmentHelper.phase_segment(probability_dict, line, threshold))
                StoreHelper.save_file(os.linesep.join(word_list), output_file)


if __name__ == '__main__':
    DataScientist.run_script('./data/clean_post_lemmatize', './data/phrase_split', 0.05, './data/probability.dic',
                             generate_dict=True)
