import re
from collections import namedtuple

class Generate_schedule_table:

    def __init__(self, lst):
        self.schedule_info = list(lst)
        self.Course = namedtuple("Course", 'course_name course_time course_place')

    # 在所有课程信息中，没课的时间段插入空课，方便前台展示
    def insert_null_course(self, res):

        null_course = lambda item, pd: {'weekday': item['weekday'], 'name': '', 'st_pd': pd, 'ed_pd': pd, 'place': '', 'st_ed_weekds': ''}

        # 如果当天没有课，插入12节空课
        for item in res:
            if len(item['courses']) == 0:
                for pd in range(1, 13):
                    item['courses'].append(null_course(item, pd))

        for item in res:

            courses = item['courses']

            # 这一天就一节课的话，添加这节课前和课后的空课即可
            if len(courses) == 1:
                for course in courses:
                    for pd in range(1, int(course['st_pd'])):
                        item['courses'].append(null_course(item, pd))

                    for pd in range(int(course['ed_pd']) + 1, 13):
                        item['courses'].append(null_course(item, pd))
                    break
            else:

                # 待插入的课程信息保存在 to_insert_courses 中
                to_insert_courses = []

                # 补充第一节课之前的所有课程
                course = courses[0]
                for pd in range(1, int(course['st_pd'])):
                    to_insert_courses.append(null_course(item, pd))
                item['courses'].sort(key=lambda x: int(x['st_pd']))

                # 补充多节课之间的空闲课程
                for index, cur_course in enumerate(courses[1:], start=1):
                    if int(cur_course['st_pd']) - int(courses[index - 1]['ed_pd']) > 1:
                        for pd in range(int(courses[index - 1]['ed_pd']) + 1, int(cur_course['st_pd'])):
                            to_insert_courses.append(null_course(item, pd))

                # 补充最后一节课之后的所有课程
                course = courses[-1]
                for pd in range(int(course['ed_pd']) + 1, 13):
                    to_insert_courses.append(null_course(item, pd))

                item['courses'] += to_insert_courses

        for item in res:
            item['courses'].sort(key=lambda x: int(x['st_pd']))
        return res

    # 处理时间上冲突的课程
    def deal_conflict_courses(self, beautify_schedule_info):

        if len(beautify_schedule_info) == 0:
            return beautify_schedule_info

        beautify_schedule_info.sort(key=lambda x: x['weekday'] + x['st_pd'])

        res_schedule_info = []
        res_schedule_info.append(beautify_schedule_info[0])

        for index, cur_course in enumerate(beautify_schedule_info[1:], start=1):
            pre_course = beautify_schedule_info[index - 1]
            if (cur_course['weekday'] == pre_course['weekday'] and
                cur_course['st_pd'] == pre_course['st_pd']):
                res_schedule_info[-1]['name'] += (' / ' + cur_course['name'])
                res_schedule_info[-1]['st_ed_weeks'] += (' / ' + cur_course['st_ed_weeks'])
                res_schedule_info[-1]['ed_pd'] = max(res_schedule_info[-1]['ed_pd'], cur_course['ed_pd'])
            else:
                res_schedule_info.append(cur_course)
        return res_schedule_info

    # TODO 改成 classmethod
    def generate(self):

        beautify_schedule_info = []

        for course in self.schedule_info:
            course = self.Course(*course)

            # 利用正则表达式提取课程的 weekday 以及 上下课时间
            weekday = re.compile(r'周(\d)').search(course.course_time).group(1)
            st_ed_weeks = re.compile(r'\d+周-\d+周').search(course.course_time).group()
            (start_period, end_period) = re.compile(r'(\d+)节-(\d+)节').search(course.course_time).groups()

            # 利用zip封装 keys values
            keys = ('name', 'weekday', 'st_pd', 'ed_pd', 'place', 'st_ed_weeks')
            values = (course.course_name, weekday, start_period, end_period, course.course_place, st_ed_weeks)

            beautify_schedule_info.append(dict(zip(keys, values)))

        beautify_schedule_info = self.deal_conflict_courses(beautify_schedule_info)


        # 创建一个dict，用以保存所有课程信息
        all_weekdays_dicts_list = []
        for i in range(1, 8):
            all_weekdays_dicts_list.append(dict(zip(('weekday', 'courses'), (str(i), []))))

        # 插入现有课程信息
        for item in beautify_schedule_info:
            for week_dict in all_weekdays_dicts_list:
                if item['weekday'] == week_dict['weekday']:
                    week_dict['courses'].append(item)
                    week_dict['courses'].sort(key=lambda x: int(x['st_pd']))

        all_weekdays_dicts_list = self.insert_null_course(all_weekdays_dicts_list)

        weekday_trans_dict = {
            '1' : '周一',
            '2': '周二',
            '3': '周三',
            '4': '周四',
            '5': '周五',
            '6': '周六',
            '7': '周日'
        }

        for week_dict in all_weekdays_dicts_list:
            week_dict['weekday'] = weekday_trans_dict[week_dict['weekday']]

        return all_weekdays_dicts_list

    def __str__(self):
        print(str(self.schedule_info))
        return str(self.schedule_info)

def main():
    param_str = [('中国特色社会主义理论与实践研究-9班', '周5 3周-11周 5节-8节', '主M101'), ('矩阵理论B-2班', '周2 2周-14周 3节-4节', '主M102'), ('矩阵理论B-2班', '周4 2周-14周 3节-4节', '主M102'), ('矩阵理论B-2班 重复', '周4 2周-14周 3节-4节', '主M102'), ('人文专题课：中国绘画艺术欣赏', '周1 9周-14周 5节-8节', '主M102'), ('算法设计与分析', '周2 1周-17周 10节-12节', '主M401'), ('新型计算机网络', '周5 1周-17周 9节-11节', '主M101'), ('程序设计语言原理', '周1 1周-17周 9节-11节', '主M101')]
    cls = Generate_schedule_table(param_str)
    res = cls.generate()
    for item in res:
        for course in item['courses']:
            print(course)

if __name__ == '__main__':
    main()