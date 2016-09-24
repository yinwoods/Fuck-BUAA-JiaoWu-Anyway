#!/usr/bin/python
# -*- encoding: UTF-8 -*-
import os
import re
import string
import subprocess
from collections import namedtuple, defaultdict, OrderedDict

import pymysql
import requests
from bs4 import BeautifulSoup

from get_courses_schedule import config, course_info_filter


class Crawler():


    def __init__(self):

        # 数据库连接
        self.conn = pymysql.connect(host='localhost', user='root', password='root', db='fuck_buaa', charset='utf8')
        self.cursor = self.conn.cursor()

        # 使用代理
        proxies = {
            '1': 'http://111.13.136.46:80',
            '2': 'http://111.11.122.7:80'
        }

        self.cookies = ''
        self.session = requests.Session()
        self.session.proxies.update(proxies)

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "gsmis.graduate.buaa.edu.cn",
            "User-Agent": "Mozilla/5.0(X11;Linuxx86_64) AppleWebKit/537.36(KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36"
        }

    def __del__(self):

        self.cursor.close()
        self.conn.close()
        self.session.close()

    # 获取验证码
    def get_verify_code(self):

        imageUrl = 'http://gsmis.graduate.buaa.edu.cn/gsmis/Image.do'

        res = self.session.get(url=imageUrl, headers=self.headers)
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

    # 过滤验证码， 提高识别率
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
        try:
            return code.group()
        except AttributeError:
            return AttributeError

    # 直到登录成功为止
    def login(self):

        baseUrl = 'http://gsmis.graduate.buaa.edu.cn'
        loginUrl = 'http://gsmis.graduate.buaa.edu.cn/gsmis/indexAction.do'
        imageUrl = baseUrl + '/gsmis/Image.do'


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
            try:
                if len(self.filter_verify_code(verifyCode)) == 4:
                    print('验证码 =', verifyCode)
                    break
            except TypeError:
                self.login()


        data = {
            "id" : config.username,
            "password" : config.password,
            "checkcode" : verifyCode
        }

        self.session.cookies.update(self.cookies)
        response = self.session.post(url=loginUrl, data=data, headers=self.headers)
        if response.text.find('您的位置') != -1:
            print('登录成功')
            return
        else:
            print('验证码错误，尝试再次登入')
            self.login()

    # 获取已选课程信息
    def get_selected_courses(self):
        # 这个辣鸡教务系统登录后一定要访问任意一个二级目录，否则登录信息丢失
        pre_url = 'http://gsmis.graduate.buaa.edu.cn/gsmis/toModule.do?prefix=/py&page=/pySelectCourses.do?do=xsXuanKe'
        response = self.session.get(pre_url, headers=self.headers)

        url = 'http://gsmis.graduate.buaa.edu.cn/gsmis/py/pyYiXuanKeCheng.do'
        response = self.session.get(url=url, headers=self.session.headers)

        # 获取个人的课表信息

        CourseInfo = namedtuple("CourseInfo", "course_id course_name course_attr course_category course_period course_cred")

        html = BeautifulSoup(response.text, 'html.parser')
        trlist = html.find_all(class_="tablefont2")

        # attr:
        # 01 - 公共必修课
        # 0201 - 基础理论课
        # 0202 - 一级学科理论课
        # 0203 - 二级学科理论课

        # 因为这里无法了解所有课程类型的代码
        # 所以创建 defaultdict，当key不存在时，抛出KeyError
        attr_dict = defaultdict(KeyError)
        attr_dict.update({
            '01': '公共必修课',
            '0201': '基础理论课',
            '0202': '一级学科理论课',
            '0203': '二级学科理论课',
        })

        # 保存所有的课程信息并作为函数结果返回
        res = []

        # 这里的 filter 用来滤掉非选课表中的行
        for tr in filter(lambda x: len(x.find_all('td')) == 13, trlist):
            tdlist = tr.find_all('td')

            #TODO KeyError 还未处理
            # 这里的 map 是为了对每个列调用get_text().strip()
            # 利用 namedtuple 的 _make() 函数来保存相应内容
            courseinfo = CourseInfo._make(
                map(lambda x: x.get_text().strip(),
                    (tdlist[1], tdlist[2], tdlist[3], tdlist[5], tdlist[8], tdlist[9])))

            # 利用 attr_dict 替换垃圾信息
            courseinfo = courseinfo._replace(course_attr=attr_dict[re.compile('\d+').search(courseinfo.course_attr).group()])
            res.append(courseinfo._asdict())

        return res

    # 获取北航研究生所有课程信息，并导入数据库
    def save_all_courses_info_to_mysql(self):
        url = 'http://gsmis.graduate.buaa.edu.cn/gsmis/xw/kcbQueryAction.do'

        data = {
            'zdnf': '2016',
            'kkjj': '1',
            'jiaoshi_id': '',
            'kkyx': '',
        }
        response = self.session.post(url=url, data=data, headers=self.headers)
        html = BeautifulSoup(response.text, 'html.parser')
        printTable = html.find(id='printTable')

        # mon, tue, wed, thu, fri, sat, sun
        Week_schedule = namedtuple('Week_schedule', 'mon tue wed thu fri sat sun')
        week_schedule = Week_schedule._make(
            map(lambda x: str(x.select('td')[1]), (printTable.select('tr')[1].select('td > table > tr')[1:])))

        for index, day in enumerate(week_schedule):
            day = re.sub(r'</(.*?)>', '', day)
            day = re.sub(r'<td(.*?)>', '', day)

            for item in day.replace('<br/>', '').split('<br>'):
                cls = course_info_filter.Courses(item)

                try:
                    query = 'INSERT INTO all_courses_info(course_name, course_time, course_place) VALUES (%s, %s, %s)'
                    self.cursor.execute(query, (cls.course_name, '周' + str(index + 1) + '  ' + cls.course_time, cls.course_place, ))
                    self.conn.commit()
                except Exception as exc:
                    print(exc)
                    print(repr(cls))
                    raise Exception

    # 搜索指定课程名称的课程的课程信息
    def search_course(self, course_name):

        course_name = re.sub('--\d$', '', course_name)
        course_name = course_name.replace('--', '-')
        query = 'SELECT course_name, course_time, course_place from all_courses_info where course_name = %s'
        self.cursor.execute(query, (course_name, ))
        self.conn.commit()

        return self.cursor.fetchall()

    # 获取课程表
    def get_courses_schedule(self):
        # 获取所有课程信息并保存到数据库， 仅处理一次
        query = 'SELECT COUNT(*) FROM all_courses_info'
        self.cursor.execute(query)
        self.conn.commit()
        cnt = self.cursor.fetchone()[0]
        if cnt == 0:
            self.save_all_courses_info_to_mysql()

        res_courses_info = []

        # 依次查询已选课表的信息
        res = self.get_selected_courses()
        for item in res:
            courseinfo = OrderedDict(item)
            res = self.search_course((courseinfo['course_name']))

            # 过滤掉对应排课为空的课程信息，例如英语硕免
            for item in res:
                if not len(item) == 0:
                    res_courses_info.append(item)
        return res_courses_info

#TODO: 把verify.jpg 以及 verify.txt保存到tmp目录中

def main():
    crawler =Crawler()
    crawler.login()
    print(crawler.get_courses_schedule())

if __name__ == "__main__":
    main()
