#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path as path
import os
from store_helper import StoreHelper
from segment_helper import SegmentHelper


class LemmatizerHelper(object):
    @staticmethod
    def run_lemmatize(src_folder, dst_folder):
        for i in range(8535):
            input_file = path.join(src_folder, "%04d.dat" % i)
            output_file = path.join(dst_folder, "%04d.dat" % i)
            if StoreHelper.is_file_exist(input_file):
                file_content = StoreHelper.read_file(input_file)
                new_content = [SegmentHelper.normalize(line) for line in file_content.splitlines()]
                StoreHelper.save_file(os.linesep.join(new_content), output_file)
            else:
                print ("%s not exist!" % input_file)


if __name__ == '__main__':
    LemmatizerHelper.run_lemmatize("../data/clean_post_without_header", "../data/clean_post_lemmatize")
