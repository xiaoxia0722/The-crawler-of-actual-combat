# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     :  11:44
# @Author   : XiaoXia
# @Blog     : https://xiaoxiablogs.top
# @File     : the_latest_joke.py

import requests
import json
from lxml import etree
from pprint import pprint


def get_response(request_url: str) -> requests.Response:
    """
    请求链接，获取响应
    :param request_url: 请求的地址
    :return: Response
    """
    # 设置ua
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
    headers = {
        'User-Agent': ua
    }
    url_response = requests.get(request_url, headers=headers)
    url_response.encoding = 'utf-8'
    return url_response


def joke_dict(a_response: requests.Response) -> dict:
    """
    获取每个段子的字典
    :param a_response: 响应
    :return: dict
    """
    with a_response:
        div = etree.HTML(a_response.text).xpath("//div[@class='block untagged noline mb15 bs2']")[0]
        # 获取作者
        author = div.xpath("//div[@class='author']/text()")[1].replace("\r\n", "")
        # 获取内容
        joke = div.xpath("//div[@class='content']/text()")[0].replace("\t", "").replace("\r\n", "")
        # 获取喜欢与不喜欢的数量
        like = div.xpath("//li[@class='up']/a/text()")[0]
        dislike = div.xpath("//li[@class='down']/a/text()")[0]
        # 获取评论的数量
        comment = div.xpath("//li[@class='comment']/a/text()")[0]
        # 将段子信息存放到字典中
        return {
            'author': author,
            'joke': joke,
            'like': like,
            'dislike': dislike,
            'comment': comment
        }


def write_in_json(json_str: str, number: int):
    """
    将json字符串写入文件
    :param number: 页码
    :param json_str: 要写入的json字符串
    """
    with open("jokes_{}.json".format(number), 'w+', encoding='utf-8') as f:
        f.write(json_str)


if __name__ == '__main__':
    # 糗事百科网站
    url = "http://www.yicommunity.com/zuixin/"
    # 糗事百科段子详细连接模版
    url_demo = "http://www.yicommunity.com/"
    for i in range(1, 11):
        print(str(i)*20)
        index = "index_{}.html".format(i)
        if i == 1:
            index = "index.html"
        print(url + index)
        response = get_response(url + index)
        joke_list = []
        with response:
            html = etree.HTML(response.text)
            # 获取每个段子的详细链接
            all_div = html.xpath("//div[@class='col1']")[0]
            # 获取每个段子的div
            divs = all_div.xpath("./div/div")[0]
            a_all = divs.xpath("//div[@class='detail']//a/@href")
            for a in a_all:
                response_a = get_response(url_demo + a)
                div_dict = joke_dict(response_a)
                joke_list.append(div_dict)
                pprint(div_dict)
    write_in_json(json.dumps(div_dict), i)

