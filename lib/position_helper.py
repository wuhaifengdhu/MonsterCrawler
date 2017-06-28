#!/usr/bin/python
# -*- coding: utf-8 -*-
from dict_helper import DictHelper
from text_helper import TextHelper
from store_helper import StoreHelper
from segment_helper import SegmentHelper
from nltk.corpus import stopwords


class PositionHelper(object):
    def __init__(self, raw_position, word_list=[]):
        self.raw_position = raw_position.lower()
        self.word_list = word_list
        self.phrase_dict = DictHelper.dict_from_count_list(self.word_list)
        self.new_words_list = []

    def generate_word_list(self):
        words_list = []
        for line in self.raw_position.splitlines():
            words_list.extend(SegmentHelper.lemmatization(SegmentHelper.segment_text(line)))
        return words_list

    def _get_working_year_words(self, year_convert_file=None):
        year_list = TextHelper.get_years_pattern(self.raw_position)
        if len(year_list) == 0:
            default_year_requirement = "[0]"
            self.new_words_list.append(default_year_requirement)
            year_list = [default_year_requirement]
        elif year_convert_file is not None:
            year_convert_dict = StoreHelper.load_data(year_convert_file, {})
            year_list = [year_convert_dict[item] for item in year_list if item in year_convert_dict]
        return DictHelper.dict_from_count_list(year_list)

    def _get_skill_words(self, skill_dict):
        return TextHelper.get_dict_pattern(self.raw_position, skill_dict)

    def _get_discipline_words(self, discipline_dict):
        discipline_phrase_dict = TextHelper.get_dict_pattern(self.raw_position, discipline_dict)
        return discipline_phrase_dict

    def _get_education_words(self, education_dict):
        education_phrase_dict = TextHelper.get_dict_pattern(self.raw_position, education_dict)
        if len(education_phrase_dict) == 0:
            default_education_requirement = "Bachelor"
            self.new_words_list.append(default_education_requirement)
            return {default_education_requirement: 1}
        else:
            return education_phrase_dict

    def _get_responsibility_words(self, education_dict):
        return TextHelper.get_dict_pattern(self.raw_position, education_dict)

    def _add_and_remove(self, words_dict):
        for words, count in words_dict.items():
            if words in self.phrase_dict:
                if self.phrase_dict[words] < count:
                    DictHelper.increase_dic_key(self.phrase_dict, words, count - self.phrase_dict[words])
                    self._count_down_single_word(words, count - self.phrase_dict[words])
                elif self.phrase_dict[words] > count:
                    print ("Warning: phrase match times little than origin split: %s" % words)
            else:
                DictHelper.increase_dic_key(self.phrase_dict, words, count)
                self._count_down_single_word(words, count)

    def _count_down_single_word(self, words, decrease_value=1):
        word_list = [word for word in words.split(' ') if len(word) > 0]
        for word in word_list:
            DictHelper.decrease_dic_key(self.phrase_dict, word, decrease_value)

    def convert(self, skill_dict, discipline_dict, education_dict, responsibility_dict, year_convert_file):
        year_phase_dict = self._get_working_year_words(year_convert_file)
        skill_phase_dict = self._get_skill_words(skill_dict)
        discipline_phase_dict = self._get_discipline_words(discipline_dict)
        education_phase_dict = self._get_education_words(education_dict)
        responsibility_phase_dict = self._get_responsibility_words(responsibility_dict)
        self._add_and_remove(year_phase_dict)
        self._add_and_remove(skill_phase_dict)
        self._add_and_remove(discipline_phase_dict)
        self._add_and_remove(education_phase_dict)
        self._add_and_remove(responsibility_phase_dict)
        for word in self.new_words_list:
            DictHelper.increase_dic_key(self.phrase_dict, word)
        result_dict = {"education": education_phase_dict.keys(), "major": discipline_phase_dict.keys(),
                       "skills": skill_phase_dict.keys(),
                       "working-year": year_phase_dict.keys(),
                       "responsibility": responsibility_phase_dict.keys()}
        return result_dict

    def generate_phrase_dict(self, skill_dict, discipline_dict, education_dict, responsibility_dict):
        self.convert(skill_dict, discipline_dict, education_dict, responsibility_dict, None)
        return self.phrase_dict

    def convert_2(self, probability_dict):
        year_phase_list = self._get_working_year_words()
        phrase_list = self._remove_conjunction_segment(probability_dict)
        phrase_list.extend(year_phase_list)
        return DictHelper.dict_from_count_list(phrase_list)

    def _remove_conjunction_segment(self, probability_dict):
        phase_list = []
        sentence_list = []
        word_list = SegmentHelper.segment_text(self.raw_position)
        word_group = []
        for word in word_list:
            if word in stopwords.words('english'):
                if len(word_group) > 0:
                    sentence_list.append(' '.join(word_group))
                    word_group = []
            else:
                word_group.append(word)
        if len(word_group) > 0:
            sentence_list.append(' '.join(word_group))
        for sentence in sentence_list:
            phase_list.extend(SegmentHelper.phase_segment(probability_dict, sentence, 0.05))
        return phase_list


if __name__ == '__main__':
    year_convert = StoreHelper.load_data('../resource/year_convert.dat', {})
    print year_convert['four year']







