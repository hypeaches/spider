# encoding=utf-8

import ssl
import urllib.request


class NovelBBiQuGe:
    @staticmethod
    def init_conf(conf):
        conf.url_index_html_name = ""
        conf.novel_list_string_split = "<dd>"
        conf.novel_list_string_line_startswith = "<a href="

    @staticmethod
    def init_url(url, conf):
        conf.url_index = '{}/'.format(url)
        conf.url_prefix = url

    @staticmethod
    def init_html(url):
        context = ssl.create_default_context()
        urllib.request.urlopen(url, context=context)

    @staticmethod
    def get_novel_list_string_from_html(html):
        html_list_index = html.find('<div id="list">')
        html = html[html_list_index:]
        html_end_index = html.find('</div>')
        html = html[15:html_end_index]
        return html

    @staticmethod
    def split_novel_list_line(line):
        line = line.replace("'", '"')
        name = line.split(">")
        ind = name[1].find("</")
        name = name[1][:ind]
        href = line.split('"')
        href = href[1]
        return [name, href]
