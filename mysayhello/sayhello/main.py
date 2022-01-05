from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import os
import sys
import click
import pymysql
from flask import flash, redirect, url_for, render_template
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from gevent import pywsgi

app = Flask(__name__)
# app = Flask('sayhello')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
bootstrap = Bootstrap(app)
moment = Moment(app)


# -------------------------------------------------

class tuple_class():
    def __init__(self,tuple1):
        self.id = tuple1[0]
        self.name = tuple1[1]
        self.body = tuple1[2]
        self.timestamp = tuple1[3]
# --------------------------------------------------
db_host = "172.23.0.2"
# -----------

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

# -----------------------------------------------------------
class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()
# ----------------------------数据库操作-----------------------------------------
# 创建sayhello数据库
def create_database():
    mydb = pymysql.connect(
    host=db_host,
    user="root",
    passwd="123456"
    )
    mycursor = mydb.cursor()
    try:
        mycursor.execute("DROP DATABASE if exists sayhello")
        print('删除数据库成功')
        mycursor.execute("CREATE DATABASE if not exists sayhello")
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败")
        print(e)


# 连接数据库
def connet_database(host=db_host,user='root',passwd='123456',db='sayhello'):
    connect = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    cur = connect.cursor()
    return connect,cur


# 创建表
def create_table():
    connect,cur = connet_database()
    sql = """
    CREATE TABLE if not exists sayhello(
    msgid INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(30) not null,
    usermsg VARCHAR(255),
    timestamp datetime
    ) 
    """
    try:
        # 执行创建表的sql
        cur.execute(sql)
        print("创建表成功")
    except Exception as e:
        print("创建表失败")
        print(e)
    finally:
        # 关闭连接
        connect.close()


# 插入数据
def insert_msg(name, body, timestamp):
    connect,cur = connet_database()
    mysql_db_name = "sayhello"
    try:
      cur.execute(f'INSERT INTO {mysql_db_name} (username, usermsg, timestamp) VALUES ("{name}","{body}","{timestamp}")')
      # 执行sql语句
      # cur.execute(sql)
      # 执行sql语句
      connect.commit()
      print("数据插入表成功")
    except:
      # 发生错误时回滚
      print("插入失败")
      connect.rollback()
    # 关闭数据库连接
    connect.close()


@app.cli.command()
@click.option('--count', default=1, help='Quantity of messages, default is 1.')
def forge(count):
    """Generate fake messages."""
    """create table."""
    # 创建数据库
    create_database()
    # 创建数据库表
    create_table()
    click.echo('create table.')
    from faker import Faker
    fake = Faker()
    click.echo('Working...')
    for i in range(count):
        name = fake.name(),
        body = fake.sentence(),
        timestamp = fake.date_time_this_year()
        # 数据库插入
        insert_msg(name, body, timestamp)
    click.echo('Created %d fake messages.' % count)


# 插入数据
def insert_msg(name, body):
    connect,cur = connet_database()
    mysql_db_name = "sayhello"
    now_time = datetime.utcnow()
    try:
      cur.execute(f'INSERT INTO {mysql_db_name} (username,usermsg,timestamp) VALUES ("{name}","{body}","{now_time}")')
      # 执行sql语句
      # cur.execute(sql)
      # 执行sql语句
      connect.commit()
      print("插入成功")
    except:
      # 发生错误时回滚
      connect.rollback()
    # 关闭数据库连接
    connect.close()


def search_msg():
    connect,cur = connet_database()
    # cur.execute("SELECT * FROM sayhello")
    cur.execute("SELECT * FROM sayhello ORDER BY  timestamp desc")
    result = cur.fetchall()
    return result

# -----------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        # 重新写插入的
        insert_msg(name, body)

        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))

    # 重新写读数据库
    message = search_msg()
    # print(message)
    messages = []
    for i in range(len(message)):
        my_mesasages = tuple_class(message[i])
        messages.append(my_mesasages)
    # print('--------------')
    # print(messages)
    return render_template('index.html', form=form, messages=messages)


if __name__ == '__main__':


    # app.jinja_env.trim_blocks = True
    # app.jinja_env.lstrip_blocks = True
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
