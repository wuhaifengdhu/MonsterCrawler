#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
import ntpath
import string
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from lib.store_helper import StoreHelper
from nltk.corpus import stopwords


stemmer = PorterStemmer()


class NltkHelper(object):
    @staticmethod
    def get_tokens(text):
        # remove unicode
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
        lowers = text.lower()
        # remove the punctuation using the character deletion step of translate
        no_punctuation = lowers.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(no_punctuation)
        return tokens

    @staticmethod
    def remove_stopwords(tokens):
        filtered = [w for w in tokens if not w in stopwords.words('english')]
        return filtered

    @staticmethod
    def stem_tokens(tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    @staticmethod
    def tokenize(text):
        tokens = NltkHelper.get_tokens(text)
        stems = NltkHelper.stem_tokens(tokens)
        return stems

    @staticmethod
    def compute_tfidf(token_file_dict):
        tfidf = TfidfVectorizer(tokenizer=NltkHelper.tokenize, stop_words='english')
        tfs = tfidf.fit_transform(token_file_dict)
        return tfidf, tfs

    @staticmethod
    def generate_token_dict(text_file_list):
        token_file_dict = {}
        for text_file in text_file_list:
            file_name = ntpath.basename(text_file)
            if StoreHelper.is_file_exist(text_file):
                file_content = StoreHelper.read_file(text_file)
                lowers = file_content.lower()
                no_punctuation = lowers.translate(None, string.punctuation)
                token_file_dict[file_name] = no_punctuation
        return token_file_dict


if __name__ == '__main__':
    text_file_list = ["../data/clean_post_without_header/%04d.dat" % i for i in range(35)]
    _token_file_dict = NltkHelper.generate_token_dict(text_file_list)
    _tfidf, _tfs = NltkHelper.compute_tfidf(_token_file_dict)
    StoreHelper.store_data(_tfs, "../data/nltk/tfs.dat")
    feature_names = _tfidf.get_feature_names()
    for col in _tfs.nonzero()[1]:
        print feature_names[col], ' - ', _tfs[0, col]
