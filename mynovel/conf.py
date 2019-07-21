# enconding=utf-8


class Conf:
    # 小说章节索引页面，如：http://www.shuquge.com/txt/30668/index.html
    url_index = ""
    # 小说正文前缀，如：http://www.shuquge.com/txt/30668
    # url_prefix/index.html即为小说正文。
    # 如：http://www.shuquge.com/txt/30668/4791747.html
    url_prefix = ""
    # 索引页面html文件名，inst初始化
    url_index_html_name = ""
    # 小说索引列表，如：
    # [
    #   ["第一章 黄山真君和九洲一号群", "http://www.shuquge.com/txt/30668/4791747.html"],
    #   ["第二章 且待本尊算上一卦", "http://www.shuquge.com/txt/30668/4791748.html"],
    #   ["第三章 一张丹方", "http://www.shuquge.com/txt/30668/4791749.html"]
    # ]
    novel_index_list = []
    # 工作目录
    work_dir = "./novel"
    # 小说文件名
    novel_file_name = "novel.txt"
    # 保存已下载章节的文件名
    novel_current_section_file_name = "current_section"
    # 保存小说的完整路径名，值为：work_dir/novel_file_name
    novel_file_path = ""
    # 保存已下载章节的完整路径名，值为：work_dir/current_section_file_name
    novel_current_section_file_path = ""
    # 当前要下载的小说的索引，下一个将要被下载的章节为：novel_index_list[novel_current_section]
    # 保存在"novel_current_section_file_path"指定的文件中
    novel_current_section = 0
    # inst初始化
    novel_list_string_split = ""
    # inst初始化
    novel_list_string_line_startswith = ""
