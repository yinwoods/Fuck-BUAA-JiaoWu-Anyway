import config
import string
import requests
import subprocess
from PIL import Image
from bs4 import BeautifulSoup
from io import StringIO
from urllib.request import urlretrieve

class Crawler():

    def __init__(self):
        self.baseUrl = 'http://gsmis.graduate.buaa.edu.cn'
        self.loginUrl = 'http://gsmis.graduate.buaa.edu.cn/gsmis/indexAction.do'
        self.imageUrl = self.baseUrl + '/gsmis/Image.do'

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

    #获取验证码
    def getVerifyCode(self):
        res = self.session.get(url=self.imageUrl, headers=self.headers)
        with open('verify.jpg', 'wb') as f:
            f.write(res.content)

        self.cookies = res.cookies

        p = subprocess.Popen(['tesseract', 'verify.jpg', 'verify'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        with open('verify.txt', 'r') as f:
            return f.read()

    def login(self):

        while True:
            # 获取验证码
            verifyCode = self.getVerifyCode()
            verifyCode = verifyCode.strip(string.punctuation).strip()
            print('verifycode = ', verifyCode)
            print('len(verifycode) = ', len(verifyCode))
            if len(verifyCode) == 4:
                print(verifyCode)
                break


        data = {
            "id" : config.username,
            "password" : config.password,
            "checkcode" : verifyCode
        }

        self.session.cookies.update(self.cookies)

        response = self.session.post(url=self.loginUrl, data=data, headers=self.headers)
        print(response.cookies)
        print(response.text)


def main():
    crawler =Crawler()
    crawler.login()

if __name__ == "__main__":
    main()
