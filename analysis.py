#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from lib.store_helper import StoreHelper
from lib.html_helper import HTMLHelper
from lib.word_frequency import WordFrequency
from lib.position_helper import PositionHelper
from lib.dict_helper import DictHelper
from lib.tfidf import TFIDF
import operator
import os


class Main(object):
    @staticmethod
    def convert_position():
        skills_dict = StoreHelper.load_data("./resource/skills.dat", {})
        discipline_dict = StoreHelper.load_data("./resource/discipline.dat", {})
        education_dict = StoreHelper.load_data("./resource/education.dat", {})
        for i in range(4980):
            text_file = "./data/datascientist/%04d.txt" % i
            word_file = "./data/words/%04d.txt" % i
            context = StoreHelper.read_file(text_file)
            position_helper = PositionHelper(context)
            position_dict_list = position_helper.convert(skills_dict, discipline_dict, education_dict)
            StoreHelper.save_file("\n".join([str(item) for item in position_dict_list]), word_file)

    @staticmethod
    def get_tfidf():
        blob_dict_list = []
        total_dict = {}
        skills_dict = StoreHelper.load_data("./resource/skill.dat", {})
        discipline_dict = StoreHelper.load_data("./resource/discipline.dat", {})
        education_dict = StoreHelper.load_data("./resource/education.dat", {})
        for i in range(4980):
            text_file = "./data/datascientist/%04d.txt" % i
            context = StoreHelper.read_file(text_file)
            position_helper = PositionHelper(context)
            blob_dict_list.append(position_helper.convert(skills_dict, discipline_dict, education_dict)[4])

        tfidf = TFIDF(blob_dict_list)
        for i in range(4980):
            print ("Working on %i article!" % i)
            tf_idf_dict = tfidf.get_tf_idf(blob_dict_list[i])
            # tf_idf_dict = {key: "%.6f" % value for key, value in tf_idf_dict.items()}
            DictHelper.merge_dict(total_dict, tf_idf_dict)
        StoreHelper.store_data(total_dict, "./data/tfidf.dat")

    @staticmethod
    def get_frequency_from_file(file_name):
        _html_list = StoreHelper.load_data(file_name, [])
        _dict = {}
        for _url, _web_source in _html_list:
            clean_content = HTMLHelper.remove_tag(_web_source)
            _dict.update(WordFrequency.get_frequency_dict(clean_content))
        return _dict

    @staticmethod
    def run_script():
        # Step 1, read url from text file
        crawl_dict = StoreHelper.parse_file("./resource/url_list")

        # step 2
        total_dict = {}
        for location, url_list in crawl_dict.items():
            file_name = "./data/post/%s.dat" % location
            print (file_name)
            if StoreHelper.is_file_exist(file_name):
                total_dict.update(Main.get_frequency_from_file(file_name))

        # sort dict
        total_dict = sorted(total_dict.items(), key=operator.itemgetter(1), reverse=True)
        StoreHelper.store_data(total_dict, "word_frequency.dat")

    @staticmethod
    def run_cluster():
        final_vector = [[0 for j in range(310)] for i in range(4980)]
        key_set = StoreHelper.load_data("./resource/feature.dat", {}).keys()
        print("key set length: %i" % len(key_set))

        blob_dict_list = []
        skills_dict = StoreHelper.load_data("./resource/skills.dat", {})
        discipline_dict = StoreHelper.load_data("./resource/discipline.dat", {})
        education_dict = StoreHelper.load_data("./resource/education.dat", {})
        for i in range(4980):
            text_file = "./data/datascientist/%04d.txt" % i
            context = StoreHelper.read_file(text_file)
            position_helper = PositionHelper(context)
            blob_dict_list.append(position_helper.convert(skills_dict, discipline_dict, education_dict)[4])

        tfidf = TFIDF(blob_dict_list)
        for i in range(4980):
            print("Working on %i article!" % i)
            tf_idf_dict = tfidf.get_tf_idf(blob_dict_list[i])
            # tf_idf_dict = {key: "%.6f" % value for key, value in tf_idf_dict.items()}
            for j in range(310):
                if key_set[j] in tf_idf_dict:
                    final_vector[i][j] = tf_idf_dict[key_set[j]]
        StoreHelper.store_data(final_vector, "./data/vectors.dat")

    @staticmethod
    def generate_all_text():
        crawl_dict = StoreHelper.parse_file("./resource/url_list")
        count_numbers = 0
        for location in crawl_dict.keys():
            file_name = "./data/post/%s.dat" % location
            positions = StoreHelper.load_data(file_name, [])
            for url, web_source in positions:
                if 'data scientist' in web_source.lower():
                    text_content = HTMLHelper.get_text(web_source)
                    # text_dict = WordFrequency.get_frequency_dict(text_content)
                    # output = [str(item) for item in text_dict]
                    # output.extend([" ", text_content, " ",  url])
                    StoreHelper.save_file(text_content, "./data/datascientist/%04d.txt" % count_numbers)
                    count_numbers += 1
                else:
                    print ("Data Scientist not found in %s!" % url)


if __name__ == "__main__":
    Main.run_cluster()
    # Main.get_tfidf()
    # data_dict = StoreHelper.load_data('./data/tfidf.dat', {})
    # data_list = DictHelper.get_sorted_list(data_dict)
    # store_str = '\n'.join(["%s:%.6f" % (key, value / 4980) for key, value in data_list])
    # StoreHelper.save_file(store_str, './data/tfidf_average.txt')
