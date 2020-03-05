# 爬取糗事百科的最新的段子
网站:<http://www.yicommunity.com/zuixin/>

通过爬虫爬取糗事百科的最新的段子，并将其存储到json文件。

**这次抓取一共有两种方法:**
- lol_hero_photo.py
    - 使用普通方式抓取
    - 抓取时间长
- lol_hero_photo_thread.py
    - 使用多线程进行抓取
    - 抓取时间比普通方法要短很多

> 因为抓取的次数不多，所以就没用使用代理。