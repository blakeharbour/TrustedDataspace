from hotel import settings
import pymysql

from django.conf import settings
import os
import torch.nn as nn
import torch.nn.functional as F



def Dbconnection():
    # db = pymysql.connect("139.196.165.207", "crawl_w", "Bdm_OjX6UwnjbnobjJ1CVLKQ88cSZRKo", "crawl", charset="utf8")
    dbengine = settings.DATABASES['default']['ENGINE']
    dbname = settings.DATABASES['default']['NAME']
    dbuser = settings.DATABASES['default']['USER']
    dbpassword = settings.DATABASES['default']['PASSWORD']
    dbhost = settings.DATABASES['default']['HOST']
    dbport = settings.DATABASES['default']['PORT']
    return pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname, charset="utf8")


def selecttable(tablename, fields="", constr="",groupby="", order="", limit=""):
    db = Dbconnection()
    cursor = db.cursor()
    selectsql=''
    try:
        if fields == "":
            selectsql = " select * from " + tablename
        else:
            selectsql = " select " + fields + " from " + tablename

        if constr != "":
            selectsql = selectsql + " where " + constr

        if groupby != "":
            selectsql = selectsql + " group by " + groupby

        if order != "":
            selectsql = selectsql + " order by  " + order

        if limit != "":
            selectsql = selectsql + " limit  " + str(limit*10-10) + "," +str(10)
        #
        print(selectsql)
        cursor.execute(selectsql)
        result_select = cursor.fetchall()

        # 执行sql语句
        cursor.close()
        db.close()
        return result_select
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        print('selecttable Error')
        print("selectsql:" +selectsql)
        return 0


# 执行命令
def dbsql(strsql):
    db = Dbconnection()
    cursor = db.cursor()
    try:
        cursor.execute(strsql)
        # 执行sql语句
        db.commit()
        cursor.close()
        db.close()
        return 0
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        print(strsql)
        return 1

# 增
def inserttable(pro_js, tablename="", con1=""):
    data = 0
    strsql = "insert into " + tablename + " (" + con1 + ") values " +"("+ pro_js+")"
    print("addstrsql：", strsql)
    data = dbsql(strsql)

    return data

# 删除
def deletetable(tablename, constr):
    db = Dbconnection()
    cursor = db.cursor()
    try:
        if constr!="":
            deletesql = " delete from " + tablename + " where " + constr
        else:
            deletesql = " delete from " + tablename
        # print("deletesql")
        # print(deletesql)
        cursor.execute(deletesql)

        db.commit()
        cursor.close()
        db.close()
        return 1
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        return 0


#改
def updatetable(tablename, updatstr, constr):
    db = Dbconnection()
    cursor = db.cursor()
    try:
        updatesql = " update " + tablename + " set " + updatstr + " where " + constr
        print(updatesql)
        cursor.execute(updatesql)
        # 执行sql语句
        db.commit()
        cursor.close()
        db.close()
        return 1
    except:
        db.rollback()
        db.close()
        return 0
    # 关闭数据库连接
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(4, 5)  # 修改输入特征数
        self.fc2 = nn.Linear(5, 3)  # 修改输出类别数为 3 (鸢尾花数据集有 3 个类别)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

