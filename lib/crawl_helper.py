#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import requests
import urlparse
from bs4 import BeautifulSoup
from urllib import urlencode
from lib.store_helper import StoreHelper


class CrawlHelper(object):
    @staticmethod
    def extract_job_id_list(web_source):
        job_list = list(set(re.findall('{"@type":"ListItem","position":[0-9]+,"url":"([^"]*)"', web_source)))
        print("Get %i job ids from web source" % len(job_list))
        return job_list

    @staticmethod
    def get_total_items(web_source):
        numbers = re.findall('([0-9]*)[+]? Jobs Found', web_source)
        try:
            return int(numbers[0]) if len(numbers) > 0 else 0  # Default value for total number
        except ValueError:
            return 0

    @staticmethod
    def next_url(current_url):
        url_parts = list(urlparse.urlparse(current_url))
        para_dict = dict(urlparse.parse_qsl(url_parts[4]))
        if 'page' in para_dict:
            para_dict['page'] = str(int(para_dict['page']) + 1)
        else:
            para_dict['page'] = 2
        url_parts[4] = urlencode(para_dict)
        return urlparse.urlunparse(url_parts)

    @staticmethod
    def get_web_source(web_url):
        response = requests.get(web_url)
        print("Get web source from %s" % web_url)
        if response.url != web_url:
            print ("Directed url: %s" % response.url)
        try:
            soup = BeautifulSoup(response.content.decode('utf-8',  'ignore'), 'lxml')
            return soup.prettify().encode('utf-8')
        except UnicodeDecodeError:
            print ("Unicode error happended when crawl %s" % web_url)
            return ""

    @staticmethod
    def get_all_job_url(web_url):
        web_content = CrawlHelper.get_web_source(web_url)
        url_list = CrawlHelper.extract_job_id_list(web_content)
        total_items = CrawlHelper.get_total_items(web_content)
        total_pages = (total_items / 25)
        for i in range(total_pages):
            web_url = CrawlHelper.next_url(web_url)
            url_list.extend(CrawlHelper.extract_job_id_list(CrawlHelper.get_web_source(web_url)))
        return url_list

    @staticmethod
    def get_all_job_post(url_file, post_file):
        post_info_list = []
        for url in StoreHelper.load_data(url_file, {}):
            web_content = CrawlHelper.get_web_source(url)
            post_info_list.append((url, web_content))
        StoreHelper.store_data(post_info_list, post_file)


if __name__ == '__main__':
    pass



