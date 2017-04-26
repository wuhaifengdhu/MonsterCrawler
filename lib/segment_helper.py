#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


class SegmentHelper(object):
    @staticmethod
    def segment_text(text):
        """Return a list of words that is the best segmentation of `text`."""
        result = []
        for x in re.split(r'[;, \s&#]', text):
            # Deal with condition digital and letter mix
            y_list = [y for y in re.split(r'([\d%]+)', x) if len(y) > 0]
            result.extend(y_list)
        return result


if __name__ == '__main__':
    print SegmentHelper.segment_text("w\tu;hai\nhello")
    print SegmentHelper.segment_text("wu-hai;feng,df%33+5")