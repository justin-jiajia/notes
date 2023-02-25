# Notes

### 介绍
一个小笔记应用。使用Flask编写，[demo](https://notes.hijiajia.xyz/) ，欢迎使用！

### 安装教程
#### 1.安装依赖
```shell
pip install -r requirements.txt
```
#### 2.写.env文件
```shell
vim .env

# secret随机字符，请将“strong string"替换为随机字符
SECRET_KEY=strong string 
# 数据库地址
# MySql: mysql://username:password@host/databasename
# Sqlite: sqlite:////home/ubuntu/notes.db
SQLALCHEMY_DATABASE_URI = sqlite:////home/ubuntu/notes.db
```
#### 3.初始化数据库
```shell
python -m flask initdb
```
#### 4.启动！
##### 通过Gunicorn（仅支持Linux）
```shell
gunicorn -b 0.0.0.0:8010 -w 4 wsgi:app
```
##### 通过内置开发服务器（仅开发！！）
```shell
flask run
```
### 感谢 不分先后
1. Logo来自 [FlatIconDesign](http://flat-icon-design.com/?p=794)
2. CDN使用 [字节跳动静态资源公共库](http://cdn.bytedance.com/)
