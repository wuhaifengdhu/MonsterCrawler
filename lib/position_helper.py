#!/usr/bin/python
# -*- coding: utf-8 -*-
from word_frequency import WordFrequency
from dict_helper import DictHelper
from text_helper import TextHelper


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
        print (year_phase_list)
        print (skill_phase_list)
        print (discipline_phase_list)
        print (education_phase_list)
        self._add_and_remove(year_phase_list)
        self._add_and_remove(skill_phase_list)
        self._add_and_remove(discipline_phase_list)
        self._add_and_remove(education_phase_list)
        return year_phase_list, skill_phase_list, discipline_phase_list, education_phase_list, self.phrase_dict




