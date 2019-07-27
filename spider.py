# encoding:UTF-8 

import requests
import bs4

class VGSpider:
    def __init__(self):
        # 新闻类别
        self.category_list = [
            ("国际", "world"),
            ("国内", "domestic"),
            ("经济", "business"),
            ("娱乐", "entertainment"),
            ("体育", "sports"),
            ("科技", "it"),
            ("科学", "science"),
            ("地区", "local")
        ]

    def scrape_news_topics(self, category="world"):
        # 新闻列表页
        url="https://news.yahoo.co.jp/topics/" + category
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text,'lxml')
        li_list = soup("li", "newsFeed_item")

        return [
            (
                li.find("div", "newsFeed_item_title").text,
                li.find("a", "newsFeed_item_link")['href']
            )
            for li in li_list
            if li.find("div", "newsFeed_item_title") is not None and \
                li.find("a", "newsFeed_item_link") is not None
        ]

        
        

# pick up页
# url="https://news.yahoo.co.jp/pickup/6331061"
# data = requests.get(url)
# soup = bs4.BeautifulSoup(data.text,'lxml')
# div = soup.find("div", "news-comment-plugin")
# print(div['data-full-page-url'])

# comment页
# 由于是动态页面，需要模拟ajax
# # 格式：
# 网址："https://news.yahoo.co.jp/comment/plugin/v1/full/"
# 最简参数："keys", "full_page_url", "comment_num"

# 抓取key
# url="https://headlines.yahoo.co.jp/cm/main?d=20190724-00000067-kyodonews-int"
# data = requests.get(url)
# soup = bs4.BeautifulSoup(data.text,'lxml')
# div = soup.find("div", "news-comment-plugin")

# 创建参数包
# parameter = {
#     "keys", div['data-keys'],
#     "full_page_url", url,
#     "comment_num", 20
# }
# url = "https://news.yahoo.co.jp/comment/plugin/v1/full/"
# data = requests.get(url, parameter)
# soup = bs4.BeautifulSoup(data.text,'lxml')
# span_list = soup("span", "cmtBody")
# for span in span_list:
#     print(span.text + '\n')

