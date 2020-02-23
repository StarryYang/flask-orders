#encoding:utf-8
from datetime import datetime

from exts import db
# 用户表设置
class User (db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    # role =1 用户，2商户，3 管理员
    role = db.Column(db.String(20), nullable=False)
    # 默认用户地址，同步设置用户地址的选择id
    address = db.Column(db.String(256),nullable=False)
#     地址管理模型
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    phone= db.Column(db.String(11), nullable=False)
    username =  db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    is_address = db.Column(db.String(2),nullable=False)
    status  = db.Column(db.String(2),nullable=False)
#  菜品分类列表
class Cate(db.Model):
    __tablename__ = 'cate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    num = db.Column(db.String(50), nullable=False)
    des = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(2), nullable=False)