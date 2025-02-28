import time

import mysql.connector
import config.configs as configs

def get_connection():
    mydb = mysql.connector.connect(
        host=configs.mysqlurl,
        user=configs.mysqlaccount,
        password=configs.mysqlpassword,
        database=configs.mysqlname,
        port=configs.mysqlport,
    )
    return mydb


# 连接数据库
def sql_update(sql, val):
    mydb = get_connection()
    # 创建游标对象
    mycursor = mydb.cursor()
    # 修改数据
    mycursor.execute(sql, val)
    # 执行事务
    mydb.commit()
    # 关闭数据库连接
    mycursor.close()
    mydb.close()
def sql_updatenew(sql, val):
    mydb = get_connection()
    # 创建游标对象
    mycursor = mydb.cursor()
    try:
        # 修改数据
        mycursor.execute(sql, val)
        # 获取最后插入的ID
        last_id = mycursor.lastrowid
        # 执行事务
        mydb.commit()
        return last_id
    finally:
        # 关闭数据库连接
        mycursor.close()
        mydb.close()

def sql_select(sql, val):
    mydb = get_connection()
    # 创建游标对象
    mycursor = mydb.cursor()
    # 查询数据
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    # 关闭数据库连接
    mycursor.close()
    mydb.close()
    return myresult

