#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.crawl_helper import CrawlHelper
from lib.store_helper import StoreHelper


class Main(object):
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
    def view_downloaded_data():
        crawl_dict = Main.parse_file("./resource/url_list")
        total_numbers = 0
        for location in crawl_dict.keys():
            file_name = "./data/post/%s.dat" % location
            positions = StoreHelper.load_data(file_name, [])
            print ("Find %i record in %s" % (len(positions), file_name))
            total_numbers += len(positions)
        print ("In summary, total downloaded %i records!" % total_numbers)

    @staticmethod
    def run_script():
        # Step 1, read url from text file
        crawl_dict = Main.parse_file("./resource/url_list")
        print crawl_dict

        # step 2, get job post url from web source
        for location, url_list in crawl_dict.items():
            print ("working on %s get job url" % location)
            if StoreHelper.is_file_exist("./data/url/%s.dat" % location):
                print ("File already exist, ignore this steps!")
                continue
            url_set = set()
            for url in url_list:
                _list = CrawlHelper.get_all_job_url(url)
                url_set = url_set.union(set(_list))
            print ("Totally get %i url for %s\n" % (len(url_set), location))
            if len(url_set) > 0:
                StoreHelper.store_data(list(url_set), "./data/url/%s.dat" % location)

        # step 3, get job post according to url
        for location, url_list in crawl_dict.items():
            print ("working on %s get job post information" % location)
            if StoreHelper.is_file_exist("./data/post/%s.dat" % location):
                print ("File already exist, ignore this steps!")
                continue
            CrawlHelper.get_all_job_post("./data/url/%s.dat" % location, "./data/post/%s.dat" % location)


if __name__ == '__main__':
    Main.run_script()