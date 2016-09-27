# -*- coding: utf-8 -*-

from get_courses_schedule.main import Crawler
from generate_schedule_table import Generate_schedule_table

from flask import Flask
from flask import request, render_template
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__, static_url_path='')

app.debug = True
app.config['SECRET_KEY'] = 'yinwoods'

@app.route('/')
def index():
    loginForm = LoginForm()
    return render_template('index.html', loginForm=loginForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        crawler = Crawler(username, password)
        status_code = crawler.login()

        if status_code == 'FAILED':
            return '<h1>没有该用户或者密码错误!</h1>'
        courses_info = crawler.get_courses_schedule()

        schedule_info = Generate_schedule_table(courses_info).generate()

        print('!!!', schedule_info)

        return render_template('schedule.html', schedule_info=schedule_info, cur_user=username)
    else:
        return '<html><body><h1>请先登录</h1></body></html>'


class LoginForm(Form):
    username = StringField(label='输入用户名：', validators=[DataRequired()])
    password = StringField(label='输入密码：', validators=[DataRequired()])
    rememver_me = BooleanField(label='记住登录', default=False)

if __name__ == '__main__':
    app.run()
