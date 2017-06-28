#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir, makedirs, path, remove, removedirs
from os.path import isfile, isdir, join
import gzip
import shutil
import os
import re


class SystemHelper(object):
    @staticmethod
    def list_files_in_directory(directory, escape_hidden_file=False, name_suffix=None):
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        if escape_hidden_file:
            files = [f for f in files if not f.startswith('.')]
        if name_suffix is not None:
            name_suffix = name_suffix.lower()
            files = [f for f in files if name_suffix in f.lower()]
        return [join(directory, f) for f in files]

    @staticmethod
    def list_dirs_in_directory(directory, escape_hidden_dir=False):
        dirs = [_dir for _dir in listdir(directory) if isdir(join(directory, _dir))]
        if escape_hidden_dir:
            dirs = [_dir for _dir in dirs if not _dir.startswith('.')]
        return [join(directory, _dir) for _dir in dirs]

    @staticmethod
    def move_to_folder(source, target_folder):
        shutil.move(source, target_folder)

    @staticmethod
    def touch(file_name, times=None):
        with open(file_name, 'a'):
            os.utime(file_name, times)

    @staticmethod
    def delete(file_name):
        if not path.exists(file_name):
            print ("File %s not exist! Ignore delete method!" % file_name)
            return
        if isdir(file_name):
            removedirs(file_name)
        else:
            remove(file_name)

    @staticmethod
    def make_dir(dir_path, delete_if_exist=False):
        if path.exists(dir_path) and isdir(dir_path):
            if delete_if_exist:
                SystemHelper.delete(dir_path)
            else:
                print ("Dir %s exist, ignore create dir" % dir_path)
                return
        makedirs(dir_path)

    @staticmethod
    def unzip_gz_file(gz_file, unzip_to_file):
        file_content = SystemHelper.read_gz_file(gz_file)
        with open(unzip_to_file, 'wb') as f:
            f.write(file_content)

    @staticmethod
    def read_gz_file(gz_file):
        with gzip.open(gz_file, 'rb') as f:
            file_content = f.read()
        return file_content

    @staticmethod
    def append_to_file(file_name, lines):
        # if not path.exists(file_name):
        #     file_handler = open(file_name, 'w+')
        #     file_handler.close()
        with open(file_name, "a") as f:
            f.write(lines)

    @staticmethod
    def copy_to_folder(src, target_folder):
        try:
            shutil.copy(src, target_folder)
        except IOError:
            print ("Do not have create permission for %s" % target_folder)
            raise

    @staticmethod
    def join_path(parent_path, child_path_name, make_path_if_not_exist=True):
        full_path = path.join(parent_path, child_path_name)
        if not path.exists(full_path) and make_path_if_not_exist:
            SystemHelper.make_dir(full_path, delete_if_exist=False)
        return full_path


if __name__ == '__main__':
    _directory = '../resource/United States'
    for sub_dir in SystemHelper.list_dirs_in_directory(_directory, True):
        print (SystemHelper.list_files_in_directory(sub_dir, name_suffix='.xls'))
