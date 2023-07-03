#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2016 Arnaud Aliès

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import re

if sys.version_info[0] < 3:
    import urllib2
    import urllib
    import HTMLParser
else:
    import html
    import urllib.request
    import urllib.parse


class GoogleTranslate:
    def __init__(self, proxy=None):
        self.agent = {
            "User-Agent": "Mozilla/4.0 (\
            compatible;\
            MSIE 6.0;\
            Windows NT 5.1;\
            SV1;\
            .NET CLR 1.1.4322;\
            .NET CLR 2.0.50727;\
            .NET CLR 3.0.04506.30\
            )"
        }
        self.proxy = proxy

    def unescape(self, text):
        if sys.version_info[0] < 3:
            parser = HTMLParser.HTMLParser()
        else:
            parser = html
        return parser.unescape(text)

    def translate(self, to_translate, to_language="auto", from_language="auto"):
        """Returns the translation using google translate
        you must shortcut the language you define
        (French = fr, English = en, Spanish = es, etc...)
        if not defined it will detect it or use english by default

        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?
        """
        base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
        if sys.version_info[0] < 3:
            to_translate = urllib.quote_plus(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib2.Request(link, headers=agent)
            raw_data = urllib2.urlopen(request).read()
        else:
            to_translate = urllib.parse.quote(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib.request.Request(link, headers=self.agent)
            if self.proxy:
                request.set_proxy(self.proxy, 'http')
            raw_data = urllib.request.urlopen(request).read()
        data = raw_data.decode("utf-8")
        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        re_result = re.findall(expr, data)
        if len(re_result) == 0:
            result = ""
        else:
            result = self.unescape(re_result[0])
        return result
