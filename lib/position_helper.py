#!/usr/bin/python
# -*- coding: utf-8 -*-
from word_frequency import WordFrequency
from dict_helper import DictHelper
from text_helper import TextHelper
from segment_helper import SegmentHelper
from nltk.corpus import stopwords


class PositionHelper(object):
    def __init__(self, raw_position):
        self.raw_position = raw_position.lower()
        self.phrase_dict = self._generate_single_word_dict()

    def _generate_single_word_dict(self):
        return WordFrequency.get_frequency_dict(self.raw_position)

    def _get_working_year_words(self):
        return TextHelper.get_years_pattern(self.raw_position)

    def _get_skill_words(self, skill_dict):
        return TextHelper.get_dict_pattern(self.raw_position, skill_dict, 5)

    def _get_discipline_words(self, discipline_dict):
        return TextHelper.get_dict_pattern(self.raw_position, discipline_dict, 5)

    def _get_education_words(self, education_dict):
        return TextHelper.get_dict_pattern(self.raw_position, education_dict, 0)

    def _add_and_remove(self, words_list):
        for words in words_list:
            DictHelper.increase_dic_key(self.phrase_dict, words)
            self._count_down_single_word(words)

    def _count_down_single_word(self, words):
        word_list = [word for word in words.split(' ') if len(word) > 0]
        for word in word_list:
            DictHelper.decrease_dic_key(self.phrase_dict, word)

    def convert(self, skill_dict, discipline_dict, education_dict):
        year_phase_list = self._get_working_year_words()
        skill_phase_list = self._get_skill_words(skill_dict)
        discipline_phase_list = self._get_discipline_words(discipline_dict)
        education_phase_list = self._get_education_words(education_dict)
        # print (year_phase_list)
        # print (skill_phase_list)
        # print (discipline_phase_list)
        # print (education_phase_list)
        self._add_and_remove(year_phase_list)
        self._add_and_remove(skill_phase_list)
        self._add_and_remove(discipline_phase_list)
        self._add_and_remove(education_phase_list)
        return year_phase_list, skill_phase_list, discipline_phase_list, education_phase_list, self.phrase_dict

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








