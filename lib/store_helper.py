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

    @staticmethod
    def save_file(data, file_name):
        out = open(file_name, 'wb')
        out.write(data)
        out.close()

    @staticmethod
    def parse_file(file_path):
        url_dict = {}
        with open(file_path) as f:
            content = f.readlines()
        current_key = None
        for line in content:
            if line.startswith("#"):
                current_key = line[1:].replace(" ", "")[:-1]
                url_dict[current_key] = []
            else:
                url_dict[current_key].append(line[:-1])
        return url_dict

    @staticmethod
    def read_file(file_name):
        file_in = open(file_name, 'rb')
        data = file_in.read()
        file_in.close()
        return data


if __name__ == "__main__":
    StoreHelper.store_data({"wu": "haifeng"}, "../data/post/hi.dat")