#!/usr/bin/python
# -*- coding: utf-8 -*-
import cPickle as pickle
import os.path


class StoreHelper(object):
    @staticmethod
    def store_data(data, store_file):
        file_handler = open(store_file, 'wb')
        pickle.dump(data, file_handler)
        file_handler.close()

    @staticmethod
    def load_data(store_file, default_value=None):
        try:
            file_handler = open(store_file, 'rb')
            data = pickle.load(file_handler)
            file_handler.close()
            return data
        except IOError:
            if default_value is not None:
                print ("load file %s from disk not found, return default value %s" % (store_file, default_value))
                return default_value
            else:
                print ("load file %s from disk not found" % store_file)
                raise IOError

    @staticmethod
    def is_file_exist(file_path):
        return os.path.exists(file_path)


if __name__ == "__main__":
    StoreHelper.store_data({"wu": "haifeng"}, "../data/post/hi.dat")