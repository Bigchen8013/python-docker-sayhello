# -*- coding: utf-8 -*-

import click
from pip import main
import pymysql
from sayhello import app
from datetime import datetime

db_host = "172.23.0.2"


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

if __name__ == '__main__':
    # app.run()
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()