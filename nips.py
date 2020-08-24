#coding: utf-8
import requests
from sys import argv
from lxml import etree
from pyquery import PyQuery as pq
import time
import urllib3
urllib3.disable_warnings()

class ips():
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Prototype-Version': '1.7.3',
    'Connection': 'close',
    }
    ip = ""
    cookie = ""
    def __init__(self, ips_ip):
        self.ip = ips_ip

    def get_token_cookie(self):
        url = "https://" + self.ip + "/user/requireLogin"
        res = requests.get(headers = self.header, url = url, verify = False)
        res.encoding="utf-8"
        self.cookie = res.cookies
        dom = etree.HTML(res.text)
        token = dom.xpath('//input[6]/@value')
        return token
        
    def login(self):
        url = "https://" + self.ip + "/user/login"
        token = self.get_token_cookie()
        #抓包将加密后的密码填到下面的password中
        data = {"user[account]":"admin",
                "user[password]":"",
                "lang":"zh_CN",
                "user[token]":token
                }
        res = requests.post(url = url, data = data, cookies = self.cookie, headers = self.header, verify = False)

    def get_data(self):
        header = self.header
        header["Referer"] = "https://" + self.ip + "/ips/event"
        url = "https://" + self.ip + "/ips/eventList/detail/true/dns/true"
        res = requests.get(url = url, headers = header , cookies = self.cookie , verify = False)
        res.encoding="utf-8"
        events = pq(res.text)
        img = events('img').items()
        important = []
        for j in img:
            if "/stylesheet/nsfocus_2012/images/icon/d_" in j.attr('src') :
                important.append(j.attr('title'))
        event1 = events('.even').items()
        event2 = events('.odd').items()
        output = []
        for i1 in event1:
            output.append(i1.text())
        for i2 in event2:
            output.append(i2.text())
        flag = 0

        for out in range(0,10):
            print(output[out].replace("添加例外","").replace("\n"," | "))
            print(output[out+10].replace("添加例外","").replace("\n"," | "))

if __name__ == "__main__":
    ip1 = "10.*.*.1"
    ip2 = "10.*.*.2"
    ip3 = "10.*.*.3"
    a = ips(ip1)
    b = ips(ip2)
    c = ips(ip3)
    a.login()
    b.login()
    c.login()
    while True:
        print("[*]{}".format(ip1))
        a.get_data()
        time.sleep(20)
        print("[*]{}".format(ip2))
        b.get_data()
        time.sleep(20)
        print("[*]{}".format(ip3))
        c.get_data()
        time.sleep(20)