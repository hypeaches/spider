# encoding=utf-8

import os
import sys
import urllib.request
import zlib

from conf import Conf
from bbiquge import NovelBBiQuGe
from shuquge import NovelShuQuGe


class MyNovel:
    # 支持从以下来源下载书籍
    from_list = [
        ["www.shuquge.com", NovelShuQuGe()],
        ["www.bbiquge.com", NovelBBiQuGe()]
    ]
    inst = NovelShuQuGe()
    conf = Conf()
    # 小说索引页面的html
    index_html = ""
    # 小说章节
    chapter_text = ""

    def download(self, url, work_dir):
        print("初始化")
        self.init(url, work_dir)
        print("获取索引页面")
        self.get_index_html()
        print("解析索引页面")
        self.parse_novel_list()
        print("开始下载")
        self.get_novel()

    def init(self, url, work_dir):
        self.init_inst(url)
        self.inst.init_conf(self.conf)
        self.init_url(url)
        self.init_work_dir(work_dir)
        self.inst.init_html(url)

    def init_inst(self, url):
        ret = False
        for item in self.from_list:
            if url.find(item[0]) >= 0:
                self.inst = item[1]
                ret = True
        if not ret:
            print("不支持从该网站下载书籍：", url)
            exit(1)

    def init_url(self, url):
        ind = url.rfind(self.conf.url_index_html_name)
        if ind >= 0:
            url = url[:ind]
        ind = url.rfind("/")
        if ind >= 0:
            url = url[:ind]
        self.inst.init_url(url, self.conf)

    def init_work_dir(self, work_dir):
        self.conf.work_dir = work_dir
        self.conf.novel_file_path = os.path.join(self.conf.work_dir, self.conf.novel_file_name)
        self.conf.novel_current_section_file_path = os.path.join(self.conf.work_dir,
                                                                 self.conf.novel_current_section_file_name)
        if not os.path.exists(self.conf.work_dir):
            os.makedirs(self.conf.work_dir)
        self.conf.novel_current_section = self.read_current_section()

    def read_current_section(self):
        section = 0
        try:
            fd = open(self.conf.novel_current_section_file_path, 'r')
            section = int(fd.read())
            fd.close()
        except FileNotFoundError:
            pass
        return section

    def write_current_section(self, section):
        fd = open(self.conf.novel_current_section_file_path, mode='w')
        fd.write(str(section))
        fd.close()

    def get_index_html(self):
        response = urllib.request.urlopen(self.conf.url_index)
        self.index_html = self.decode_html(response)

    def parse_novel_list(self):
        line_list = self.inst.get_novel_list_string_from_html(self.index_html)
        line_list = line_list.split(self.conf.novel_list_string_split)
        for line in line_list:
            line = line.strip(" ")
            if line.startswith(self.conf.novel_list_string_line_startswith):
                split_line = self.inst.split_novel_list_line(line)
                self.conf.novel_index_list.append([split_line[0], '{}/{}'.format(self.conf.url_prefix, split_line[1])])

    def get_novel_text(self, url):
        response = urllib.request.urlopen(url)
        html = self.decode_html(response)
        ind = html.find('id="content"')
        txt = html[ind:]
        ind = txt.find(">")
        txt = txt[ind + 1:]
        ind = txt.find("</div>")
        txt = txt[:ind]
        txt = txt.replace("<br/>", "\n")
        txt = txt.replace("<br />", "\n")
        self.chapter_text = txt
        txt = ""
        chapter_lines = self.chapter_text.split("\n")
        for line in chapter_lines:
            line = line.strip(" ")
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace("\r\n", "")
            line = line.replace("<br/>", "")
            line = line.replace("<br />", "")
            line = line.replace("&nbsp;", "")
            if len(line) == 0:
                continue
            txt = txt + line + "\n"
        return txt

    def get_novel(self):
        novel_file_open_mode = 'a'
        if self.conf.novel_current_section == 0:
            novel_file_open_mode = 'w'

        try:
            novel_file = open(self.conf.novel_file_path, novel_file_open_mode)
            for ind in range(self.conf.novel_current_section, len(self.conf.novel_index_list)):
                print("正在下载:", self.conf.novel_index_list[ind][0])
                novel_text = self.get_novel_text(self.conf.novel_index_list[ind][1])
                novel_file.write(self.conf.novel_index_list[ind][0] + "\n")
                novel_file.write(novel_text)
                self.write_current_section(ind + 1)
        except FileExistsError as err:
            print("异常: FileExistsError")
            print("文件读写失败:", err.filename)
            print("错误码:", err.errno)
            print("args:", err.args)
            exit(1)
        except FileNotFoundError as err:
            print("异常: FileNotFoundError")
            print("文件读写失败:", err.filename)
            print("错误码:", err.errno)
            print("args:", err.args)
            exit(1)
        except urllib.error.HTTPError as err:
            print("下载小说失败:", err.errno, err.args)
        finally:
            novel_file.close()

    @staticmethod
    def decode_html(response):
        info = '{}'.format(response.info())
        ind = info.find('Content-Encoding: gzip')
        if ind >= 0:
            html = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)  # 获取到页面的源代码
            html = html.decode('utf-8', 'ignore')
            return html
        return response.read().decode('gbk')


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("使用方法：")
        print(sys.argv[0], "<index url> [小说保存路径]")
        exit(1)
    index_url = sys.argv[1]
    download_work_dir = "./novel"
    if len(sys.argv) == 3:
        download_work_dir = sys.argv[2]
    if (not index_url.endswith(".html")) and (not index_url.endswith("/")):
        index_url = index_url + "/"
    mn = MyNovel()
    mn.download(index_url, download_work_dir)
    # mn.download("https://www.bbiquge.com/book_110354/", "./novel")
    # mn.download("http://www.shuquge.com/txt/30668/index.html", "./novel")
