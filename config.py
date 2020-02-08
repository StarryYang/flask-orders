#encoding:utf-8
# author:yh
# 2020-02-06
# 项目配置文件
# 设置编码语言utf-8

import os
# 开启debug 模式
DEBUG = True
# session秘钥生成
SECTEATE_KEY = os.urandom(24)

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'order'
USERNAME = 'root'
PASSWORD = '12345678'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI