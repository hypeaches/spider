import os
import sys
import urllib.request
import zlib


commandline = "http://www.shuquge.com/txt/30668/index.html"


def init_url():
    global commandline
    global index_html
    global novel_prefix

    if len(sys.argv) == 2:
        commandline = sys.argv[1]
    ind = commandline.rfind("index.html")
    if ind >= 0:
        commandline = commandline[:ind]
    ind = commandline.rfind("/")
    if ind >= 0:
        commandline = commandline[:ind]
    index_html = '{}/index.html'.format(commandline)
    novel_prefix = commandline


novel_list = []
index_html = ""
novel_prefix = ""


def init_work_dir():
    global work_dir
    global index_file_path
    global novel_file_path
    global novel_text_file_path
    global current_section_file_path

    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    index_file_path = os.path.join(work_dir, index_file_name)
    novel_file_path = os.path.join(work_dir, novel_file_name)
    novel_text_file_path = os.path.join(work_dir, novel_text_file_name)
    current_section_file_path = os.path.join(work_dir, current_section_file_name)


work_dir = "./novel"
novel_file_name = "novel.txt"
index_file_name = "index.html"
novel_text_file_name = "tmp"
current_section_file_name = "current_section"

index_file_path = ""
novel_file_path = ""
novel_text_file_path = ""
current_section_file_path = ""


def save_novel_index():
    response = urllib.request.urlopen(index_html)
    html = get_decoded_html(response)
    fd = open(index_file_path, mode='w')
    fd.write(html)
    fd.close()


def get_novel_list_table():
    fd = open(index_file_path, mode="r")
    html = fd.read()
    fd.close()
    html_list_index = html.find('class="listmain"')
    html = html[html_list_index:]
    html_list_index = html.find('</dt>')
    html = html[html_list_index + 1:]
    html_list_index = html.find('</dt>')
    html_end_index = html.find('</div>')
    html = html[html_list_index + 5:html_end_index]
    return html


def split_line(line):
    name = line.split(">")
    ind = name[2].find("</")
    name = name[2][:ind]
    href = line.split('"')
    href = href[1]
    return [name, href]


def parse_novel_list():
    global novel_list
    line_list = get_novel_list_table().split("\n")
    for line in line_list:
        line = line.strip(" ")
        if line.startswith("<dd>"):
            splited = split_line(line)
            novel_list.append([splited[0], '{}/{}'.format(novel_prefix, splited[1])])


def get_decoded_html(response):
    info = '{}'.format(response.info())
    ind = info.find('Content-Encoding: gzip')
    if ind >= 0:
        html = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)  # 获取到页面的源代码
        html = html.decode('utf-8', 'ignore')
        return html
    return response.read().decode('utf-8')


def get_novel_text(url):
    response = urllib.request.urlopen(url)
    html = get_decoded_html(response)
    ind = html.find('id="content" class="showtxt"')
    txt = html[ind:]
    ind = txt.find(">")
    txt = txt[ind + 1:]
    ind = txt.find("</div>")
    txt = txt[:ind]
    tmp_file = open(novel_text_file_path, mode='w')
    tmp_file.write(txt)
    tmp_file.close()
    txt = ""
    for line in open(novel_text_file_path):
        line = line.strip(" ")
        line = line.strip("<br/>")
        line = line.strip("&nbsp;")
        if line == "":
            continue
        txt = txt + line
    return txt


def get_current_section():
    section = 0
    try:
        fd = open(current_section_file_path, 'r')
        section = int(fd.read())
        fd.close()
    except FileNotFoundError:
        a = 1
    return section


def set_current_section(section):
    fd = open(current_section_file_path, mode='w')
    fd.write(str(section))
    fd.close()


if __name__ == "__main__":
    init_url()
    init_work_dir()
    save_novel_index()
    parse_novel_list()

    print("总章节数：", len(novel_list))

    section = get_current_section()
    if section == 0:
        novel_file = open(novel_file_path, mode='w')
    else:
        novel_file = open(novel_file_path, mode='a')

    for ind in range(section, len(novel_list)):
        print("正在下载：", novel_list[ind][0])
        # print("正在下载：", novel_list[ind][0], "\t", novel_list[ind][1])
        try:
            novel_text = get_novel_text(novel_list[ind][1])
            novel_file.write(novel_list[ind][0] + "\n")
            novel_file.write(novel_text + "\n")
            set_current_section(ind + 1)
        except urllib.error.HTTPError:
            print("网站禁止继续爬取，请等待一段时间后再试")
            break
    novel_file.close()

