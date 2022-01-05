import pymysql
from datetime import datetime


# 连接数据库
def connet_database(host="localhost",port=3306,user='root',passwd='123456',db='sayhello',charset='utf8'):
    connect = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cur = connect.cursor()
    return connect,cur


# 创建表
def create_table():
    connect,cur = connet_database()
    sql = """
    CREATE TABLE sayhello(
    msgid INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(30) not null,
    usermsg VARCHAR(255),
    timestamp datetime DEFAULT NULL
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
def insert_msg():
    connect,cur = connet_database()
    # SQL 插入语句
    sql = "INSERT INTO sayhello(username, usermsg, timestamp) VALUES ('%s', '%s', '%s' )" % \
        ('jack','mother fuck', datetime.now())
    try:
      # 执行sql语句
      cur.execute(sql)
      # 执行sql语句
      connect.commit()
      print("插入成功")
    except:
      # 发生错误时回滚
      connect.rollback()
    # 关闭数据库连接
    connect.close()


# 查询数据
def search_msg():
    connect,cur = connet_database()
    cur.execute("SELECT * FROM sayhello")
    result = cur.fetchall()

    for x in result:
        print(x)

