#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import os
import lxml
from lxml.html.clean import Cleaner
from lxml.etree import XMLSyntaxError
from store_helper import StoreHelper

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


if __name__ == '__main__':
    _html_list = StoreHelper.load_data("../data/post/Delaware.dat", [])
    _web_source = _html_list[4][1]
    print (_html_list[4][0])
    # print(_web_source)
    print (HTMLHelper.get_text(_web_source))
