import re
from collections import namedtuple

class Generate_schedule_table:

    def __init__(self, lst):
        self.schedule_info = list(lst)
        self.Course = namedtuple("Course", 'course_name course_time course_place')

    def insert_null_course(self, res):
        for item in res:
            if len(item['courses']) == 0:
                for pd in range(1, 13):
                    item['courses'].append(
                        {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''})

        for item in res:

            courses = item['courses']

            # 这一天就一节课的话
            if len(courses) == 1:
                for course in courses:
                    for pd in range(1, int(course['st_pd'])):
                        item['courses'].append(
                            {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''})

                    for pd in range(int(course['ed_pd']) + 1, 13):
                        item['courses'].append(
                            {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''})
                    break
            else:

                # 待插入的课程信息保存在 to_insert_courses 中
                to_insert_courses = []

                # 补充第一节课之前的所有课程
                course = courses[0]
                for pd in range(1, int(course['st_pd'])):
                    to_insert_courses.append(
                        {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''})
                item['courses'].sort(key=lambda x: int(x['st_pd']))

                # 补充两节课之间的空闲课程
                for index, cur_course in enumerate(courses[1:], start=1):

                    if int(cur_course['st_pd']) - int(courses[index - 1]['ed_pd']) > 1:
                        for pd in range(int(courses[index - 1]['ed_pd']) + 1, int(cur_course['st_pd'])):
                            to_insert_courses.append(
                                {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''})

                # 补充最后一节课之后的所有课程
                course = courses[-1]
                for pd in range(int(course['ed_pd']) + 1, 13):
                    to_insert_courses.append(
                        {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''})

                item['courses'] += to_insert_courses

        for item in res:
            item['courses'].sort(key=lambda x: int(x['st_pd']))

        return res

    # TODO 改成 classmethod
    def generate(self):

        schedule_info = []

        for course in self.schedule_info:
            course = self.Course(*course)

            # 利用正则表达式提取课程的 weekday 以及 上下课时间
            weekday = re.compile(r'周(\d)').search(course.course_time).group(1)
            st_ed_weeks = re.compile(r'\d+周-\d+周').search(course.course_time).group()
            (start_period, end_period) = re.compile(r'(\d+)节-(\d+)节').search(course.course_time).groups()

            # 利用zip封装 keys values
            keys = ('name', 'weekday', 'st_pd', 'ed_pd', 'place', 'st_ed_weekds')
            values = (course.course_name, weekday, start_period, end_period, course.course_place, st_ed_weeks)

            schedule_info.append(dict(zip(keys, values)))

        all_weekday_dicts_list = []
        for i in range(1, 8):
            all_weekday_dicts_list.append(dict(zip(('weekday', 'courses'), (str(i), []))))

        for item in schedule_info:
            for week_dict in all_weekday_dicts_list:
                if item['weekday'] == week_dict['weekday']:
                    week_dict['courses'].append(item)
                    week_dict['courses'].sort(key=lambda x: x['st_pd'])

        all_weekday_dicts_list = self.insert_null_course(all_weekday_dicts_list)


        # TODO 插入在这里
        weekday_trans_dict = {
            '1' : '周一',
            '2': '周二',
            '3': '周三',
            '4': '周四',
            '5': '周五',
            '6': '周六',
            '7': '周日'
        }

        for week_dict in all_weekday_dicts_list:
            week_dict['weekday'] = weekday_trans_dict[week_dict['weekday']]

        return all_weekday_dicts_list

    def __str__(self):
        print(str(self.schedule_info))
        return str(self.schedule_info)

def main():
    param_str = [('中国特色社会主义理论与实践研究-9班', '周5 3周-11周 5节-8节', '主M101'), ('矩阵理论B-2班', '周2 2周-14周 3节-4节', '主M102'), ('矩阵理论B-2班', '周4 2周-14周 3节-4节', '主M102'), ('人文专题课：中国绘画艺术欣赏', '周1 9周-14周 5节-8节', '主M102'), ('算法设计与分析', '周2 1周-17周 9节-11节', '主M401'), ('新型计算机网络', '周5 1周-17周 9节-11节', '主M101'), ('程序设计语言原理', '周1 1周-17周 9节-11节', '主M101')]
    cls = Generate_schedule_table(param_str)
    res = cls.generate()
    for item in res:
        print(res)

if __name__ == '__main__':
    main()