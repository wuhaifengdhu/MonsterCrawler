#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.crawl_helper import CrawlHelper
from lib.store_helper import StoreHelper
from lib.html_helper import HTMLHelper
from lib.segment_helper import SegmentHelper
from lib.dict_helper import DictHelper
from lib.text_helper import TextHelper


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
    def extract_download_data():
        crawl_dict = Main.parse_file("./resource/url_list")
        total_numbers = 0
        for location in crawl_dict.keys():
            file_name = "./data/post/%s.dat" % location
            positions = StoreHelper.load_data(file_name, [])
            print ("Find %i record in %s" % (len(positions), file_name))
            for url, position in positions:
                # step 1, store origin file
                # output1 = "./data/text/%04d.html" % total_numbers
                # StoreHelper.save_file(position, output1)
                output2 = "./data/clean_post_without_header/%04d.dat" % total_numbers
                print ("work on position: %4d" % total_numbers)
                status, content = HTMLHelper.get_post(position)
                if status is False:
                    print ("Error happen on extract %s" % url)
                    # StoreHelper.save_file(position, output2)
                else:
                    StoreHelper.save_file(HTMLHelper.post_clean(content), output2)
                total_numbers += 1
        print ("In summary, total downloaded %i records!" % total_numbers)

    @staticmethod
    def extract_company_name():
        crawl_dict = Main.parse_file("./resource/url_list")
        company_name_dict = {}
        total_numbers = 0
        for location in crawl_dict.keys():
            file_name = "./data/post/%s.dat" % location
            positions = StoreHelper.load_data(file_name, [])
            print ("Find %i record in %s" % (len(positions), file_name))
            for url, position in positions:
                print ("work on position: %4d" % total_numbers)
                company_list = HTMLHelper.get_company_name(position)
                if len(company_list) == 0:
                    print ("Can not found company name in position %d url is %s" % (total_numbers, url))
                elif len(company_list) == 1:
                    company_name_dict[total_numbers] = SegmentHelper.normalize(company_list[0])
                    print ("Found company name %s for position %d" % (company_list[0], total_numbers))
                else:
                    company_name_dict[total_numbers] = SegmentHelper.normalize(company_list[0])
                    print ("Found multi company name %s for position %d (choose the first one)" %(str(company_list), total_numbers))
                total_numbers += 1
        StoreHelper.save_file(company_name_dict, "company_name.txt")
        StoreHelper.store_data(company_name_dict, "company_name.dic")
        print ("In summary, total downloaded %i records!" % total_numbers)

    @staticmethod
    def get_company_rank():
        company_rank_dict = {}
        us_list_company_data_file = './resource/company_list.dat'
        fortune_500_company_data_file = './resource/fortune-500.dat'
        posting_company_data_file = 'company_name.dic'

        posting_company_dict = StoreHelper.load_data(posting_company_data_file, {})
        us_list_company_dict = StoreHelper.load_data(us_list_company_data_file, {})
        fortune_500_company_dict = StoreHelper.load_data(fortune_500_company_data_file, {})

        for company_name in posting_company_dict.values():
            rank = 3  # default normal company
            for company in fortune_500_company_dict:
                if TextHelper.word_in_phrase(company_name, company):
                    rank = 1
            if rank == 3:
                for company in us_list_company_dict:
                    if TextHelper.word_in_phrase(company_name, company):
                        rank = 2
            company_rank_dict[company_name] = rank
        StoreHelper.store_data(company_rank_dict, 'company_rank.dic')
        print (DictHelper.get_sorted_list(company_rank_dict, sorted_by_key=False, reverse=False))

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
    Main.get_company_rank()
