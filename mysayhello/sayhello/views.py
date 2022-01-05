# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for, render_template
from sayhello import app
from sayhello.forms import HelloForm
from test import connet_database
from datetime import datetime
from sayhello.models import tuple_class


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
