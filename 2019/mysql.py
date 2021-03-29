#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Fighter.Yao'
__time__ = '2019/8/14 16:02'

# 导入依赖
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类
Base = declarative_base()

# 定义User对象
class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    age = Column(int(3))
    sex = Column(int(1))


# 初始化数据库链接
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/test')

# 创建DBSession类型
DBSession = sessionmaker(bind=engine)
