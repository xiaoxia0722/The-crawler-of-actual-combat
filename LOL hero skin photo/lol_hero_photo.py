# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2/25/2020 2:24 PM
# @Author   : XiaoXia
# @Blog     : https://xiaoxiablogs.top
# @File     : lol_hero_photo.py
import datetime

import requests
import simplejson
import os

# lol英雄网站
url_demo = "https://game.gtimg.cn/images/lol/act/img/js/hero/"
# lol英雄列表
hero_list = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
# 设置ua
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
headers = {
	'User-Agent': ua
}


def dirIsExist(dir_name: str):
	"""
	判断文件夹是否存在,不存在则创建
	:param dir_name: 文件夹名称
	"""
	if not os.path.exists("./hero/"):
		os.mkdir("./hero/")
	path = "./hero/{}/".format(dir_name)
	if not os.path.exists(path):
		os.mkdir(path)


def getJson(hero_url: str) -> requests.models.Response:
	"""
	获取json响应
	:param hero_url: 英雄列表的获取链接
	:return:
	"""
	response = requests.get(hero_url)
	return response


def getImagesUrl(hero_id: str) -> list:
	"""
	获取皮肤照片链接
	:param hero_id: 英雄编号
	:return: 皮肤照片数组
	"""
	response = getJson(url_demo + hero_id + ".js")
	images = simplejson.loads(response.text)['skins']
	image_list = []
	'''
	skinId: 图片的编号
	name: 皮肤名称
	mainImg: 图片地址
	'''
	for image in images:
		image_dic = {
			"name": image['name'],
			"url": image['mainImg']
		}
		# 由于其中还有一些炫彩模型，所以要去除掉
		if image_dic['url']:
			image_list.append(image_dic)

	return image_list


def saveImage(url: str, image_name: str, path: str):
	"""
	通过链接获取图片并且将图片保存到相应的目录下
	:param path: 保存目录
	:param image_name: 图片名称
	:param url: 图片地址
	"""
	response = requests.get(url, headers=headers)
	image_path = path + image_name + ".jpg"

	with response:
		# 得到图片的二进制文件
		image_file = response.content
		with open(image_path, "wb+") as f:
			f.write(image_file)
			f.flush()


if __name__ == "__main__":
	# 该语句是用于计算程序运行时间的，不需要可以删除
	start_time = datetime.datetime.now()
	jsons = getJson(hero_list)
	heros = simplejson.loads(jsons.text)["hero"]
	for hero in heros:
		'''
		编号: heroId
		称号: name
		英文名: alias
		中文名: title
		'''
		name = hero['name'] + '-' + hero['title']

		name = name.replace("/", "")
		# 获取每个英雄的皮肤名称及链接列表
		image_lists = getImagesUrl(hero['heroId'])
		# 创建该英雄的文件夹
		dirIsExist(name)
		for img in image_lists:
			# 联盟中有K/DA的皮肤，所以需要将/去掉
			print(img["name"].replace("/", ""))
			saveImage(img['url'], img["name"].replace("/", ""), './hero/{}/'.format(name))
	print("全部爬取完毕")
	# 下面部分是用于计算程序运行时间的，不需要可以删除
	end_time = datetime.datetime.now()
	print("总用时为:", end_time - start_time)
