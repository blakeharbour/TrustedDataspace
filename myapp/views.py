# -*- coding:utf-8 -*-
import json
import subprocess

import corsheaders
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from django.shortcuts import render
from django.http import JsonResponse
import torch

from torch.utils.tensorboard import SummaryWriter
import os
import json
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from sklearn.datasets import load_iris
import pandas as pd
from sklearn.model_selection import train_test_split
from django.views.decorators.csrf import csrf_exempt
import webbrowser
import asyncio
from myapp import api_views

from django.forms.models import *
import pymysql

# from hotel import settings
from . import models

from django.http import JsonResponse
from django.shortcuts import render

from .models import SampleAlignment
from .myjob import *
from .service import TensorBoardService


# from myapp.fed_PU_sci1203.maincf import main

def login(request):
    return render(request, 'login1.html')


def index(request):
    return render(request, 'index.html')


# 参与者列表
def guest_list(request):
    return render(request, 'guest-list.html')


# 参与者添加
def guest_add(request):
    return render(request, 'guest-add.html')


# 参与者编辑
def guest_edit(request):
    return render(request, 'guest-edit.html')


# 发起训练
def model_list(request):
    return render(request, 'model-list.html')


# 增加模型
def model_add(request):
    return render(request, 'model-add.html')


# 发起训练
def modeldel_list(request, parameter):
    context = {'parameter': parameter}
    return render(request, 'modeldel-list.html', context)


def modeldel_add(request, parameter):
    context = {'parameter': parameter}
    return render(request, 'modeldel-add.html', context)


def member_list(request):
    return render(request,'member-list.html')


def member_add(request):
    return render(request,'member-add.html')


def member_edit(request):
    return render(request,'member-edit.html')


def welcome(request):
    return render(request, 'welcome.html')


def changepassword(request):
    return render(request, 'change-password.html')


def sample_alignment(request):
    return render(request, 'sample-alignment.html')


def train_model(request):
    return render(request, 'model_training.html')
def jxclogin(request):
    proobj=request.body
    projs=json.loads(proobj)
    username=projs[0]["username"]
    password=projs[0]["password"]
    print(username)
    print(password)
    # username='wu'
    # password='123'
    filterstr="username= "+"'"+username+"'"
    passwordlist=selecttable("rail_user","password",filterstr,'','','')
    print(passwordlist)
    # (('123',),)
    if passwordlist !=():
        if passwordlist[0][0]==password:
            return JsonResponse({'status':'0','data':'success！','msg':'success'})
        else:
            return JsonResponse({'status':'1', 'data': 'fail！', 'msg': 'success'})
    else:
        return JsonResponse({'status': '2', 'data': 'fail！', 'msg': 'success'})

#创建参与者
def createguest(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    ip = projs[0]["ip"]
    remark = projs[0]["remark"]
    username = projs[0]["username"]
    password = projs[0]["password"]
    data_share_url = projs[0]["data_share_url"]



    # username = "lucy"
    # password = "123456"
    # phone="12345687"
    # remark=""
    # print(res_dict)
    # 在userlist这个表里新建一条记录
    pro_js = "'" + guest + "','" + ip + "','" + remark + "','" + username + "','" + password + "','" + data_share_url + "'"
    inserttable(pro_js, tablename="guest_list", con1="guest,ip,remark,username,password,data_share_url")

    print('xinzengchenggong')
    return JsonResponse({'status': 0})
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
#查找参与者
def searchguest(request):
    guestlist = selecttable("guest_list", "id,guest,ip,remark,testtime,statu,username,password,data_share_url", '', '', '', '')
    print('查找成功')
    print(guestlist)
    return JsonResponse({'status': 0, 'data': guestlist, 'msg': 'success'})
from datetime import datetime
def editguest(guestlist):
    # userid=None
    # username='lusd'
    # password = "123456"
    # phone="12345687"
    # remark=""
    result=0
    pro_js = "statu="+"'"+guestlist[5]+"',testtime="+"'"+guestlist[4]+"'"
    filterstr="id="+"'"+str(guestlist[0])+"'"
    result=updatetable("guest_list",pro_js, filterstr)
    if result==1:
        print('xiugaichenggong')
    if result==0:
        print('xiugaishibai')
    return result
#测试参与者
import pytz
@csrf_exempt
def ping_view(request):
    print('开始')

    if request.method == 'POST':
        proobj = request.body
        projs = json.loads(proobj)
        id = projs[0]["id"]
        print(id)
        guestlist = selecttable("guest_list", "id,guest,ip,remark,testtime,statu", "id="+"'"+id+"'", '', '', '')
        print('ping查找成功')
        print(guestlist)
        ip_address = guestlist[0][2]
        print(ip_address)
        # 执行ping命令
        # 执行 ping 命令
        try:
            print('开始')
            subprocess.run(['ping','-c', '4', ip_address], check=True)
            print('结束')
            guestlist_list=[]
            # 设置北京时区
            beijing_timezone = pytz.timezone('Asia/Shanghai')
            # 获取当前时间并应用时区
            current_time = datetime.now(beijing_timezone)
            # 格式化时间为 "yyyy-mm-dd" 形式
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            # subprocess.run(['ping', '-n', '4', ip_address], check=True)
            print(guestlist[0][0])
            guestlist_list.append(guestlist[0][0])
            guestlist_list.append(guestlist[0][1])
            guestlist_list.append(guestlist[0][2])
            guestlist_list.append(guestlist[0][3])
            guestlist_list.append(str(formatted_time))  # Append the current time as a string
            guestlist_list.append("success")

            result_edit=editguest(guestlist_list)
            if result_edit == 1:
                return JsonResponse({'status': '0', 'data': 'success！', 'msg': 'success'})
            if result_edit == 0:
                return JsonResponse({'status':'1','data':'fail！','msg':'fail'})

        except subprocess.CalledProcessError:
            guestlist_list.append(guestlist[0][0])
            guestlist_list.append(guestlist[0][1])
            guestlist_list.append(guestlist[0][2])
            guestlist_list.append(guestlist[0][3])
            guestlist_list.append(str(datetime.now().time()))  # Append the current time as a string
            guestlist_list.append("fail")
            editguest(guestlist_list);
            return JsonResponse({'status': '2', 'data': 'fail！', 'msg': 'fail'})

    # return render(request, 'ping_template.html')

#查找模型
def searchmodel(request):
    modellist = selecttable("model_list", "id,guest,model,goal,status,Learning_Rate,Weight_Decay,Batch_Size,preci,recall1,error1,val_loss,modelurl,preci_url,recall1_url,error1_url,val_loss_url", '', '', '', '')
    print('查找成功')
    print(modellist)
    return JsonResponse({'status': 0, 'data': modellist, 'msg': 'success'})
#查找模型明细
def searchmodeldel(request):
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    modelid = projs[0]["modelid"]
    modeldellist = selecttable("modeldel_list", "id,modelid,guest,dataurl,status", "modelid='"+modelid+"'", '', '', '')
    print('查找成功')
    print(modeldellist)
    return JsonResponse({'status': 0, 'data': modeldellist, 'msg': 'success'})
def updatemodel(request):
    proobj = request.body
    data_dict = json.loads(proobj)
    print(data_dict)
    id = data_dict["id"]
    guest = data_dict["guest"]
    model = data_dict["model"]
    goal = data_dict["goal"]
    status = "申请中"
    pro_js = "status=" + "'" + status + "',model="+"'"+model+"',guest="+"'"+guest+"',goal="+"'"+goal+"'"
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("model_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
def updatemodel1(request):
    data_dict = json.loads(request)
    print(data_dict)
    id = data_dict["id"]
    guest = data_dict["guest"]
    model = data_dict["model"]
    goal = data_dict["goal"]
    status = "申请中"
    pro_js = "status=" + "'" + status + "',model="+"'"+model+"',guest="+"'"+guest+"',goal="+"'"+goal+"'"
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("model_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
#修改指标
def updatemodel_level(request):
    data_dict = json.loads(request)
    print("data_dict",data_dict)
    preci = data_dict['preci']
    recall1 = data_dict['recall']
    error1 = data_dict['error']
    loss1 = data_dict['loss']
    model_url = data_dict['model_url']
    modelid = data_dict['modelid']

    pro_js = "preci=" + "'" + str(preci) + "',recall1="+"'"+str(recall1)+"',error1="+"'"+str(error1)+"',val_loss="+"'"+str(loss1)+"',modelurl="+"'"+str(model_url)+"'"
    filterstr = "id=" + "'" + modelid + "'"
    updatetable("model_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
def updatemodeldel(request):
    proobj = request.body
    data_dict = json.loads(proobj)
    id = data_dict['id']
    modelid = data_dict['modelid']
    guest = data_dict['guest']
    dataurl = data_dict['dataurl']
    status = "申请中"
    pro_js = "status=" + "'" + status + "',modelid="+"'"+str(modelid)+"',guest="+"'"+guest+"',dataurl="+"'"+dataurl+"'"
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("modeldel_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
def updatemodeldel1(request):
    data_dict = json.loads(request)
    id = data_dict["id"]
    modelid = data_dict["modelid"]
    guest = data_dict["guest"]
    dataurl = data_dict["dataurl"]
    status = "申请中"
    pro_js = "status=" + "'" + status + "',modelid="+"'"+str(modelid)+"',guest="+"'"+guest+"',dataurl="+"'"+dataurl+"'"
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("modeldel_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
def searchmodelall(id):
    modelalllist = selecttable("model_list,modeldel_list", "modeldel_list.id,modeldel_list.modelid,modeldel_list.guest,modeldel_list.dataurl,modeldel_list.status,model_list.model,model_list.goal", "modeldel_list.modelid=model_list.id and modeldel_list.id='"+id+"'", '', '', '')
    print('查找成功')
    print(modelalllist)
    # return JsonResponse({'status': 0, 'data': modelalllist, 'msg': 'success'})
    return modelalllist
def count_searchmodelall(id):
    modelalllist = selecttable("model_list,modeldel_list", "count(id)", "modeldel_list.modelid=model_list.id and and modeldel_list.status in ('拒绝申请','申请中') and modeldel_list.modelid='"+str(id)+"'", '', '', '')
    print('查找成功')
    print(modelalllist)
    # return JsonResponse({'status': 0, 'data': modelalllist, 'msg': 'success'})
    return modelalllist

#创建模型
def createmodel(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    model = projs[0]["model"]
    goal = projs[0]["goal"]
    Learning_Rate = projs[0]["Learning_Rate"]
    Weight_Decay = projs[0]["Weight_Decay"]
    Batch_Size = projs[0]["Batch_Size"]
    status="未申请"
    pro_js = "'" + guest + "','" + model + "','" + goal + "','" + status + "','" + Learning_Rate + "','" + Weight_Decay + "','" + Batch_Size + "'"
    inserttable(pro_js, tablename="model_list", con1="guest,model,goal,status,Learning_Rate,Weight_Decay,Batch_Size")
    print('模型新增成功')
    return JsonResponse({'status': 0})

def deletemodel(request):
    proobj = request.body
    print(proobj)
    projs = json.loads(proobj)
    print(projs)
    id = projs["id"]
    print(id)
    fiterstr="id = "+id
    deletetable("model_list", fiterstr)
    print('删除成功')
    return JsonResponse({'status': 0})
#编辑模型
def editmodelall(request):
    proobj = request.body
    print(proobj)
    # 将字节串解码为字符串
    proobj_str = proobj.decode('utf-8')
    # 将字符串解析为字典
    data_dict = json.loads(json.loads(proobj_str))

    print("数据是",data_dict)
    # id = data_dict.get("id")
    print(id)
    modelid = data_dict["modelid"]
    guest = data_dict["guest"]
    dataurl = data_dict["dataurl"]
    status = data_dict["status"]
    model = data_dict["model"]
    goal = data_dict["goal"]
    status_check = data_dict["status_check"]
    if(status_check=='1'):
        status='同意申请'
    else:
        status = '拒绝申请'
    pro_js = "status="+"'"+status+"'"
    filterstr="id="+"'"+str(id)+"'"
    updatetable("modeldel_list",pro_js, filterstr)
    count=count_searchmodelall(modelid)
    print('count',count)
    if (count == '0'):
        status_Z = '申请成功'
        pro_js = "status=" + "'" + status_Z + "'"
        filterstr = "id=" + "'" + modelid + "'"
        updatetable("model_list", pro_js, filterstr)
    else:
        status = '未申请'
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
def editmodelall1(request):
    proobj = request.body
    data_dict = json.loads(proobj)
    id = data_dict[0]['id']
    modelid = data_dict[0]['modelid']
    guest = data_dict[0]['guest']
    dataurl = data_dict[0]['dataurl']
    status = data_dict[0]['status']
    model = data_dict[0]['model']
    goal = data_dict[0]['goal']
    status_check = data_dict['status_check']
    if(status_check=='1'):
        status='同意申请'
    else:
        status = '拒绝申请'
    pro_js = "status="+"'"+status+"'"
    filterstr="id="+"'"+str(id)+"'"
    updatetable("modeldel_list",pro_js, filterstr)
    count=count_searchmodelall(modelid)
    print('count',count)
    if (count == '0'):
        status_Z = '申请成功'
        pro_js = "status=" + "'" + status_Z + "'"
        filterstr = "id=" + "'" + modelid + "'"
        updatetable("model_list", pro_js, filterstr)
    else:
        status = '未申请'
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
from datetime import datetime


#创建模型明细
def createmodeldel(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    dataurl = projs[0]["dataurl"]
    modelid=projs[0]["modelid"]
    status="未申请"
    pro_js = "'" + guest + "','" + dataurl + "','" + modelid + "','" + status + "'"
    inserttable(pro_js, tablename="modeldel_list", con1="guest,dataurl,modelid,status")
    print('模型新增成功')
    return JsonResponse({'status': 0})

def deletemodeldel(request):
    proobj = request.body
    print(proobj)
    projs = json.loads(proobj)
    print(projs)
    id = projs["id"]
    print(id)
    fiterstr="id = "+id
    deletetable("modeldel_list", fiterstr)
    print('删除成功')
    return JsonResponse({'status': 0})


#发起申请
import paramiko
# def upload_file(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = request.FILES['file']
#             handle_uploaded_file(uploaded_file)
#             # 在这里将文件传递给另一台虚拟机
#             upload_to_remote_server(uploaded_file)
#             return HttpResponse('File uploaded successfully.')
#     else:
#         form = FileUploadForm()
#     return render(request, 'upload.html', {'form': form})
def handle_uploaded_file(file):
    with open('./myapp/fed_PU_sci1203/dataset/tr', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
#申请
import socket
def upload_modelapply(request):
    print("------开始传输------")
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    id = projs[0]["id"]

    data=searchmodelall(id)
    upload_to_remote_server(data[0][2])
    # 转化为字典
    result_dict = {
        "id": str(data[0][0]),
        "modelid": str(data[0][1]),
        "guest": data[0][2],
        "dataurl": data[0][3],
        "status": data[0][4],
        "model": data[0][5],
        "goal": data[0][6],
    }
    modeldel_dict= {
        "id": str(data[0][0]),
        "modelid": str(data[0][1]),
        "guest": data[0][2],
        "dataurl": data[0][3],
        "status": data[0][4],
    }
    model_dict = {
        "id": data[0][1],
        "guest": data[0][2],
        "model": data[0][5],
        "goal": data[0][6],
        "status": data[0][4],
    }
    modeldel_json=json.dumps(modeldel_dict, ensure_ascii=False)
    model_json = json.dumps(model_dict, ensure_ascii=False)
    # 转换为 JSON 格式
    json_data = json.dumps(result_dict, ensure_ascii=False)
    print("json格式",modeldel_json)
    updatemodeldel1(modeldel_json)
    updatemodel1(model_json)
    # upload_modelinfo(data)
    #response = requests.post("http://127.0.0.1:8000/check_apply_re/", json=data_test)
    #需要传输的信息
    # 获取 IP 地址
    ip_address = socket.gethostbyname(socket.gethostname())
    guestlist = selecttable("guest_list", "id,guest,ip,remark,testtime,statu,data_share_url", "guest=" + "'" + data[0][2] + "'", '',
                            '', '')
    data_url = guestlist[0][6]
    print("ip",ip_address)
    model_tran_dict= {
        # "id": str(data[0][0]),
        "model_id": str(data[0][1]),
        "host":str(ip_address),
        "data_url": data_url+'port_feature.txt',#修改
        "status": "未申请",
        "model": data[0][5],
        "goal": data[0][6],
        "status_check": "0",
    }
    json_model_tran = json.dumps(model_tran_dict, ensure_ascii=False)
    guestlist = selecttable("guest_list", "id,guest,ip,remark,testtime,statu", "guest=" + "'" + data[0][2] + "'", '', '', '')
    ip_address = guestlist[0][2]

    url = "http://"+str(ip_address)+":8000/model_self_insert/"
    print(url)
    response = requests.post(url, json=json_model_tran)
    return JsonResponse({'status': 0, 'msg': 'success'})
def upload_to_remote_server(guest):
    print("开始传输文件")
    # 修改为你的目标虚拟机的IP地址、用户名和密码
    guestlist = selecttable("guest_list", "id,guest,ip,remark,testtime,statu,username,password,data_share_url", "guest=" + "'" + guest + "'", '',
                            '', '')
    ip_address = guestlist[0][2]
    # host = '192.168.1.121'
    # port = 22
    # username = 'ywj'
    # password = 'ywj'
    host = guestlist[0][2]
    port = 22
    username = guestlist[0][6]
    password = guestlist[0][7]

    # 连接到目标虚拟机
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port, username, password)

    # 上传文件到目标虚拟机
    sftp = ssh_client.open_sftp()
    local_path = './myapp/fed_PU/share_data/port_feature.txt'
    # remote_path = '/home/ywj/xiangmu/myapp/mount_point/port_feature.txt' # 修改为目标虚拟机上的目标路径
    remote_path = guestlist[0][8]+"port_feature.txt" # 修改为目标虚拟机上的目标路径
    sftp.put(local_path, remote_path)
    sftp.close()

    # 关闭SSH连接
    ssh_client.close()
    print("结束传输文件")
    # return JsonResponse({'status': 0, 'msg': 'success'})
import requests
import json
def upload_modelinfo(data):
    # 处理逻辑
    print("开始调用外部方法")
    data1= {"key": "value", "another_key": "another_value"}
    response = requests.post("http://127.0.0.1:8000/model_self_insert/", json=data1)
    result = response.json()
    print(result)
from myapp.fed_PU_sci1203 import main
from myapp.fed_PU_sci1203 import maincf
# from myapp.fed_PU import client_port
async def model_test(request):
    print('开始执行')
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    modelid = projs[0]["modelid"]
    await maincf.main(modelid)
    # client_port.datapsi()
    print('执行成功')
    return JsonResponse({'status': 0, 'msg': 'success'})

# from django_q.tasks import AsyncTask

def editguest(guestlist):
    # userid=None
    # username='lusd'
    # password = "123456"
    # phone="12345687"
    # remark=""
    result=0
    pro_js = "statu="+"'"+guestlist[5]+"',testtime="+"'"+guestlist[4]+"'"
    filterstr="id="+"'"+str(guestlist[0])+"'"
    result=updatetable("guest_list",pro_js, filterstr)
    if result==1:
        print('xiugaichenggong')
    if result==0:
        print('xiugaishibai')
    return result

def deleteguest(request):
    proobj = request.body
    print(proobj)
    projs = json.loads(proobj)
    print(projs)
    userid = projs["userid"]
    # userid = request.POST.get('userid')
    # userid = "2"
    print(userid)
    fiterstr="id = "+userid
    deletetable("guest_list", fiterstr)
    print('删除成功')
    return JsonResponse({'status': 0})
def createuser(request):
    proobj = request.body
    projs = json.loads(proobj)
    username = projs[0]["username"]
    password = projs[0]["password"]
    phone = projs[0]["phone"]
    remark = projs[0]["remark"]
    # username = "lucy"
    # password = "123456"
    # phone="12345687"
    # remark=""
    # print(res_dict)
    # 在userlist这个表里新建一条记录
    pro_js = "'" + username + "','" + password + "','" + phone + "','" + remark + "'"
    inserttable(pro_js, tablename="userlist", con1="username,password,phone,remark")

    print('xinzengchenggong')
    return JsonResponse({'status': 0})

def deleteuser(request):
    proobj = request.body
    print(proobj)
    projs = json.loads(proobj)
    print(projs)
    userid = projs["userid"]
    # userid = request.POST.get('userid')
    # userid = "2"
    print(userid)
    fiterstr="userid = "+userid
    deletetable("userlist", fiterstr)
    print('删除成功')
    return JsonResponse({'status': 0})



def edituser(request):
    proobj = request.body
    projs = json.loads(proobj)
    username = projs[0]["username"]
    password=projs[0]["password"]
    userid = projs[0]["userid"]
    phone = projs[0]["phone"]
    remark = projs[0]["remark"]
    # userid=None
    # username='lusd'
    # password = "123456"
    # phone="12345687"
    # remark=""
    pro_js = "username="+"'"+username+"',password="+"'"+password+"',phone="+"'"+phone+"',remark="+"'"+remark+"'"
    filterstr="userid="+"'"+userid+"'"
    updatetable("userlist",pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})

def searchuser(request):
    userlist = selecttable("userlist", "userid,username,phone", '', '', '', '')
    print('查找成功')
    print(userlist)
    return JsonResponse({'status': 0, 'data': userlist, 'msg': 'success'})

def oneuser(request):
    proobj = request.body

    projs = json.loads(proobj)
    print(projs)
    userid = projs["userid"]
    print(userid)
    fiterstr="userid = "+userid
    userlist = selecttable("userlist", "userid,username,phone,password,remark", fiterstr, '', '', '')
    print('查找成功')
    return JsonResponse({'status': 0, 'data': userlist, 'msg': 'success'})

def searchSampleAlignment(request):
    userlist = selecttable("sample_alignment", "ID,SAMPLE_NUM,SAMPLE_NUM_SUCCESS,modelid", '', '', '', '')
    print('查找成功')
    print(userlist)
    return JsonResponse({'status': 0, 'data': userlist, 'msg': 'success'})

def saveSampleAlignment(request):
    # proobj = request.body
    projs = json.loads(request)
    print(projs)
    # for proj in projs:
    SAMPLE_NUM = projs["SAMPLE_NUM"]
    SAMPLE_NUM_SUCCESS = projs["SAMPLE_NUM_SUCCESS"]
    alignment = SampleAlignment(SAMPLE_NUM=SAMPLE_NUM,  SAMPLE_NUM_SUCCESS=SAMPLE_NUM_SUCCESS)
    alignment.save()
    print("修改成功")
    return JsonResponse({'status': 0})

def insertSampleAlignment(request):
    # proobj = request.body
    projs = json.loads(request)
    print(projs)
    # for proj in projs:
    SAMPLE_NUM = projs["SAMPLE_NUM"]
    SAMPLE_NUM_SUCCESS = projs["SAMPLE_NUM_SUCCESS"]
    modelid = projs["modelid"]
    pro_js = "'" + str(SAMPLE_NUM)+ "','" +str(SAMPLE_NUM_SUCCESS) + "','" +'1'+ "'"
    inserttable(pro_js, tablename="sample_alignment", con1="SAMPLE_NUM,SAMPLE_NUM_SUCCESS,modelid")
    print('xinzengchenggong')
    return JsonResponse({'status': 0})
def train_model_board(request):
    # 使用 scikit-learn 加载鸢尾花数据集
    iris = load_iris()
    iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    iris_df['target'] = iris.target

    # 划分数据集为训练集和测试集
    train_data, test_data = train_test_split(iris_df, test_size=0.2, random_state=42)

    # 初始化神经网络
    model = SimpleNN()

    # 使用 TensorBoard 记录器
    log_dir = os.path.join(os.path.dirname(__file__), 'tensorboard_logs')
    tensorboard_service = TensorBoardService(logdir=log_dir)
    writer = SummaryWriter(log_dir=log_dir)

    # 定义损失函数和优化器
    criterion = torch.nn.CrossEntropyLoss()  # 适用于分类任务的损失函数
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # 模型训练
    for epoch in range(100):
        # 假设你的数据集有输入和目标列，根据实际情况修改
        inputs = torch.Tensor(train_data.drop('target', axis=1).values)
        targets = torch.LongTensor(train_data['target'].values)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        # 使用 TensorBoard 记录损失值
        writer.add_scalar('Loss', loss.item(), epoch)

    # 关闭 TensorBoard 记录器
    writer.close()

    # 启动 TensorBoard 服务
    tensorboard_service.run_tensorboard()

    print('tensor train finsh')

    return JsonResponse({'status': 'success'})


async def train_model_boardnew(request):
    #铁路查找模型信息表对应的model id
    #selecttable("MODEL_INFO", "id,model_name,model_goal,is_be", '', '', '', '')
    modelId = "1"
    await maincf.main()

    # 异步运行启动 TensorBoard
    # 手动检查 TensorBoard 是否启动并获取 URL
    # if tensorboard_service.url:
    #     return HttpResponse(f'TensorBoard 已在 {tensorboard_service.url} 启动')
    # else:
    #     return HttpResponse("TensorBoard 启动，但无法获取 URL。请手动检查。")

    print('tensor train finsh')

    return JsonResponse({'status': 'success'})


