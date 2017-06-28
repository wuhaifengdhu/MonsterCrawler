#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.store_helper import StoreHelper
from lib.dict_helper import DictHelper
from lib.distance_helper import DistanceHelper
from lib.distance_helper import DistanceHelper
from lib.csv_helper import CsvHelper


class Main(object):
    @staticmethod
    def cross():
        profile_list = StoreHelper.load_data('./resource/convert_profile.dat', [])
        position_dict = StoreHelper.load_data("./data/position_vector_01.dat", {})
        print (len(position_dict.values()[0]))
        vector_list = StoreHelper.load_data('vector.dat', [])
        print (sum([len(value) for value in vector_list]))
        vector_dict = {'years': vector_list[0], 'education': vector_list[1], 'major': vector_list[2],
                       'skills': vector_list[3], 'responsibility': vector_list[4]}
        vector_length = [len(item_list) for item_list in vector_list]
        vector_length_dict = {'years': (0, sum(vector_length[:1])),
                              'education': (sum(vector_length[:1]), sum(vector_length[:2])),
                              'major': (sum(vector_length[:2]), sum(vector_length[:3])),
                              'skills': (sum(vector_length[:3]), sum(vector_length[:4])),
                              'responsibility': (sum(vector_length[:4]), sum(vector_length[:5]))}
        position_list = []
        index_dict = {}
        count = 0
        for index, position in position_dict.items():
            index_dict[count] = index
            count += 1
            position_phrase_dict = {}
            for feature in vector_dict:
                start, end = vector_length_dict[feature]
                for i in range(len(vector_dict[feature])):
                    if position[start + i] > 0:
                        DictHelper.append_dic_key(position_phrase_dict, feature, vector_dict[feature][i])
            position_list.append(position_phrase_dict)
        StoreHelper.store_data(index_dict, 'index_dict.dat')
        StoreHelper.store_data(position_list, 'position_list.dat')
        for feature in ['years', 'education', 'major', 'skills']:
            Main.generate_feature_vector(feature, profile_list, position_list)

    @staticmethod
    def generate_profile_position_common():
        print ("step 1, generate common feature")
        common_feature_dict = {}
        for feature in ['years', 'education', 'major', 'skills']:
            common_feature_dict[feature] = StoreHelper.load_data("position_profile_%s.dat" % feature, [])
            print ("%s: %s" % (feature, common_feature_dict[feature]))
            print ("Load %d phrase for %s" % (len(common_feature_dict[feature]), feature))

        print ("step 2, generate vector for post and profile")
        profile_list = StoreHelper.load_data('./resource/convert_profile.dat', [])
        print ("sample: %s" % profile_list[0])
        total_profile = len(profile_list)
        print ("Load %d profile from file" % total_profile)
        position_list = StoreHelper.load_data('position_list.dat', [])
        print ("sample: %s" % position_list[0])
        total_position = len(position_list)
        print ("Load %d position from file" % total_position)

        skills_convert_dict = StoreHelper.load_data('skills_convert_dict.dat', {})
        print ("Load %d skill convert dict from file" % len(skills_convert_dict))

        profile_vector = []
        position_vector = []
        count = 0
        for profile in profile_list:
            print ("Work on profile %d totally %d" % (count, total_profile))
            count += 1
            if 'skills' in profile:
                print ("skills before convert number: %d" % len(profile['skills']))
                new_skill_set = []
                for skill in profile['skills']:
                    if skill in skills_convert_dict:
                        new_skill_set.append(skill)
                profile['skills'] = list(set(new_skill_set))
                print ("skills after convert number: %d" % len(profile['skills']))
                profile_dict = {feature: [] for feature in common_feature_dict.keys()}
            for feature in common_feature_dict:
                if feature in profile:
                    for phrase in common_feature_dict[feature]:
                        profile_dict[feature].append(1 if phrase in profile[feature] else 0)
                else:
                    profile_dict[feature] = [0 for i in range(len(common_feature_dict[feature]))]
            profile_vector.append(profile_dict)

        count = 0
        for position in position_list:
            print ("Work on position %d totally %d" % (count, total_position))
            count += 1
            if 'skills' in position:
                print ("skills before convert number: %d" % len(position['skills']))
                new_skill_set = []
                for skill in position['skills']:
                    if skill in skills_convert_dict:
                        new_skill_set.append(skill)
                position['skills'] = list(set(new_skill_set))
                print ("skills after convert number: %d" % len(position['skills']))
            position_dict = {feature: [] for feature in common_feature_dict.keys()}
            for feature in common_feature_dict:
                if feature in position:
                    for phrase in common_feature_dict[feature]:
                        position_dict[feature].append(1 if phrase in position[feature] else 0)
                else:
                    position_dict[feature] = [0 for i in range(len(common_feature_dict[feature]))]
            position_vector.append(position_dict)

        print ("step 3, store into data file")
        print ("Profile sample: %s" % str(profile_vector[0]))
        print ("Position sample: %s" % str(position_vector[0]))
        StoreHelper.store_data(profile_vector, 'profile_vector_common.dat')
        StoreHelper.store_data(position_vector, 'position_vector_common.dat')

    @staticmethod
    def find_position_candidate(position_index, threshold, feature_weight_dict=None):
        if feature_weight_dict is None:
            feature_weight_dict = {'years': 0.25, 'education': 0.25, 'major': 0.25, 'skills': 0.25}
        profile_vector = StoreHelper.load_data('profile_vector_common.dat', [])
        position_vector = StoreHelper.load_data('position_vector_common.dat', [])
        index_dict = StoreHelper.load_data('index_dict.dat', {})

        if position_index is None:
            max_distance = []
            count = 0
            total_account = len(position_vector)
            for position in position_vector[: 30]:
                print ("total position %d now is %d" % (total_account, count))
                count += 1
                distance_list = [Main.generate_match_ratio(position, profile, feature_weight_dict) for profile in
                                 profile_vector]
                max_distance.append(max(distance_list))
            print (max_distance)
            print ("max distance %f" % max(max_distance))
            print ("Totally %d profile meet requirements" % sum(
                [1 if distance > threshold else 0 for distance in max_distance]))
        else:
            position = position_vector[index_dict[position_index]]
            print ("Position: %s" % str(position))
            distance_list = [Main.generate_match_ratio(position, profile, feature_weight_dict) for profile in profile_vector]
            print (distance_list)
            print ("max distance %f" % max(distance_list))
            print ("Totally %d profile meet requirements" % sum([1 if distance > threshold else 0 for distance in distance_list]))

    @staticmethod
    def generate_cosine_similarity(position, profile, feature_weight_dict):
        position_vector = []
        profile_vector = []
        for feature in feature_weight_dict:
            position_vector.extend(position[feature])
            profile_vector.extend(profile[feature])
        return DistanceHelper.compute_distance(position_vector, profile_vector)

    @staticmethod
    def vector_less_than(vector_a, vector_b):
        if len(vector_b) != len(vector_a):
            print ("Error! year match vector length not equal! %s vs %s" % (str(vector_a), str(vector_b)))
            return 0
        sum_a = 0
        sum_b = 0
        length = len(vector_a)
        for i in range(length - 1, -1, -1):
            sum_a = (sum_a + vector_a[i]) * length
            sum_b = (sum_b + vector_b[i]) * length
        return sum_a <= sum_b

    @staticmethod
    def years_match(vector_position, vector_profile):
        return 1 if Main.vector_less_than(vector_position, vector_profile) else 0

    @staticmethod
    def major_match(vector_position, vector_profile):
        for major in vector_profile:
            if major in vector_position:
                return 1
        return 0

    @staticmethod
    def education_match(vector_position, vector_profile):
        return 1 if Main.vector_less_than(vector_position, vector_profile) else 0

    @staticmethod
    def skills_match(vector_position, vector_profile, match_rate_require=0.8):
        if len(vector_position) != len(vector_profile):
            print ("Error! year match vector length not equal! %s vs %s" % (str(vector_position), str(vector_profile)))
            return 0
        match_rate = sum([vector_position[i] * vector_profile[i] for i in range(len(vector_position))]) / \
                     (sum(vector_position) * 1.0)
        return 1 if match_rate >= match_rate_require else 0

    @staticmethod
    def generate_match_ratio(position, profile, weight_dict=None):

        match_dict = {
            'years': Main.years_match, 'education': Main.education_match, 'major': Main.major_match,
            'skills': Main.skills_match
        }
        match_ratio = 1
        for feature in weight_dict:
            match_ratio *= match_dict[feature](position[feature], profile[feature])
        return match_ratio

    @staticmethod
    def test_average_skills_per_post():
        position_list = StoreHelper.load_data('position_list.dat', [])
        skill_number_list = [len(post['skills']) if 'skills' in post else 0 for post in position_list]
        print (skill_number_list)
        print ("total position number %d, average %f skills per post!" % (
        len(position_list), sum(skill_number_list) * 1.0 / len(position_list)))

    @staticmethod
    def convert_skill_100():
        skills_list = StoreHelper.load_data("position_profile_skills.dat", [])
        skills_convert_dict = {}
        prefered_list = ["analysis", "python", "r", "analytics", "machine learning", "sql", "modeling", "big data",
                         "hadoop", "java", "statistics", "mathematics", "sas", "data mining", "processing", "spark",
                         "security", "visualization", "testing", "c", "access", "optimization", "hive", "integration",
                         "excel", "tableau", "scripting", "development", "scala", "matlab", "linux", "nosql",
                         "management", "intelligence", "aws", "regression", "spss", "pig", "clustering", "saas",
                         "oracle", "go", "physics", "classification", "javascript", "operations research", "mapreduce",
                         "forecasting", "engineering", "powerpoint", "automation", "b2b", "segmentation", "dashboard",
                         "computing", "deep learning", "defense", "unix", "hbase", "d3", "perl", "algorithms",
                         "advertising", "word", "communication", "simulation", "data collection", "hardware", "command",
                         "apache", "troubleshooting", "ruby", "mongodb", "mysql", "probability", "hdfs", "econometrics",
                         "data warehousing", "scrum", "cassandra", "databases", "git", "cluster",
                         "statistical software", "manufacturing", "improvement", "pricing", "data architecture",
                         "critical thinking", "html", "design", "strategy", "fraud", "microsoft office", "teradata",
                         "quality assurance", "data integration", "experimentation", "customer service",
                         "bioinformatics"]
        for key in prefered_list:
            match = False
            if key not in skills_list:
                for skill in skills_list:
                    if key in skill:
                        match = True
                        if skill not in skills_convert_dict:
                            skills_convert_dict[skill] = key
                        else:
                            print ("%s key duplicate" % skill)
                        break
            else:
                match = True
                skills_convert_dict[key] = key
            if not match:
                print (key)
        StoreHelper.store_data(skills_convert_dict, 'skills_convert_dict.dat')
        print (len(skills_convert_dict))

    @staticmethod
    def generate_feature_vector(feature, profile_list, position_list):
        print ("Totally have %d profile" % len(profile_list))
        print ("Totally have %d position post" % len(position_list))

        # step 1, get fully set of this feature
        profile_phrase_list = []
        for profile in profile_list:
            profile_phrase_list.extend(profile[feature])
        profile_phrase_list = list(set(profile_phrase_list))
        print ("Totally get %d words in profile for feature %s" % (len(profile_phrase_list), feature))
        position_phrase_list = []
        for position in position_list:
            if feature in position:
                position_phrase_list.extend(position[feature])
        position_phrase_list = list(set(position_phrase_list))
        print ("Totally get %d words in position for feature %s" % (len(position_phrase_list), feature))

        # step 2, generate full sum
        phrase_list = list(set(profile_phrase_list).union(set(position_phrase_list)))
        print ("Totally get %d words in all for feature %s" % (len(phrase_list), feature))
        StoreHelper.store_data(phrase_list, "position_profile_%s.dat" % feature)

        # step 3, generate sum value
        # profile_sum = [0 for i in range(len(phrase_list))]
        # position_sum = [0 for i in range(len(phrase_list))]
        # for i in range(len(phrase_list)):
        #     for profile in profile_list:
        #         if phrase_list[i] in profile[feature]:
        #             profile_sum[i] += 1
        #     for position in position_list:
        #         if feature in position and phrase_list[i] in position[feature]:
        #             position_sum[i] += 1
        # max_distance = DistanceHelper.compute_distance([i * 1.0 / len(profile_list) for i in profile_sum],
        #                                                [i * 1.0 / len(position_list) for i in position_sum])
        # csv_column = [feature, "total number"]
        # csv_column.extend(phrase_list)
        # csv_data = [["profile", len(profile_list)], ["position", len(position_list)]]
        # csv_data[0].extend([str(i) for i in profile_sum])
        # csv_data[1].extend([str(i) for i in position_sum])
        # CsvHelper.write_list_to_csv("sum_%s.csv" % feature, csv_column, csv_data, sort_data_row=0, escape_first=2,
        #                             append_rows=[['cross distance', max_distance]])


if __name__ == '__main__':
    # Main.generate_profile_position_common()
    _weight_dict = {'years': 0.25, 'education': 0.25, 'major': 0.25, 'skills': 0.25}
    Main.find_position_candidate(None, 0.5, _weight_dict)



