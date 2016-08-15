#!/usr/bin/python
# -*- encoding: UTF-8 -*-
import re
import config
import string
import requests
import subprocess
from PIL import Image
from bs4 import BeautifulSoup
from io import StringIO

class Crawler():


    def __init__(self):
        self.baseUrl = 'http://gsmis.graduate.buaa.edu.cn'
        self.loginUrl = 'http://gsmis.graduate.buaa.edu.cn/gsmis/indexAction.do'
        self.imageUrl = self.baseUrl + '/gsmis/Image.do'


        # 使用代理
        proxies = {
            'http': 'http://218.202.111.10:80',
            'http': 'http://111.11.122.7:80'
        }

        self.cookies = ''
        self.session = requests.Session()
        self.session.proxies.update(proxies)

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep - alive",
            "Host": "gsmis.graduate.buaa.edu.cn",
            "User-Agent": "Mozilla/5.0(X11;Linuxx86_64) AppleWebKit/537.36(KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36"
        }

    def __del__(self):
        pass

    # 获取验证码
    def get_verify_code(self):
        res = self.session.get(url=self.imageUrl, headers=self.headers)
        with open('verify.jpg', 'wb') as f:
            f.write(res.content)

        # 保存此次访问验证码对应的cookie
        self.cookies = res.cookies

        # 使用tesseract来识别验证码, 并保存到verify.txt中
        p = subprocess.Popen(['tesseract', 'verify.jpg', 'verify'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

        # 返回验证码
        with open('verify.txt', 'r') as f:
            return f.read()

    # 过滤验证码
    def filter_verify_code(self, verifyCode):
        # 找出被错误识别为字母的数字

        if len(verifyCode) < 4:
            return verifyCode

        alpha_digit_map = {
                'B': '8',
                'D': '0',
                'E': '6',
                'g': '9',
                'i': '1',
                'I': '1',
                'j': '1',
                'J': '1',
                'm': '11',
                'M': '11',
                'o': '0',
                'O': '0',
                'q': '9',
                'Q': '0',
                's': '5',
                'S': '5',
                'z': '2',
                'Z': '2',
                }

        # 将错误识别的字母替换为相似的数字
        verifyCode.translate(alpha_digit_map)

        # 使用正则表达式匹配4位数字
        regx = re.compile('(\d{4})')
        code = regx.match(verifyCode)
        return code.group()

    # 直到登录成功为止
    def login(self):

        while True:
            # 获取验证码
            verifyCode = self.get_verify_code()

            verifyCode = verifyCode.strip()
            punctuation = string.punctuation + '‘’'
            for cha in punctuation:
                verifyCode = verifyCode.replace(cha, '')
            verifyCode = verifyCode.strip()

            # 验证码始终是四位数，因此过滤掉不符合条件的结果
            # 使用正则表达式来提取4位数字
            if len(self.filter_verify_code(verifyCode)) == 4:
                print('验证码 =', verifyCode)
                break


        data = {
            "id" : config.username,
            "password" : config.password,
            "checkcode" : verifyCode
        }

        self.session.cookies.update(self.cookies)

        response = self.session.post(url=self.loginUrl, data=data, headers=self.headers)
        if response.text.find('您的位置') != -1:
            print('登录成功')
        else:
            self.login()


def main():
    crawler =Crawler()
    crawler.login()

if __name__ == "__main__":
    main()
