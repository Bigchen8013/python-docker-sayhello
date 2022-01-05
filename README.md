# python-docker-sayhello

## 一、功能介绍

使用python、mariadb和docker开发一个留言板，用户填写用户名和留言信息即可提交供别人查看。

## 二、程序运行方式

### 1. 创建mariadb容器
```bash
# 获取mariadb最新的镜像
docker pull mariadb

# 创建mariadb的网络层，名字在为mariadb-network
docker network create mariadb-network

#创建mariadb容器,名字为flask-mariadb,登录密码为123456,将本地的3306和docker容器的3306端口进行映射
docker run \
  -d \
  -p 3306:3306 \
  --network mariadb-network \
  --name flask-mariadb \
  --env MARIADB_USER=cxt-user \
  --env MARIADB_ROOT_PASSWORD=123456 \
  --env DB_HOST=mariadb-host \
  mariadb:latest

 查看mariadb容器的IP地址，便于python容器能够连接到mariadb
docker inspect flask-mariadb
将看到的ip地址取出来赋值给python程序中的db_host
```

### 2. 创建python程序镜像
创建Dockfile文件，里面内容可从代码里查看

根据Dockerfile文件创建python镜像, 镜像取名为py39-docker:v1.0.0
```bash
docker build --tag py39-docker:v1.0.0 .
````
python程序的内容在mysayhello文件夹中，主要程序在sayhello文件夹下的main.pywen文件

### 3. 连接两个容器
编写run.sh文件，首先创建初始的假消息，然后运行main.py文件

连接两个容器,创建的新容器名为py-test，对本地5000端口和docker容器的5000端口进行映射
```
docker run \
-d \
-p 5000:5000 \
--name py-test \
--link flask-mariadb \
--network mariadb-network \
py39-docker:v1.0.0
```

## 三、程序运行截图
程序运行后在http://127.0.0.1:5000/进行查看

初始界面，生成一条假消息：
![image](https://github.com/Bigchen8013/python-docker-sayhello/blob/master/images/ini.png)

填写留言信息：
![image](https://github.com/Bigchen8013/python-docker-sayhello/blob/master/images/message.png)

提交留言后：
![image](https://github.com/Bigchen8013/python-docker-sayhello/blob/master/images/submit.png)

提交后的所有信息显示：
![image](https://github.com/Bigchen8013/python-docker-sayhello/blob/master/images/all_result.png)



