#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from lib.store_helper import StoreHelper
from lib.html_helper import HTMLHelper
from lib.word_frequency import WordFrequency
from lib.position_helper import PositionHelper
from lib.dict_helper import DictHelper
from lib.segment_helper import SegmentHelper
from lib.cluster_helper import ClusterHelper
from lib.tfidf import TFIDF
import operator
import csv
import random


class Main(object):
    @staticmethod
    def convert_position():
        skills_dict = StoreHelper.load_data("./resource/skills.dat", {})
        print ("Get %i words from %s" %(len(skills_dict), "skills dict"))
        discipline_dict = StoreHelper.load_data("./resource/discipline.dat", {})
        print("Get %i words from %s" % (len(discipline_dict), "discipline_dict"))
        education_dict = StoreHelper.load_data("./resource/education.dat", {})
        print("Get %i words from %s" % (len(education_dict), "education_dict"))
        responsibility_dict = StoreHelper.load_data("./resource/responsibility.dat", {})
        print("Get %i words from %s" % (len(responsibility_dict), "responsibility_dict"))
        for i in range(8535):
            text_file = "./data/clean_post_lemmatize/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file):
                print ("working on file %s" % text_file)
                word_list = StoreHelper.load_data("./data/gensim_split/%04d.dat" % i, [])
                word_data = "./data/result_dict/%04d.dat" % i
                word_text = "./data/result_dict/%04d.txt" % i
                context = StoreHelper.read_file(text_file)
                position_helper = PositionHelper(context, word_list)
                result_dict = position_helper.convert(skills_dict, discipline_dict, education_dict, responsibility_dict, './resource/year_convert.dat')
                StoreHelper.save_file(result_dict, word_text)
                StoreHelper.store_data(result_dict, word_data)

    @staticmethod
    def generate_phase_list():
        probability_dict = StoreHelper.load_data('./data/probability.dic', {})
        print ("Get %i dict from file" % len(probability_dict))
        for i in range(8535):
            text_file = "./data/clean_post_lemmatize/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file):
                word_file = "./data/phrase_split/%04d.dat" % i
                context = StoreHelper.read_file(text_file)
                position_helper = PositionHelper(context)
                position_dict_list = position_helper.convert_2(probability_dict)
                StoreHelper.save_file("\n".join([str(item) for item in position_dict_list]), word_file)
            else:
                print ("%s not exist!" % text_file)

    @staticmethod
    def compute_tfidf():
        blob_dict = {}
        total_dict = {}
        probability_dict = StoreHelper.load_data('./data/probability.dic', {})
        print("Get %i dict from file" % len(probability_dict))
        for i in range(8535):
            text_file = "./data/clean_post_lemmatize/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file):
                context = StoreHelper.read_file(text_file)
                position_helper = PositionHelper(context)
                blob_dict[i] = position_helper.convert_2(probability_dict)

        tfidf = TFIDF(blob_dict.values())
        for i in range(8535):
            if i in blob_dict:
                output_file = "./data/tfidf-dat/%04d.dat" % i
                print ("Working on %i article!" % i)
                tf_idf_dict = tfidf.get_tf_idf(blob_dict[i])
                DictHelper.merge_dict(total_dict, tf_idf_dict)
                tf_idf_dict = {key: float("%.6f" % value) for key, value in tf_idf_dict.items()}
                StoreHelper.store_data(tf_idf_dict, output_file)
        StoreHelper.store_data(total_dict, "./data/tfidf.dat")

    @staticmethod
    def generate_blob_list():
        blob_list = []
        for i in range(8535):
            phrase_dict_file = "./data/result_dict/%04d.dat" % i
            text_file = "./data/clean_post_lemmatize/%04d.dat" % i
            if StoreHelper.is_file_exist(phrase_dict_file):
                phrase_dict = StoreHelper.load_data(phrase_dict_file, {})
                text_content = StoreHelper.read_file(text_file)
                word_list = []
                for line in text_content.splitlines():
                    if line.endswith('.'):
                        line = line[:-1]
                    for word in line.split(' '):
                        word_list.append(word)
                for _type in phrase_dict.keys():
                    for words in phrase_dict[_type]:
                        for word in words.split(' '):
                            if word in word_list:
                                word_list.remove(word)
                        word_list.append(words)
                blob_list.append(DictHelper.dict_from_count_list(word_list))
        StoreHelper.store_data(blob_list, './data/blob_list.dat')
        return blob_list

    @staticmethod
    def get_tfidf():
        blob_dict_list = Main.generate_blob_list()
        profile_dict_list = StoreHelper.load_data('./resource/merged_profile.dat', [])
        blob_dict_list.extend(profile_dict_list)
        tfidf = TFIDF(blob_dict_list)
        j = 0
        for i in range(8535):
            text_file = "./data/clean_post_lemmatize/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file):
                print("Working on %s article!" % text_file)
                tf_idf_dict = tfidf.get_tf_idf(blob_dict_list[j])
                StoreHelper.store_data(tf_idf_dict, "./data/tfidf-dat/%04d.dat" % i)
                StoreHelper.save_file(DictHelper.get_sorted_list(tf_idf_dict), "./data/tfidf/%04d.dat" % i)
                j += 1
                # DictHelper.merge_dict(total_dict, tf_idf_dict)
        # StoreHelper.store_data(total_dict, "./data/tfidf.dat")
        # StoreHelper.save_file(DictHelper.get_sorted_list(total_dict), "./data/tfidf.txt")

    @staticmethod
    def get_only_words_in_5():
        for i in range(8535):
            result_dict = {}
            words_dict_file = "./data/result_dict/%04d.dat" % i
            tfidf_dict_file = "./data/tfidf-dat/%04d.dat" % i
            if StoreHelper.is_file_exist(tfidf_dict_file):
                tfidf_dict = StoreHelper.load_data(tfidf_dict_file, {})
                words_dict = StoreHelper.load_data(words_dict_file, {})
                for _type in words_dict.keys():
                    result_dict[_type] = {}
                    for word in words_dict[_type]:
                        if word in tfidf_dict:
                            result_dict[_type][word] = tfidf_dict[word]
                        else:
                            normal_word = SegmentHelper.normalize(word)
                            if normal_word in tfidf_dict:
                                print ("Saved by normalize for %s" % normal_word)
                                result_dict[_type][word] = tfidf_dict[normal_word]
                            else:
                                print ("%s not found in %s" % (word, tfidf_dict_file))
                # for _type in result_dict.keys():
                #     result_dict[_type] = DictHelper.get_sorted_list(result_dict[_type])
                # print (result_dict.keys())
                StoreHelper.store_data(result_dict, "./data/words_only/data/%04d.dat" % i)
                StoreHelper.save_file(result_dict, "./data/words_only/text/%04d.txt" % i)

    @staticmethod
    def get_post_vector():
        year_list = []
        education_list = []
        major_list = []
        skill_list = []
        responsibility_list = []
        position_tfidf_dict = {}
        for i in range(8535):
            phrase_dict_file = "./data/words_only/data/%04d.dat" % i
            if StoreHelper.is_file_exist(phrase_dict_file):
                phrase_dict = StoreHelper.load_data(phrase_dict_file, {})
                position_tfidf_dict[i] = phrase_dict
                if 'working-year' in phrase_dict:
                    year_list.extend(phrase_dict['working-year'].keys())
                if 'education' in phrase_dict:
                    education_list.extend(phrase_dict['education'].keys())
                if 'major' in phrase_dict:
                    major_list.extend(phrase_dict['major'].keys())
                if 'skills' in phrase_dict:
                    skill_list.extend(phrase_dict['skills'].keys())
                if 'responsibility' in phrase_dict:
                    responsibility_list.extend(phrase_dict['responsibility'].keys())
        year_list = list(set(year_list))
        print ("year list count: %d" % len(year_list))
        education_list = list(set(education_list))
        print("education_list list count: %d" % len(education_list))
        major_list = list(set(major_list))
        print("major_list list count: %d" % len(major_list))
        skill_list = list(set(skill_list))
        print("skill_list list count: %d" % len(skill_list))
        responsibility_list = list(set(responsibility_list))
        print("responsibility_list list count: %d" % len(responsibility_list))
        StoreHelper.store_data([year_list, education_list, major_list, skill_list, responsibility_list], 'vector.dat')

        position_vectors = {}
        for i in range(8535):
            if i in position_tfidf_dict:
                position = []
                for word in year_list:
                    position.append(0 if word not in position_tfidf_dict[i]['working-year'] else position_tfidf_dict[i]['working-year'][word])
                for word in education_list:
                    position.append(0 if word not in position_tfidf_dict[i]['education'] else position_tfidf_dict[i]['education'][word])
                for word in major_list:
                    position.append(0 if word not in position_tfidf_dict[i]['major'] else position_tfidf_dict[i]['major'][word])
                for word in skill_list:
                    position.append(0 if word not in position_tfidf_dict[i]['skills'] else position_tfidf_dict[i]['skills'][word])
                for word in responsibility_list:
                    position.append(0 if word not in position_tfidf_dict[i]['responsibility'] else position_tfidf_dict[i]['responsibility'][word])
                position_vectors[i] = position
        StoreHelper.store_data(position_vectors, './data/position_vector_01.dat')

    @staticmethod
    def generate_feature_list():
        vector_data = StoreHelper.load_data('vector.dat', [])
        vector_dict = {'year': vector_data[0], 'education': vector_data[1], 'major': vector_data[2],
                       'skill': vector_data[3], 'responsibility': vector_data[4]}
        StoreHelper.save_file(vector_dict, 'vector.txt')

    @staticmethod
    def generate_csv_file(value_with_01, file_name='feature', select_feature=None):
        vector_list = StoreHelper.load_data('vector.dat', [])
        # Generate csv column
        csv_column = ['cluster_number', 'position_number']
        if select_feature is None:
            for item_list in vector_list:
                for item in item_list:
                    csv_column.append(item)
        else:
            vector_dict = {'working-year': vector_list[0], 'education': vector_list[1], 'major': vector_list[2],
                           'skills': vector_list[3], 'responsibility': vector_list[4]}
            vector_length = [len(item_list) for item_list in vector_list]
            vector_length_dict = {'working-year': (0, sum(vector_length[:1])),
                                  'education': (sum(vector_length[:1]), sum(vector_length[:2])),
                                  'major': (sum(vector_length[:2]), sum(vector_length[:3])),
                                  'skills': (sum(vector_length[:3]), sum(vector_length[:4])),
                                  'responsibility': (sum(vector_length[:4]), sum(vector_length[:5]))}
            start, end = vector_length_dict[select_feature]
            csv_column.extend(vector_dict[select_feature])

        # Generate data
        data_dict = StoreHelper.load_data('./data/position_vector_01.dat', {})
        print ("data_dict row=%d, column=%d" % (len(data_dict), len(data_dict[1])))
        tag_dict = StoreHelper.load_data('position_tag.dat', {})

        # tag dict record {0: [1,4], 2: [2,3]}
        tag_dict = {key: value for key, value in tag_dict.items() if len(value) > 50}
        print ("Tag dict keys after filter: %s" % (str(tag_dict.keys())))
        for key in tag_dict:
            data_column = []
            for number in tag_dict[key]:
                row_value = [int(key), number]
                if select_feature is not None:
                    row_value.extend(data_dict[number][start: end])
                else:
                    row_value.extend(data_dict[number])
                data_column.append(row_value)
            print("data_column row=%d, column=%d" % (len(data_column), len(data_column[1])))
            if select_feature is not None:
                show_vector_list = [vector_dict[select_feature]]
            else:
                show_vector_list = vector_list
            sort_csv_column, sort_data_column = Main.sort_column(csv_column, data_column, show_vector_list, 2, value_with_01)
            print("sort_data_column row=%d, column=%d" % (len(sort_data_column), len(sort_data_column[1])))
            Main.write_list_to_csv('%s_class_%d.csv' % (file_name, key), sort_csv_column, sort_data_column)

    @staticmethod
    def get_0_1_value(value):
        if value > 0:
            return 1
        else:
            return 0

    @staticmethod
    def sort_column(csv_column, data_column, vector_list, start, value_with_01):
        new_csv_column = csv_column[: start]
        # convert to column index
        data_column = [[data_column[i][j] for i in range(len(data_column))] for j in range(len(data_column[0]))]
        for column_list in data_column:
            sum_value = sum([Main.get_0_1_value(value) if value_with_01 else value for value in column_list])
            column_list.insert(0, sum_value)
        new_data_column = data_column[: start]
        for item_list in vector_list:
            origin_data_dict = {}
            print ("Working on area: %s" % csv_column[start: start + len(item_list)])
            for i in range(start, start + len(item_list)):
                tmp_key = data_column[i][0]
                if value_with_01:
                    while tmp_key in origin_data_dict:
                        tmp_key = data_column[i][0] + random.random()
                origin_data_dict[tmp_key] = (csv_column[i], data_column[i])
            sorted_list = DictHelper.get_sorted_list(origin_data_dict, sorted_by_key=True)
            print ("after sort:")
            for sum_value, columns in sorted_list:
                new_csv_column.append(columns[0])
                new_data_column.append(columns[1])
            start += len(item_list)
        # convert back to row indexed
        new_data_column = [[new_data_column[i][j] for i in range(len(new_data_column))] for j in range(len(new_data_column[0]))]
        return new_csv_column, new_data_column

    @staticmethod
    def write_list_to_csv(csv_file, csv_columns, data_list):
        try:
            with open(csv_file, 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(csv_columns)
                for data in data_list:
                    writer.writerow(data)
        except IOError as (error_no, strerror):
            print("I/O error({0}): {1}".format(error_no, strerror))
        return

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

    @staticmethod
    def cluster_with_birch(position_dict=None):
        if position_dict is None:
            position_dict = StoreHelper.load_data("./data/position_vector_01.dat", {})
        _vector_list = position_dict.values()
        _index_list = position_dict.keys()
        ClusterHelper.birch_cluster(_vector_list, _index_list)

    @staticmethod
    def generate_company_list():
        company_name_dict = StoreHelper.load_data('company_name.dic', {})
        company_dict = {}
        for company_name in company_name_dict.values():
            DictHelper.increase_dic_key(company_dict, company_name)
        print ("Totally %d company" % len(company_dict.keys()))
        StoreHelper.save_file(DictHelper.get_sorted_list(company_dict), "company_dict.txt")

    @staticmethod
    def generate_feature_vectors():
        # step 1, generate total dict for each feature
        feature_total_dict = {}
        for i in range(8535):
            result_dict_file = "./data/words_only/data/%04d.dat" % i
            if StoreHelper.is_file_exist(result_dict_file):
                result_dict = StoreHelper.load_data(result_dict_file, {})
                for feature in result_dict:
                    DictHelper.append_dic_key(feature_total_dict, feature, result_dict[feature])

        # step 2, generate feature vector for each feature
        feature_vector_header_dict = {}
        for feature in feature_total_dict:
            feature_list = []
            for words_dict in feature_total_dict[feature]:
                feature_list.extend(words_dict.keys())
            feature_list = list(set(feature_list))
            feature_vector_header_dict[feature] = feature_list
        StoreHelper.store_data(feature_vector_header_dict, 'feature_vector_header.dat')

        # step 3, collect value for each feature vector
        feature_vector_dict = {}
        for feature in feature_vector_header_dict:
            feature_dict = {}
            feature_list = feature_vector_header_dict[feature]
            for i in range(8535):
                result_dict_file = "./data/words_only/data/%04d.dat" % i
                if StoreHelper.is_file_exist(result_dict_file):
                    result_dict = StoreHelper.load_data(result_dict_file, {})
                    feature_dict[i] = [result_dict[feature][words] if words in result_dict[feature] else 0 for words in feature_list]
            feature_vector_dict[feature] = feature_dict
        # print (feature_vector_dict.keys())
        # print (str([len(value[1]) for value in feature_vector_dict.values()]))
        StoreHelper.store_data(feature_vector_dict, 'feature_vector.dat')
        StoreHelper.save_file(feature_vector_dict, 'feature_vector.txt')

    @staticmethod
    def cluster_features():
        feature_vector_dict = StoreHelper.load_data('feature_vector.dat', {})
        for feature in feature_vector_dict:
            print ("Running cluster for %s" % feature)
            Main.cluster_with_birch(feature_vector_dict[feature])
            Main.generate_csv_file(value_with_01=True, file_name=feature, select_feature=feature)

    @staticmethod
    def compute_center_point(exclude_post=[1404, 3721, 4337, 2085, 7246], select_feature=None):
        position_vectors = StoreHelper.load_data('./data/position_vector_01.dat', {})
        for index in exclude_post:
            if index in position_vectors:
                del position_vectors[index]
        vector_list = StoreHelper.load_data('vector.dat', [])

        vector_dict = {'working-year': vector_list[0], 'education': vector_list[1], 'major': vector_list[2],
                       'skills': vector_list[3], 'responsibility': vector_list[4]}
        vector_length = [len(item_list) for item_list in vector_list]
        vector_length_dict = {'working-year': (0, sum(vector_length[:1])),
                              'education': (sum(vector_length[:1]), sum(vector_length[:2])),
                              'major': (sum(vector_length[:2]), sum(vector_length[:3])),
                              'skills': (sum(vector_length[:3]), sum(vector_length[:4])),
                              'responsibility': (sum(vector_length[:4]), sum(vector_length[:5]))}

        csv_index = position_vectors.keys()

        if select_feature is None:
            csv_column = []
            for item_list in vector_list:
                csv_column.extend(item_list)
            csv_data = position_vectors.values()
            csv_file = 'center_point.csv'
        else:
            start, end = vector_length_dict[select_feature]
            csv_column = vector_dict[select_feature]
            csv_data = [position[start: end] for position in position_vectors.values()]
            csv_file = '%s_center_point.csv' % select_feature
        center_point = [0 for i in range(len(csv_column))]
        for position in csv_data:
            for i in range(len(center_point)):
                center_point[i] += position[i]
        center_point = [value / len(position_vectors) for value in center_point]
        print ("Center point: %s" % str(center_point))
        StoreHelper.store_data(center_point, 'center_point.dat')
        center_dict = {csv_column[i]: center_point[i] for i in range(len(csv_column))}
        print (center_dict)
        center_list = DictHelper.get_sorted_list(center_dict, sorted_by_key=False)
        print (center_list)
        Main.write_list_to_csv(csv_file, [pair[0] for pair in center_list], [[pair[1] for pair in center_list]])

        max_distance = (0, 0)
        for i in range(len(csv_data)):
            distance = Main.compute_distance(center_point, csv_data[i])
            if distance > max_distance[1]:
                max_distance = (csv_index[i], distance)
        print("max distance: %s" % str(max_distance))

    @staticmethod
    def compute_distance(vector_a, vector_b):
        if len(vector_a) != len(vector_b):
            print ("Error: vector length do not equal %d compare with %d" % (len(vector_a), len(vector_b)))
            return 0
        cross_sum = a_sum = b_sum = 0
        for i in range(len(vector_a)):
            cross_sum += vector_a[i] * vector_b[i]
            a_sum += vector_a[i] * vector_a[i]
            b_sum += vector_b[i] * vector_b[i]
        if a_sum == 0 or b_sum == 0:
            print ("warn: one of vector is 0")
            return 0
        return cross_sum / ((a_sum * b_sum) ** 0.5)

    @staticmethod
    def generate_cluster_vector():
        # initialize value
        value_with_01 = True

        # step 1, convert position into feature dicts
        # Main.convert_position()

        # step 2, compute tfidf for each position
        # Main.get_tfidf()

        # step 3, filter only contain 5 features words
        # Main.get_only_words_in_5()

        # step 4, generate post vector
        # Main.get_post_vector()

        # step 5, use birch make cluster
        Main.cluster_with_birch()

        # step 6, generate readable csv
        Main.generate_csv_file(value_with_01)

if __name__ == "__main__":
    # Main.generate_feature_vectors()

    # Main.cluster_features()

    Main.compute_center_point(select_feature='responsibility')

    # Main.generate_cluster_vector()

