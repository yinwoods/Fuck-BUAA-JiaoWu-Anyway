from flask import Flask
from get_courses_schedule.main import Crawler
from flask import request, render_template
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__, static_url_path='')

app.debug = True
app.config['SECRET_KEY'] = 'yinwoods'

toolbar = DebugToolbarExtension(app)


@app.route('/')
def index():
    loginForm = LoginForm()
    return render_template('index.html', loginForm=loginForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        print('<html><body><h1>yinwoods</h1></body></html>')

        username = request.form.get('username')
        password = request.form.get('password')

        with open('get_courses_schedule/config.py', 'w') as f:
            f.write('username = \'' + username + '\'\n')
            f.write('password = \'' + password + '\'\n')
        crawler = Crawler()
        crawler.login()
        crawler.get_courses_schedule()
    return '<html><body><h1>hello world</h1></body></html>'

class LoginForm(Form):
    username = StringField(label='输入用户名：', validators=[DataRequired()])
    password = StringField(label='输入密码：', validators=[DataRequired()])
    rememver_me = BooleanField(label='记住登录', default=False)

if __name__ == '__main__':
    app.run()
