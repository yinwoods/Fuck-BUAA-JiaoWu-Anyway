# Fuck-BUAA-JiaoWu-Anyway
基于北航辣鸡教务系统定制的各种脚本

### 演示：

演示地址： [http://buaa.yinwoods.com](http://buaa.yinwoods.com)

#### 要解决的依赖：

- python 包有： pymysql flask requests bs4

- 软件有： mysql, tesseract-ocr，其中tesseract-ocr安装教程[http://miphol.com/muse/2013/05/install-tesseract-ocr-on-ubunt.html]

运行 get_courses_schedule 目录下的 database.sql 创建数据库以及数据表

运行 get_courses_schedule 目录下的 main.py 即可输出相应的课表信息

### 使用方法：
	运行 app.py, 通过浏览器访问 http://localhost:5000 即进入系统首页

### 已实现功能：

- 登录

- 生成课表（尝试通过主流课程表APP导入[目前未找到主流课程表APP相应接口]）

- 生成html表格版课程表

- 解决账号/密码错误识别，给出相应提示

- 解决同一时间段内多门课程显示错误的问题

### TODO：

- 生成excel版课程表

- 查看奖助信息

- 填写教评信息

暂时想到的功能就这么多。
