# BUAA-Crawler
北航学生教务系统爬虫接口

### 使用方法：

#### 要解决的依赖：

- python 包有： pymysql flask requests bs4

- 软件有： mysql, tesseract-ocr，其中tesseract-ocr安装教程[http://miphol.com/muse/2013/05/install-tesseract-ocr-on-ubunt.html]

在config中输入变量username、password，并设置为相应的账号密码，例如：

username='ZY1606123'
password='123456'

运行 get_courses_schedule 目录下的 database.sql 创建数据库以及数据表

运行 get_courses_schedule 目录下的 main.py 即可输出相应的课表信息

### 已实现功能：

- 登录

- 生成课表（尝试通过主流课程表APP导入[目前未找到主流课程表APP相应接口]）

### TODO：

- 生成html表格版课程表

- 生成excel版课程表

- 查看奖助信息

- 填写教评信息

暂时想到的功能就这么多。
