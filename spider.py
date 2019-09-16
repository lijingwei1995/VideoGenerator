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
        t = p.text.replace('\n','')

        # 完整新闻
        p_d = soup.find("p", "tpcNews_detailLink")
        d_url = p_d.find("a")['href']

        if div is None:
            return t, div, d_url
        else:
            return t, div['data-full-page-url'], d_url

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
            "comment_num" : comment_num * 4
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
        for i in range(comment_num * 4):
            if len(comments[i]) <= max_comment_length:
                c.append(comments[i].replace('\n',''))
                a.append(authors[i])

        if(len(c) < comment_num):
            raise Exception("合格评论数不足"+str(comment_num)+"!")

        return c[0:comment_num], a[0:comment_num]
    
    def scrape_news_details(self, url):
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text,'lxml')

        # title
        div = soup.find("div", "hd")
        h1 = div.find("h1")
        # print(h1.text)

        # paragraph
        p = soup.find("div", "paragraph")
        p_list = p.text.replace("\u3000", "").split("\n\n")
        while '' in p_list:
            p_list.remove('')
        # print(p_list)

        # img
        t = soup.find("div", "thumb")
        if(t is None):
            raise Exception("新闻不含图片")
        # img_url = t.find("img")['src']

        full_img_page_url = t.find("a")['href']
        img_data = requests.get(full_img_page_url)
        img_soup = bs4.BeautifulSoup(img_data.text,'lxml')
        li = img_soup.find("li", "mainImgCont")
        img_url = li.find("img")['src']
        # 下载图片
        with open('cache2/img.png','wb') as f:
            f.write(requests.get(img_url).content)

        return h1.text, p_list


# 测试代码
if __name__ == "__main__":
    v = VGSpider()

    url = "https://headlines.yahoo.co.jp/hl?a=20190915-00000056-jij-pol"
    v.scrape_news_details(url)
#     c, a = v.scrape_news_comments(url, 20)
#     print(a)