# encoding:UTF-8 

import http.client
import hashlib
import urllib
import random
import json


class VGTranslator:
    appid = '20190831000330830' #你的appid
    secretKey = '9jqwdxw3OHEun1JNZibU' #你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'jp'
    toLang = 'zh'

    def __init__(self):
        pass

    # 翻译单个字符串
    def translate(self, q):
        salt = random.randint(32768, 65536)
        sign = self.appid+q+str(salt)+self.secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode("utf8"))
        sign = m1.hexdigest()
        myurl = self.myurl+'?appid='+self.appid+'&q='+urllib.parse.quote(q)+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(salt)+'&sign='+sign

        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
    
        #response是HTTPResponse对象
        response = httpClient.getresponse()

        return json.loads(response.read().decode('utf-8'))['trans_result'][0]['dst']


    # 翻译字符串列表
    def translate_list(self, q_list):
        # 因为URI长度有限制，所以设置每次请求的条目数
        n = 10
        i = 0
        q = ""
        R = []

        # 根据q_list动态调整n
        max_length = 1000
        def sum(l):
            s = 0
            for i in l:
                s = s + i
            return s
        len_list = [len(q) for q in q_list]
        while(max([sum(len_list[i:i+n]) for i in range(0,len(q_list),n)]) > max_length):
            n = n - 3
        print("request_num:"+str(n))

        # 将q_list转换为一个字符串
        for i in range(len(q_list)):
            q = q + q_list[i] + "\n"

            if((i+1) % n == 0 or i == len(q_list)-1):

                salt = random.randint(32768, 65536)
                sign = self.appid+q+str(salt)+self.secretKey
                m1 = hashlib.md5()
                m1.update(sign.encode("utf8"))
                sign = m1.hexdigest()
                myurl = self.myurl+'?appid='+self.appid+'&q='+urllib.parse.quote(q)+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(salt)+'&sign='+sign

                httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
                httpClient.request('GET', myurl)
            
                #response是HTTPResponse对象
                response = httpClient.getresponse()
                trans_result = json.loads(response.read().decode('utf-8'))['trans_result']

                R = R + [r["dst"] for r in trans_result]
                q = ""

        return R


# 测试代码
if __name__=="__main__":
    t = VGTranslator()
    q = "２９日に発表された統計によると、２０１８年に英国で女の子の赤ちゃんに「アレクサ」という名前を付けた親が、前年に比べて半数以上減ったことが明らかになった。米アマゾン・ドット・コムの音声アシスタントが同名であることが影響した可能性がある。"
    q_list = ["２９日に発表された統計によると", "２０１８年に英国で女の子の赤ちゃんに"]
    print(t.translate_list(q_list))