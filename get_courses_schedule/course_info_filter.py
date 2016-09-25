import re

class Courses:

    def __init__(self, info):
        self.info = info.strip()

    # 返回一条信息中的课程名称
    @property
    def course_name(self):
        regx = re.compile('《(.*?)》')
        return regx.search(self.info).group(1)

    # 返回一条信息中的上课时间
    @property
    def course_time(self):
        start_pos = self.info.find('》') + 1
        res = self.info[start_pos:].split(' ')[0]

        # 要在第 2n 个 '周'、'节' 字后加两个空格
        cnt1 = cnt2 = 0
        for index, char in enumerate(res):
            if char == '周':
                cnt1 += 1
                if cnt1 % 2 == 0:
                    res = res[0:index] + '周  ' + res[index+1:]

        for index, char in enumerate(res):
            if char == '节':
                cnt2 += 1
                if cnt2 % 2 == 0:
                    res = res[0:index] + '节  ' + res[index + 1:]
        return res.strip()

    # 返回一条信息中的上课地点
    @property
    def course_place(self):
        return ' '.join(self.info.split(' ')[1:])

    def __repr__(self):
        print('-' * 100, end='\n|\t')
        print('原信息：', self.info, end='\n|\t')
        print('课程名称:', self.course_name, end='\n|\t')
        print('上课时间:', self.course_time, end='\n|\t')
        print('上课地点:', self.course_place, end='\n')
        print('-' * 100)
        return ''

def main():
    cls = Courses('[《应用密码学》5周-16周7节-8节 主M404 ')
    print(cls)

if __name__ == '__main__':
    main()