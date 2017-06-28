#!/usr/bin/python
# -*- coding: utf-8 -*-
from system_helper import SystemHelper
from excel_helper import ExcelHelper
from store_helper import StoreHelper
from text_helper import TextHelper
from segment_helper import SegmentHelper
from dict_helper import DictHelper


class ProfileHelper(object):
    @staticmethod
    def generate_excel_list(home_folder):
        excel_list = []
        for sub_dir in SystemHelper.list_dirs_in_directory(home_folder, True):
            excel_list.extend(SystemHelper.list_files_in_directory(sub_dir, name_suffix='.xls'))
        print ("Totally collected %d excel file" % len(excel_list))
        return excel_list

    @staticmethod
    def generate_profile_list(excel_name):
        user_profile_list = []
        _, raw_data = ExcelHelper.read_excel(excel_name, header=None)
        row_number, column_number = raw_data.shape

        for i in range(1, row_number):
            if len(raw_data[i]) < 7:
                continue
            user_profile_list.append(ProfileHelper.generate_vector(raw_data[i]))
        return user_profile_list

    @staticmethod
    def generate_vector(profile_column):
        vector_dict = {'skills': ProfileHelper.generate_skills(profile_column[3]),
                       'education': ProfileHelper.generate_education(profile_column[5])[0],
                       'major': ProfileHelper.generate_education(profile_column[5])[1],
                       'years': ProfileHelper.generate_years(profile_column[6])}
        return vector_dict

    @staticmethod
    def generate_skills(skills_content):
        skill_list = str(skills_content).split('///')
        return [skill for skill in skill_list if len(skill) > 0]

    @staticmethod
    def generate_education(education_content):
        education_list = []
        major_list = []
        for education in str(education_content).split('///'):
            if len(education) == 0:
                continue
            education_detail = education.split('|')
            if len(education_detail) < 2:
                # print ("education detail not complete: %s" % str(education))
                continue
            if ',' in education_detail[1]:
                education_major = education_detail[1].split(',')
            elif '-' in education_detail[1]:
                education_major = education_detail[1].split('-')
            else:
                # print ("education major not complete: %s" % str(education))
                continue
            education_list.append(education_major[0])
            major_list.append(education_major[1])
        return education_list, major_list

    @staticmethod
    def generate_years(works_content):
        year_list = []
        work_list = str(works_content).split('///')
        for work in work_list:
            work_detail = work.split('|')
            if len(work_detail) < 3:
                # print ("work detail not complete: %s" % str(work))
                continue
            year_list.append(work_detail[2])
        return year_list

    @staticmethod
    def calculate_years(profile):
        year_list = []
        for years in profile['years']:
            year_pair = TextHelper.unicode_to_ascii(years).split('-')
            year_pair = [TextHelper.get_year(year_str) for year_str in year_pair]
            year_pair = [year for year in year_pair if year is not None]
            if len(year_pair) == 2:
                try:
                    year_list.append(year_pair[1] - year_pair[0])
                except TypeError:
                    print ("Can not minus between %s" % str(year_pair))
            else:
                print ("can not calculate %s" % str(year_pair))
        return sum(year_list)

    @staticmethod
    def get_years(profile):
        years = ProfileHelper.calculate_years(profile)
        if years == 0:
            return ['[0]']
        elif years <= 2:
            return ['(0, 2]']
        elif years <= 5:
            return ['(2, 5]']
        elif years <= 10:
            return ['(5, 10]']
        elif years <= 15:
            return ['(10, 15]']
        elif years <= 20:
            return ['(15, 20]']
        else:
            return ['(20, 30]']

    @staticmethod
    def get_highest_education(profile, education_phrase_dic, discipline_phrase_dic):
        education_dic = {}
        for i in range(len(profile['education'])):
            education = SegmentHelper.normalize(TextHelper.unicode_to_ascii(profile['education'][i]))
            education_dic[i] = TextHelper.get_dict_pattern(education, education_phrase_dic)
        education_dic = {e_dic.keys()[0]: index for index, e_dic in education_dic.items() if len(e_dic) > 0}
        if 'Doctor' in education_dic:
            return ['Doctor'], [ProfileHelper.get_discipline(profile['major'], education_dic['Doctor'], discipline_phrase_dic)]
        elif 'Master' in education_dic:
            return ['Master'], [ProfileHelper.get_discipline(profile['major'], education_dic['Master'], discipline_phrase_dic)]
        elif 'Bachelor' in education_dic:
            return ['Bachelor'], [ProfileHelper.get_discipline(profile['major'], education_dic['Bachelor'], discipline_phrase_dic)]
        else:
            return [], []

    @staticmethod
    def get_discipline(major_phrase, prefer_index, discipline_phrase_dic):
        prefer_major = major_phrase[prefer_index]
        prefer_major = SegmentHelper.normalize(TextHelper.unicode_to_ascii(prefer_major))
        prefer_major = TextHelper.get_dict_pattern(prefer_major, discipline_phrase_dic)
        if len(prefer_major) == 0:
            print ("prefer major can not found match phrase in dict: %s" % major_phrase[prefer_index])
            prefer_major = ' '.join(major_phrase)
            prefer_major = SegmentHelper.normalize(TextHelper.unicode_to_ascii(prefer_major))
            prefer_major = TextHelper.get_dict_pattern(prefer_major, discipline_phrase_dic)
            if len(prefer_major) == 0:
                print ("Can not found major words: %s" % str(major_phrase))
                return None
        max_length = max([len(key) for key in prefer_major.keys()])
        for major in prefer_major:
            if len(major) == max_length:
                return major

    @staticmethod
    def get_skills(profile, skills_dic, debug=False):
        skill_phrases = ' '.join(profile['skills'])
        skill_phrases = SegmentHelper.normalize(TextHelper.unicode_to_ascii(skill_phrases))
        if debug:
            print ("right after normalize: %s" % skill_phrases)
        skill_phrases_dict = TextHelper.get_dict_pattern(skill_phrases, skills_dic)
        if len(skill_phrases_dict) == 0:
            # print ("can not found skills in %s" % str(skills))
            return []
        else:
            return skill_phrases_dict.keys()

    @staticmethod
    def extract_profile():
        _home_folder = '../resource/United States'
        profile_list = []
        for excel_file in ProfileHelper.generate_excel_list(_home_folder):
            profile_list.extend(ProfileHelper.generate_profile_list(excel_file))
            print ("After merged file(%s) total profile list number is %d" % (excel_file, len(profile_list)))
        StoreHelper.store_data(profile_list, _home_folder + '/profile.dat')
        StoreHelper.save_file(profile_list, _home_folder + '/profile.txt')

    @staticmethod
    def convert_profile():
        education_phrase_dic = StoreHelper.load_data('../resource/education.dat')
        discipline_phrase_dic = StoreHelper.load_data('../resource/discipline.dat')
        skills_dic = StoreHelper.load_data('../resource/skills.dat')

        profile_vectors = StoreHelper.load_data('../resource/United States/profile.dat', [])
        vector_list = []
        for _profile in profile_vectors:
            educations, majors = ProfileHelper.get_highest_education(_profile, education_phrase_dic, discipline_phrase_dic)
            profile_dict = {'skills': ProfileHelper.get_skills(_profile, skills_dic),
                            'years': ProfileHelper.get_years(_profile),
                            'education': educations,
                            'major': majors}
            vector_list.append(profile_dict)
        StoreHelper.store_data(vector_list, '../resource/convert_profile.dat')
        StoreHelper.save_file(vector_list, '../resource/convert_profile.txt')

    @staticmethod
    def merge_dict():
        profile_dict_list = StoreHelper.load_data('../resource/convert_profile.dat', [])
        merged_list = []
        for profile_dict in profile_dict_list:
            merged_dict = {}
            for feature in profile_dict:
                for key in profile_dict[feature]:
                    DictHelper.increase_dic_key(merged_dict, key)
            merged_list.append(merged_dict)
        StoreHelper.store_data(merged_list, '../resource/merged_profile.dat')
        StoreHelper.save_file(merged_list, '../resource/merged_profile.txt')

if __name__ == '__main__':
    # step 1, extract profile from excels
    ProfileHelper.extract_profile()

    # step 2, convert profile according to dict
    # ProfileHelper.convert_profile()

    # step 3, convert dict to fully dict
    # ProfileHelper.merge_dict()