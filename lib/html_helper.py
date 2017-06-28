#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import os
import lxml
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
from lxml.etree import XMLSyntaxError
from store_helper import StoreHelper
from text_helper import TextHelper

cleaner = Cleaner()
cleaner.javascript = True  # This is True because we want to activate the javascript filter
cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter
cleaner.inline_style = True
cleaner.whitelist_tags = set([])
cleaner.remove_tags = ['p', 'ul', 'li', 'b', 'br', 'article', 'div', 'body', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'span']
cleaner.kill_tags = ['footer', 'a', 'noscript', 'header', 'label']


class HTMLHelper(object):
    @staticmethod
    def remove_tag(web_source):
        text = re.sub(r'<[^>]+>', '', web_source)
        return text

    @staticmethod
    def get_text(web_source):
        try:
            _html = lxml.html.document_fromstring(web_source)
        except XMLSyntaxError:
            print ("Exception when convert web source to html document")
            return web_source
        clean_text = lxml.html.tostring(cleaner.clean_html(_html))
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        return os.linesep.join([s for s in clean_text.splitlines() if len(s.strip()) > 0])

    @staticmethod
    def get_company_name(web_source):
        soup = BeautifulSoup(web_source, 'lxml')
        posts = soup.find_all('h4', class_='company')
        return [str(post.contents[0]).strip() for post in posts]

    @staticmethod
    def get_post(web_source):
        if not TextHelper.contain(web_source, 'data scientist'):
            print ("Not contain data scientist")
            return False, None
        soup = BeautifulSoup(web_source, 'lxml')
        # post = soup.find('article', id='jobview') This include header
        # if post is not None:
        #     return True, post
        post = soup.find_all('div', class_='jobview-section')
        if len(post) >= 1:
            if len(post) > 1:
                print ("Too many jobview-section")
            return (True, post[0]) if len(post) == 1 else (False, post[0])
        post = soup.findAll(True, {'class': re.compile('^panel panel-default')})
        if len(post) >= 1:
            if len(post) > 1:
                print ("Too many panel panel-default")
                post = soup.find_all('article', class_='panel panel-default m-job-view panel-body')
                if len(post) == 1:
                    return True, post[0]
                else:
                    print ("Can not solve multi panel")
                    return False, None
            return (True, post[0]) if len(post) == 1 else (False, post[0])
        post = soup.find_all('div', class_='job-show-description-scroller')
        if len(post) >= 1:
            if len(post) > 1:
                print ("Too many job-show-description-scroller")
            return (True, post[0]) if len(post) == 1 else (False, post[0])
        post = soup.find('div', id='details-job-content')
        if post is not None:
            return True, post
        post = soup.find('div', id='jobcopy')
        if post is not None:
            return True, post
        post = soup.find('div', id='bodycol')
        if post is not None:
            return True, post
        post = soup.find('div', id='JobDescription')
        return (True, post) if post is not None else (False, None)

    @staticmethod
    def post_clean(soup_element):
        styles = soup_element.find('style')
        if styles is not None:
            styles.decompose()
        shorts = soup_element.find('div', {'ng-if':'featuredJobModel.showAbstract'})
        if shorts is not None:
            shorts.decompose()
        a_link = soup_element.find('a')
        if a_link is not None:
            a_link.decompose()
        return os.linesep.join([s for s in soup_element.text.splitlines() if len(s.strip()) > 0])


if __name__ == '__main__':
    _html_list = StoreHelper.load_data("../data/post/Delaware.dat", [])
    _web_source = _html_list[4][1]
    print (_html_list[4][0])
    # print(_web_source)
    print (HTMLHelper.get_text(_web_source))
