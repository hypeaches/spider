# encoding=utf-8


class NovelShuQuGe:
    @staticmethod
    def init_conf(conf):
        conf.url_index_html_name = "index.html"
        conf.novel_list_string_split = "\n"
        conf.novel_list_string_line_startswith = "<dd>"

    @staticmethod
    def init_url(url, conf):
        conf.url_index = '{}/{}'.format(url, conf.url_index_html_name)
        conf.url_prefix = url

    @staticmethod
    def init_html(url):
        pass

    @staticmethod
    def get_novel_list_string_from_html(html):
        html_list_index = html.find('class="listmain"')
        html = html[html_list_index:]
        html_list_index = html.find('</dt>')
        html = html[html_list_index + 1:]
        html_list_index = html.find('</dt>')
        html_end_index = html.find('</div>')
        html = html[html_list_index + 5:html_end_index]
        return html

    @staticmethod
    def split_novel_list_line(line):
        name = line.split(">")
        ind = name[2].find("</")
        name = name[2][:ind]
        href = line.split('"')
        href = href[1]
        return [name, href]
