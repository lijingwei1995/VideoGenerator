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
    
    # 新闻列表页
    def scrape_news_topics(self, category="world"):    
        url="https://news.yahoo.co.jp/topics/" + category
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'lxml')
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
    def scrape_news_pickup(self, url):
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text,'lxml')
        p = soup.find("p", "tpcNews_summary")
        # p2 = soup.find("p", "tpcNews_detailLink")
        # return p.text, p2.a['href']

        div = soup.find("div", "news-comment-plugin")

        if div is None:
            return p.text, div
        else:
            return p.text, div['data-full-page-url']

    # comment页
    # 由于是动态页面，需要模拟ajax
    # # 格式：
    # 网址："https://news.yahoo.co.jp/comment/plugin/v1/full/"
    # 最简参数："keys", "full_page_url", "comment_num"
    def scrape_news_comments(self, url, comment_num):
        print(url)
        # 抓取key
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text,'lxml')
        div = soup.find("div", "news-comment-plugin")

        # 创建参数包
        parameter = {
            "keys" : div['data-keys'],
            "full_page_url" : url,
            "comment_num" : comment_num * 2
        }
        url = "https://news.yahoo.co.jp/comment/plugin/v1/full/"
        data = requests.get(url, parameter)
        soup = bs4.BeautifulSoup(data.text,'lxml')
        
        # 生成评论列表
        span_list = soup("span", "cmtBody")
        comments = [span.text for span in span_list]

        # 生成作者列表
        h1_list = soup("h1", "yjxName")
        authors = [h1.text for h1 in h1_list]

        if(len(comments) < comment_num):
            raise Exception("评论数不足"+str(comment_num)+"!")

        # 控制最大评论长度
        max_comment_length = 130
        c = []
        a = []
        for i in range(comment_num * 2):
            if len(comments[i]) <= max_comment_length:
                c.append(comments[i])
                a.append(authors[i])

        if(len(c) < comment_num):
            raise Exception("合格评论数不足"+str(comment_num)+"!")

        return c[0:comment_num], a[0:comment_num]
    

# 测试代码
# if __name__ == "__main__":
#     v = VGSpider()
#     url = "https://headlines.yahoo.co.jp/cm/main?d=20190830-00000119-jij-int"
#     c, a = v.scrape_news_comments(url, 20)
#     print(a)