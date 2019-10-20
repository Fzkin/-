# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:09:47 2019

@author: Administrator
"""

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql




def flash_aliply(uid,num,name):
    
# 打开数据库连接
    db = pymysql.connect("localhost","root","dataName","password")
# 使用cursor()方法获取操作游标 
    cursor = db.cursor()
####### SQL 更新语句 #######
    sql = """
    UPDATE friends SET alipay_num = '%s', name = '%s' WHERE  wx_uid = '%s';
            """ % (num, name, uid)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print(1)
    except:
        # 发生错误时回滚
        db.rollback()   
    db.close()   



def flash_friends(uid):
    
# 打开数据库连接
    db = pymysql.connect("localhost","root","dataName","password")
# 使用cursor()方法获取操作游标 
    cursor = db.cursor()
####### SQL 更新语句 #######
#        sql = "UPDATE friends SET wx_name = '%s' WHERE  uid = '%s'" % (name, uid)
    sql = '''
        INSERT INTO friends(wx_uid) VALUES('%s')
          '''%(uid)
#    sql = re.sub('\n','',sql)
    try:
            # 执行SQL语句
        cursor.execute(sql)
            # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()   
    db.close()   

def flash_orders(order_num, order_wx_uid, order_now_time, order_create_time, order_share_pre_fee, order_share_fee, order_return):
    
# 打开数据库连接
    db = pymysql.connect("localhost","root","dataName","password")
# 使用cursor()方法获取操作游标 
    cursor = db.cursor()
####### SQL 更新语句 #######
#        sql = "UPDATE friends SET wx_name = '%s' WHERE  uid = '%s'" % (name, uid)
    sql = '''
        INSERT INTO orders(order_num,order_wx_uid,order_now_time,order_create_time,order_share_pre_fee,order_share_fee,order_return) VALUES('%s','%s','%s','%s',%s,%s,%s)
          '''%(order_num, order_wx_uid, order_now_time, order_create_time, order_share_pre_fee, order_share_fee, order_return)
    print(sql)
#    sql = re.sub('\n','',sql)
    try:
            # 执行SQL语句
        cursor.execute(sql)
            # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()   
    db.close() 


#        order_num varchar(50) PRIMARY KEY,
#        order_wx_uid varchar(50) ,        
#        order_create_time varchar(50),
#        order_share_fee double(5,2),
#        order_share_pre_fee double(5,2),
#        order_return double(5,2),


def orders_find():
    
# 打开数据库连接
    db = pymysql.connect("localhost","root","dataName","password",cursorclass = pymysql.cursors.DictCursor)
# 使用cursor()方法获取操作游标 
    cursor = db.cursor()
####### SQL 更新语句 #######
    sql = """
    select * from orders;
            """ 
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        
        return  cursor.fetchall()
    except:
        # 发生错误时回滚
        db.rollback()   
    db.close()   
    
def search_elem(table,elem = '*',value = '0'):
    
# 打开数据库连接
    db = pymysql.connect("localhost","root","dataName","password",cursorclass = pymysql.cursors.DictCursor)
# 使用cursor()方法获取操作游标 
    cursor = db.cursor()
####### SQL 更新语句 #######
    sql = """
    select %s from %s;
            """ %(elem,table)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        k = []
        b = cursor.fetchall()
        if value == '0':
            return  b
        else:
            for i in range(len(b)):
#                print(i,cursor.fetchall()[i][elem])
                k.append(b[i][elem])
            return  k
    except:
        # 发生错误时回滚
        db.rollback()   
    db.close() 



