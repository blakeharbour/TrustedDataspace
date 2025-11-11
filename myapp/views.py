import torch
# -*- coding:utf-8 -*-
import json
import socket
import subprocess
import traceback
import json
from django.db import connection

import datetime
from django.http import JsonResponse
import corsheaders
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime, date
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
# from huggingface_hub.utils import parse_datetime
# from sqlalchemy.sql.functions import current_user

from .models import LoginUser, AssetRecord, AssetDimension, AssetDimensionDetail
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import time
import uuid
import shutil
from torch.utils.tensorboard import SummaryWriter
import os
import json
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from sklearn.datasets import load_iris
import pandas as pd
from sklearn.model_selection import train_test_split
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import SampleAlignment
from .myjob import *
from .service import TensorBoardService
from django.contrib.auth.decorators import login_required

def login_page(request):
    return render(request, 'login.html')

@login_required(login_url='/login/')
def tdindex(request):
    return render(request, 'tdindex.html')

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def mutiindex(request):
    return render(request, 'mutiindex.html')

@login_required(login_url='/login/')
def registeruser(request):
    return render(request, 'registeruser.html')

@login_required(login_url='/login/')
# 用户管理
def user_list(request):
    return render(request, 'user-list.html',{
        'current_user': request.user  # 传递用户对象到模板
    })

@login_required(login_url='/login/')
def login_add(request):
    return render(request, 'login-add.html')

@login_required(login_url='/login/')
def login_edit(request):
    return render(request, 'login-edit.html')


@login_required(login_url='/login/')
# 参与者列表
def guest_list(request):
    return render(request, 'guest-list.html')

@login_required(login_url='/login/')
# 参与者添加
def guest_add(request):
    return render(request, 'guest-add.html')

@login_required(login_url='/login/')
# 参与者编辑
def guest_edit(request):
    return render(request, 'guest-edit.html')

@login_required(login_url='/login/')
#数据接口界面
def wb_interface(request):
    return render(request, 'wb-interface.html', {
        'current_user': request.user  # 传递用户对象到模板
    })

@login_required(login_url='/login/')
#数据沙箱界面
def sjsx_interface(request):
    return render(request, 'sjsx-interface.html', {
        'current_user': request.user  # 传递用户对象到模板
    })

def sjtzadd(request):
    return render(request, 'sjtzadd.html', {
        'current_user': request.user  # 传递用户对象到模板
    })

def shaxiangip(request):
    return render(request, 'shaxiangip.html', {
        'current_user': request.user  # 传递用户对象到模板
    })

def shaxiangipbox(request):
    return render(request, 'shaxiangipbox.html', {
        'current_user': request.user  # 传递用户对象到模板
    })
def upload_to_sandbox(request):
    return render(request, 'upload_to_sandbox.html', {
        'current_user': request.user  # 传递用户对象到模板
    })


def xqflist_open(request):
    return render(request, 'xqflist_open.html', {
        'current_user': request.user  # 传递用户对象到模板
    })


@login_required(login_url='/login/')
def interface_add(request):
    return render(request, 'interface-add.html')

@login_required(login_url='/login/')
def interface_edit(request):
    return render(request, 'interface-edit.html')


@login_required(login_url='/login/')
def sjsxinterface_edit(request):
    return render(request, 'sjsxinterface-edit.html')


def dictfetchall(cursor):
    "返回带字段名的字典形式结果"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@login_required(login_url='/login/')
# 发起训练
def model_list(request):
    return render(request, 'model-list.html')

@login_required(login_url='/login/')
# 增加模型
def model_add(request):
    return render(request, 'model-add.html')

@login_required(login_url='/login/')
# 发起训练
def modeldel_list(request, parameter):
    context = {'parameter': parameter}
    return render(request, 'modeldel-list.html', context)

@login_required(login_url='/login/')
def modeldel_add(request, parameter):
    context = {'parameter': parameter}
    return render(request, 'modeldel-add.html', context)

@login_required(login_url='/login/')
def member_list(request):
    return render(request,'member-list.html')

@login_required(login_url='/login/')
def member_add(request):
    return render(request,'member-add.html')

@login_required(login_url='/login/')
def member_edit(request):
    return render(request,'member-edit.html')

@login_required(login_url='/login/')
def welcome(request):
    return render(request, 'welcome.html')

@login_required(login_url='/login/')
def changepassword(request):
    return render(request, 'change-password.html')

@login_required(login_url='/login/')
def sample_alignment(request):
    return render(request, 'sample-alignment.html')

@login_required(login_url='/login/')
def train_model(request):
    return render(request, 'model_training.html')
@login_required(login_url='/login/')
def established_project(request):
    return render(request, 'establish-project.html', {
        'current_user': request.user  # 传递用户对象到模板
    })
@login_required(login_url='/login/')
def pending_project(request):
    return render(request, 'pending_project.html')
@login_required(login_url='/login/')
def project_add(request):
    return render(request, 'project_add.html',{
        'current_user': request.user  # 传递用户对象到模板
    })

@login_required(login_url='/login/')
def project_notarization(request):
    return render(request, 'project_notarization.html', {
        'current_user': request.user  # 传递用户对象到模板
    })
@login_required(login_url='/login/')
def pengding_project(request):
    return render(request, 'pending_project.html')

@login_required(login_url='/login/')
def project_notarization_add(request):
    return render(request, 'project_notarization_add.html')

def jxclogin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data=data[0]
            print(data)
            account = data.get('username')
            password = data.get('password')

            print(account)
            print(password)
            # 使用 Django 认证系统
            user = authenticate(request, username=account, password=password)
            print(user)

            if user is not None:
                login(request, user)
                return JsonResponse({'status':'0','data':'success！','msg':'success'})
            else:
                return JsonResponse({'status': '1', 'msg': '账号或密码错误'})

        except Exception as e:
            return JsonResponse({'status': '2', 'msg': '请求解析失败'})

    return JsonResponse({'status': '3', 'msg': '仅支持 POST 请求'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 解析 JSON 数据
        data = json.loads(request.body)
        print(data)
        data=data[0]
        account = data.get('account')
        password = data.get('password')
        com = data.get('com')

        # 数据验证：确保所有字段都不为空
        if not account or not password or not com:
            return JsonResponse({'status': 'error', 'message': '所有字段不能为空'})

        # 检查账号是否已存在
        if LoginUser.objects.filter(account=account).exists():
            return JsonResponse({'status': 'error', 'message': '账号已存在'})

        # 创建新用户并保存到数据库
        user = LoginUser.objects.create_user(account=account, password=password, com=com)

        return JsonResponse({'status': 'success', 'message': '注册成功'})
    else:
        return JsonResponse({'status': 'error', 'message': 'error'})

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
    # 在userlist这个表里新建一条记录
    pro_js = "'" + guest + "','" + ip + "','" + remark + "','" + username + "','" + password + "','" + data_share_url + "'"
    inserttable(pro_js, tablename="guest_list", con1="guest,ip,remark,username,password,data_share_url")

    print('xinzengchenggong')
    return JsonResponse({'status': 0})

def createlogin(request):
    proobj = request.body
    projs = json.loads(proobj)
    account = projs[0]["account"]
    password = projs[0]["password"]
    com = projs[0]["com"]
    comid = projs[0]["comid"]
    # 在userlist这个表里新建一条记录
    pro_js = "'" + account + "','" + password + "','" + com + "','" + comid + "'"
    inserttable(pro_js, tablename="login_user", con1="account,password,com,comid")
    print('xinzengchenggong')
    return JsonResponse({'status': 0})

def editlogin(request):
    proobj = request.body
    projs = json.loads(proobj)
    account = projs[0]["account"]
    password = projs[0]["password"]
    com = projs[0]["com"]
    comid = projs[0]["comid"]
    # 在userlist这个表里新建一条记录
    pro_js = "'" + account + "','" + password + "','" + com + "','" + comid + "'"
    inserttable(pro_js, tablename="login_user", con1="account,password,com,comid")
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

def searchlogin(request):
    proobj = request.body

    projs = json.loads(proobj)
    print(projs)
    com = projs["com"]
    print(com)
    fiterstr = f"com = '{com}'"
    loginlist = selecttable("login_user", "id,account,com,comid", fiterstr,
                            '', '', '')
    print('查找成功')
    print(loginlist)
    return JsonResponse({'status': 0, 'data': loginlist, 'msg': 'success'})

def searchonelogin(request):
    proobj = request.body

    projs = json.loads(proobj)
    print(projs)
    userid = projs["userid"]
    print(userid)
    fiterstr="id = "+userid
    userlist = selecttable("login_user", "id,account,password,com,comid", fiterstr, '', '', '')
    print('查找成功')
    return JsonResponse({'status': 0, 'data': userlist, 'msg': 'success'})

def check_sandbox_ip(request):
    try:
        proobj = request.body
        projs = json.loads(proobj)

        address = projs.get("address", "").strip()
        if not address:
            return JsonResponse({'allowed': False, 'message': '缺少沙箱路径'}, status=400)
        print("[前端传来地址]:", address)

        # 自动获取客户端 IP
        client_ip = get_client_ip1()
        print(client_ip)


        # 查询 IP 白名单
        fiterstr = f"address = '{address}'"
        iplist = selecttable("sandboxip", "ip", fiterstr, '', '', '')
        print("[IP白名单]:", iplist)

        if not iplist:
            iplist = []

        allowed_ip_set = set(row[0] for row in iplist)
        is_allowed = client_ip in allowed_ip_set
        jieguo = '成功' if is_allowed else '失败'

        print("[即将插入日志]：", f"'{address}', '{client_ip}', '{jieguo}'")


        inserttable(f"'{address}', '{client_ip}', '{jieguo}'", "sandboxiplog", "address, ip, jieguo")

        return JsonResponse({
            'allowed': is_allowed,
            'message': 'IP 验证通过' if is_allowed else '当前 IP 未被授权访问'
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'allowed': False,
            'message': f"请求处理异常: {str(e)}"
        }, status=500)


def get_local_ip():
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

def get_client_ip1():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Failed to get client IP: {e}")
        return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

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

def searchinterface(request):
    # proobj = request.body
    # projs = json.loads(proobj)
    # print(projs)
    # projectName = projs["projectName"]
    # fiterstr = "projectName = " + projectName
    interfacelist = selecttable("webinterface", "id,webname,weburl,webprotocol,webtype,datatype,comallowed,projectName", '',
                            '', '', '')
    print('查找成功')
    print(interfacelist)
    return JsonResponse({'status': 0, 'data': interfacelist, 'msg': 'success'})


def searchinsbsxterface(request):
    # 如果后续需要根据请求体过滤，可以恢复下面的注释代码
    # proobj = request.body
    # projs = json.loads(proobj)
    # projectName = projs["projectName"]
    # fiterstr = "projectName = '" + projectName + "'"

    # 使用 webinsjsxterface 表，并提取所有字段
    interfacelist = selecttable(
        "webinsjsxterface",
        "confirmman, confirmtime, saveurl, zichanname, staytime, jiamipro, autoscope, delchannle",
        '', '', '', ''
    )
    print('查找成功')
    print(interfacelist)
    return JsonResponse({'status': 0, 'data': interfacelist, 'msg': 'success'})

def useBlockchain(request):
    proobj = request.body
    projs = json.loads(proobj)
    # webName = request.body.decode('utf-8')  # 转换为字符串
    webName = projs[0]["webName"]
    projectName = projs[0]["projectName"]
    type =projs[0]["type"]
    select_js = "assetName = '" + webName + "'"
    selectlist = selecttable("myapp_dataasset", "assetName,assetOwner,assetFormat,assetLevel,assetPath,assetID",
                             select_js, '',
                             '', '')
    assetName = selectlist[0][0]
    assetOwner = selectlist[0][1]
    assetFormat = selectlist[0][2]
    assetLevel = selectlist[0][3]
    assetPath = selectlist[0][4]
    assetID = selectlist[0][5]
    print(assetName)

    if (assetLevel == "L1"):
        assetLevel = "高敏感密文"
    elif (assetLevel == "L2"):
        assetLevel = "高敏感"
    elif (assetLevel == "L3"):
        assetLevel = "敏感"
    elif (assetLevel == "L4"):
        assetLevel = "低敏感"

    # 上传到区块链
    blockchain_url = "http://192.168.1.135:8080/datasharing/addRaw"

    payload = {
        "data": "anydata"
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.put(blockchain_url, data=json.dumps(payload), headers=headers)

    # 尝试解析JSON响应
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        # 处理非JSON响应的情况
        print(f"接口返回非JSON数据: {response.text}")
        return None

    # 处理成功响应
    if response_data.get("status") == "ok":
        print("区块链交易成功")
        payload_data = response_data.get("payload", {})
        # 将json字符串转换为字典
        data = json.loads(payload_data)
        print(payload_data)
        tx_time = data.get("txTime")
        tx_id = data["txID"]
        tx_hash = data["txHash"]
        print(tx_time)
        print(tx_id)
        print(tx_hash)

    # 查询项目表信息
    select_js = "projectName = '" + projectName + "'"
    selectlist = selecttable("pb8_ProjectAdd",
                             "ID,  dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus",
                             select_js, '',
                             '', '')
    projectId = str(selectlist[0][0])
    dataDemand = selectlist[0][1]
    dataOwner = selectlist[0][2]
    dataAsset = selectlist[0][3]
    dataSecurity = selectlist[0][4]
    shareWay = selectlist[0][5]

    # 在asset_record这个表里新建一条记录
    if (type == "1") :
        asset_js = "'" + assetName + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + assetPath + "','已上传数据','已完成数据传输','调用数据接口','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
        inserttable(asset_js, tablename="asset_record",
                con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")
    elif (type == "2"):
        asset_js = "'" + assetName + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + assetPath + "','未参与模型计算','已完成模型计算','模型计算','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
        inserttable(asset_js, tablename="asset_record",
                    con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")

    # 在project_notarization这个表里新建一条记录
    pro_js = "'" + projectId + "','" + projectName + "','" + dataDemand + "','" + dataOwner + "','" + dataAsset + "','已完成','" + dataSecurity + "','" + shareWay + "','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(pro_js, tablename="project_notarization",
                con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType,tranasctionTime,tranasctionId,hashDigest")

    return JsonResponse({'status': 0})


def useBlockchainshaxiang(request):#刘书琳新增
    proobj = request.body
    projs = json.loads(proobj)
    # webName = request.body.decode('utf-8')  # 转换为字符串
    webName = projs[0]["webName"]
    projectName = projs[0]["projectName"]

    select_js = "assetName = '" + webName + "'"
    selectlist = selecttable("myapp_dataasset", "assetName,assetOwner,assetFormat,assetLevel,assetPath,assetID",
                             select_js, '',
                             '', '')
    assetName = selectlist[0][0]
    assetOwner = selectlist[0][1]
    assetFormat = selectlist[0][2]
    assetLevel = selectlist[0][3]
    assetPath = selectlist[0][4]
    assetID = selectlist[0][5]
    print(assetName)

    if (assetLevel == "L1"):
        assetLevel = "高敏感密文"
    elif (assetLevel == "L2"):
        assetLevel = "高敏感"
    elif (assetLevel == "L3"):
        assetLevel = "敏感"
    elif (assetLevel == "L4"):
        assetLevel = "低敏感"

    # 上传到区块链
    blockchain_url = "http://192.168.1.135:8080/datasharing/addRaw"

    payload = {
        "data": "anydata"
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.put(blockchain_url, data=json.dumps(payload), headers=headers)

    # 尝试解析JSON响应
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        # 处理非JSON响应的情况
        print(f"接口返回非JSON数据: {response.text}")
        return None

    # 处理成功响应
    if response_data.get("status") == "ok":
        print("区块链交易成功")
        payload_data = response_data.get("payload", {})
        # 将json字符串转换为字典
        data = json.loads(payload_data)
        print(payload_data)
        tx_time = data.get("txTime")
        tx_id = data["txID"]
        tx_hash = data["txHash"]
        print(tx_time)
        print(tx_id)
        print(tx_hash)

    # 查询项目表信息
    select_js = "projectName = '" + projectName + "'"
    selectlist = selecttable("pb8_ProjectAdd",
                             "ID,  dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus",
                             select_js, '',
                             '', '')
    print(selectlist)
    projectId = str(selectlist[0][0])
    dataDemand = selectlist[0][1]
    dataOwner = selectlist[0][2]
    dataAsset = selectlist[0][3]
    dataSecurity = selectlist[0][4]
    shareWay = selectlist[0][5]

    # 在asset_record这个表里新建一条记录

    asset_js = "'" + assetName + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + assetPath + "','已上传数据','已完成数据沙箱调用','调用数据沙箱','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(asset_js, tablename="asset_record",
                con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")

    # 在project_notarization这个表里新建一条记录
    pro_js = "'" + projectId + "','" + projectName + "','" + dataDemand + "','" + dataOwner + "','" + dataAsset + "','已完成','" + dataSecurity + "','" + shareWay + "','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(pro_js, tablename="project_notarization",
                con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType,tranasctionTime,tranasctionId,hashDigest")

    return JsonResponse({'status': 0})

def createinterface(request):
    proobj = request.body
    projs = json.loads(proobj)
    webname = projs[0]["webname"]
    weburl = projs[0]["weburl"]
    webprotocol = projs[0]["webprotocol"]
    webtype = projs[0]["webtype"]
    datatype = projs[0]["datatype"]
    comallowed = projs[0]["comallowed"]
    projectName = projs[0]["projectName"]

    #查询数据资产表信息
    select_js = "assetName = '" + webname + "'"
    selectlist = selecttable("myapp_dataasset", "assetName,assetOwner,assetFormat,assetLevel,assetPath,assetID", select_js, '',
                             '', '')
    assetName = selectlist[0][0]
    assetOwner = selectlist[0][1]
    assetFormat = selectlist[0][2]
    assetLevel = selectlist[0][3]
    assetPath = selectlist[0][4]
    assetID = selectlist[0][5]
    print(assetName)

    if (assetLevel == "L1"):
        assetLevel = "高敏感密文"
    elif (assetLevel == "L2"):
        assetLevel = "高敏感"
    elif (assetLevel == "L3"):
        assetLevel = "敏感"
    elif (assetLevel == "L4"):
        assetLevel = "低敏感"


    # 上传到区块链
    blockchain_url = "http://192.168.1.135:8080/datasharing/addRaw"

    payload = {
        "data": "anydata"
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.put(blockchain_url, data=json.dumps(payload), headers=headers)

    # 尝试解析JSON响应
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        # 处理非JSON响应的情况
        print(f"接口返回非JSON数据: {response.text}")
        return None

    # 处理成功响应
    if response_data.get("status") == "ok":
        print("区块链交易成功")
        payload_data = response_data.get("payload", {})
        #将json字符串转换为字典
        data=json.loads(payload_data)
        print(payload_data)
        tx_time = data.get("txTime")
        tx_id = data["txID"]
        tx_hash = data["txHash"]
        print(tx_time)
        print(tx_id)
        print(tx_hash)

    # 在asset_record这个表里新建一条记录
    asset_js = "'" + assetName + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + weburl + "','未上传数据','已上传数据','上传数据接口','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(asset_js, tablename="asset_record", con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")


    # 在webinterface这个表里新建一条记录
    web_js = "'" + webname + "','" + weburl + "','" + webprotocol + "','" + webtype + "','" + datatype + "','" + comallowed + "','" + projectName + "'"
    inserttable(web_js, tablename="webinterface", con1="webname,weburl,webprotocol,webtype,datatype,comallowed,projectName")
    return JsonResponse({'status': 0})



def createinterfacesx(request):

    zcname = request.POST.get("zcname")  # 从前端拿 zcname
    print(zcname)

    select_js = "assetName = '" + zcname + "'"
    selectlist = selecttable("myapp_dataasset", "assetName,assetOwner,assetFormat,assetLevel,assetPath,assetID", select_js, '',
                             '', '')


    assetOwner = selectlist[0][1]
    assetFormat = selectlist[0][2]
    assetLevel = selectlist[0][3]
    assetPath = selectlist[0][4]
    assetID = selectlist[0][5]



    if (assetLevel == "L1"):
        assetLevel = "高敏感密文"
    elif (assetLevel == "L2"):
        assetLevel = "高敏感"
    elif (assetLevel == "L3"):
        assetLevel = "敏感"
    elif (assetLevel == "L4"):
        assetLevel = "低敏感"
    print("资产信息：", assetOwner, assetFormat, assetLevel, assetPath, assetID)
    # 上传到区块链
    blockchain_url = "http://192.168.1.135:8080/datasharing/addRaw"

    payload = {
        "data": "anydata"
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.put(blockchain_url, data=json.dumps(payload), headers=headers)

    # 尝试解析JSON响应
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        # 处理非JSON响应的情况
        print(f"接口返回非JSON数据: {response.text}")
        return None

    # 处理成功响应
    if response_data.get("status") == "ok":
        print("区块链交易成功")
        payload_data = response_data.get("payload", {})
        #将json字符串转换为字典
        data=json.loads(payload_data)
        print(payload_data)
        tx_time = data.get("txTime")
        tx_id = data["txID"]
        tx_hash = data["txHash"]
        print(tx_time)
        print(tx_id)
        print(tx_hash)



    # 在asset_record这个表里新建一条记录
    asset_js = "'" + zcname + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + assetPath + "','未上传数据','已上传数据','封装沙箱数据','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(asset_js, tablename="asset_record", con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")
    return JsonResponse({"status": "0", "message": "封装成功，已写入区块链"})


def getreadonlylink(request):
    print("getreadonlylink() 接口已被调用")
    print("请求方法：", request.method)

    if request.method != "POST":
        return JsonResponse({"status": 1, "message": "只支持POST请求"})

    sandbox_path = request.POST.get("sandbox_path")
    print("接收到的 sandbox_path：", sandbox_path)

    if not sandbox_path:
        return JsonResponse({"status": 1, "message": "缺少sandbox_path参数"})

    select_js = "sandbox_path = '" + sandbox_path + "'"
    print("构造的查询条件 select_js：", select_js)

    try:
        selectlist = selecttable(
            "readonlylinktable",
            "readonly_link",
            select_js,
            '',
            '',
            ''
        )

        print("查询结果 selectlist：", selectlist)

        if selectlist and len(selectlist) > 0:
            readonly_link = selectlist[0][0]
            print("返回的只读链接：", readonly_link)
            return JsonResponse({"status": 0, "readonly_link": readonly_link})
        else:
            print("未查询到数据")
            return JsonResponse({"status": 1, "message": "未找到对应的只读链接"})

    except Exception as e:
        print("查询只读链接异常:", e)
        return JsonResponse({"status": 1, "message": "服务器内部错误"})

#数据IP追踪模块
def createip(request):
    projs = json.loads(request.body)  # 是 dict，不是 list
    address = projs["address"]
    ip = projs["ip"]

    pro_js = (
        "'" + address + "','" + ip + "'"
    )
    inserttable(
        pro_js,
        tablename="sandboxip",
        con1="address,ip"
    )
    print("xinzengchenggong")
    return JsonResponse({'status': 0})



#########数据IP追踪模块2
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from myapp.models import SandboxIPLog
import logging
logger = logging.getLogger(__name__)

@require_POST
def createipbox(request):
    """
    接收 { address }，只查询 sandboxiplog 表中对应 address 的所有 ip，
    返回 { success, data: [{ ip }, …] }。
    """
    try:
        payload = json.loads(request.body.decode('utf-8'))
        address = payload.get('address', '').strip()
        if not address:
            return JsonResponse({'success': False, 'error': 'address 不能为空'}, status=400)

        # —— 只查询 ip 列 ——
        qs = (SandboxIPLog.objects
              .filter(address=address)
              .values('ip', 'jieguo'))

        data = [
            {'ip': rec['ip'], 'jieguo': rec['jieguo']}
            for rec in qs
        ]

        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        logger.error("[createipbox] 查询出错", exc_info=True)
        return JsonResponse({'success': False, 'error': '服务器内部错误'}, status=500)

#######

def insertreadonlylink(request):
    try:
        print("收到原始请求体：", request.body)

        projs = json.loads(request.body)
        print("解析后的数据 dict：", projs)

        sandbox_path = projs["sandbox_path"]
        readonly_link = projs["readonly_link"]

        print("sandbox_path =", sandbox_path)
        print("readonly_link =", readonly_link)

        pro_js = "'" + sandbox_path + "','" + readonly_link + "'"
        print("拼接后的 pro_js:", pro_js)

        inserttable(
            pro_js,
            tablename="readonlylinktable",
            con1="sandbox_path,readonly_link"
        )

        print("readonlylink新增成功")
        return JsonResponse({'status': 0})

    except Exception as e:
        print("数据库插入失败：", e)
        return JsonResponse({'status': 1, 'error': str(e)})



def createsandbox(request):
    projs = json.loads(request.body)  # 是 dict，不是 list

    confirmman = projs["confirmman"]
    confirmtime = projs["confirmtime"]
    saveurl = projs["saveurl"]
    zichanname = projs["zichanname"]
    staytime = projs["staytime"]
    jiamipro = projs["jiamipro"]
    autoscope = projs["autoscope"]
    delchannle = projs["delchannle"]

    pro_js = (
        "'" + confirmman + "','" + confirmtime + "','" + saveurl + "','" +
        zichanname + "','" + staytime + "','" + jiamipro + "','" +
        autoscope + "','" + delchannle + "'"
    )

    inserttable(
        pro_js,
        tablename="webinsjsxterface",
        con1="confirmman,confirmtime,saveurl,zichanname,staytime,jiamipro,autoscope,delchannle"
    )

    print("xinzengchenggong")
    return JsonResponse({'status': 0})


def delete_sandbox_info(request):
    try:
        projs = json.loads(request.body)
        confirmman = projs.get("confirmman", "").strip()
        saveurl = projs.get("saveurl", "").strip()

        if not confirmman or not saveurl:
            return JsonResponse({'success': False, 'message': '缺少必要参数'})

        cursor = connection.cursor()
        sql = """
            DELETE FROM webinsjsxterface
            WHERE confirmman = %s AND saveurl = %s
        """
        cursor.execute(sql, [confirmman, saveurl])
        connection.commit()  # 显式提交

        print("✅ shanchuchenggong，删除条数：", cursor.rowcount)
        return JsonResponse({'success': True, 'message': '删除成功'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def deleteinterface(request):
    proobj = request.body
    print(proobj)
    projs = json.loads(proobj)
    print(projs)
    id = projs["id"]
    # userid = request.POST.get('userid')
    # userid = "2"
    print(id)
    fiterstr="id = "+id
    deletetable("webinterface", fiterstr)
    print('删除成功')
    return JsonResponse({'status': 0})

def sysxdeleteinterface(request):
    try:
        proobj = request.body
        print(proobj)
        projs = json.loads(proobj)
        print(projs)

        confirmman = projs.get("confirmman", "").strip()
        saveurl = projs.get("saveurl", "").strip()

        if not confirmman or not saveurl:
            return JsonResponse({'status': 1, 'message': '参数不完整'})

        fiterstr = f"confirmman = '{confirmman}' AND saveurl = '{saveurl}'"
        deletetable("webinsjsxterface", fiterstr)

        print('✅ 删除成功')
        return JsonResponse({'status': 0})

    except Exception as e:
        print("❌ 删除失败：", str(e))
        return JsonResponse({'status': 1, 'message': str(e)})


def searchoneinterface(request):
    proobj = request.body

    projs = json.loads(proobj)
    print(projs)
    id = projs["id"]
    print(id)
    fiterstr="id = "+id
    interfacelist = selecttable("webinterface", "id,webname,weburl,webprotocol,webtype,datatype,comallowed,projectName", fiterstr, '', '', '')
    print('查找成功')
    return JsonResponse({'status': 0, 'data': interfacelist, 'msg': 'success'})


def sysxsearchoneinterface(request):
    projs = json.loads(request.body)
    confirmman = projs.get("confirmman", "").strip()
    saveurl = projs.get("saveurl", "").strip()

    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT confirmman, confirmtime, saveurl, zichanname, staytime, jiamipro, autoscope, delchannle
        FROM webinsjsxterface
        WHERE confirmman = %s AND saveurl = %s
    """, [confirmman, saveurl])

    data = dictfetchall(cursor)

    return JsonResponse({'status': 0, 'data': data})





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
    modellist = selecttable("model_list", "id,guest,model,goal,status,Learning_Rate,Weight_Decay,Batch_Size,preci,recall1,error1,val_loss,preci_url,recall1_url,error1_url,val_loss_url,modelurl", '', '', '', '')
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
    #response = requests.post("/check_apply_re/", json=data_test)
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
    response = requests.post("/model_self_insert/", json=data1)
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

def deletelogin(request):
    proobj = request.body
    print(proobj)
    projs = json.loads(proobj)
    print(projs)
    userid = projs["id"]
    # userid = request.POST.get('userid')
    # userid = "2"
    print(userid)
    fiterstr="id = "+userid
    deletetable("login_user", fiterstr)
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
from django.core.paginator import Paginator
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def data_asset_list(request):
    data_assets = DataAsset.objects.all().order_by('assetID')  # 获取所有数据资产并按ID排序
    paginator = Paginator(data_assets, 10)  # 每页显示10条数据
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据
    return render(request, 'data_asset_list.html', {'page_obj': page_obj})

from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, redirect, render
from .models import DataAsset, AssetRecord
import requests
import logging
from django.contrib import messages
from dateutil import parser
logger = logging.getLogger(__name__)
def add_data_asset(request):
    if request.method == 'POST':
        try:
            # 创建数据资产
            asset = DataAsset.objects.create(
                assetName=request.POST['assetName'],
                assetOwner=request.POST['assetOwner'],
                description=request.POST['description'],
                assetFormat=request.POST['assetFormat'],
                assetLevel=request.POST['assetLevel'],
                # status=request.POST['status'],
                # assetPath=request.POST['assetPath'],
            )

            # 创建初始存证记录（状态：无 → 未上传）
            record = AssetRecord.objects.create(
                assetName=asset.assetName,
                assetOwner=asset.assetOwner,
                assetFormat=asset.assetFormat,
                assetLevel=asset.assetLevel,
                assetPath='无',
                star_status='未上传数据资产',
                end_status='已上传数据资产',
                operation='新增数据资产项',
                txTime=None,
                txID='',
                txHash=''
            )

            # 上传到区块链
            blockchain_url = "http://192.168.1.135:8080/datasharing/addRaw"
            payload = {
                "assetID": str(asset.assetID),
                "assetName": asset.assetName,
                "assetOwner": asset.assetOwner,
                # "assetField": asset.description,
                "assetFormat": asset.assetFormat,
                "assetLevel": asset.assetLevel,
                # "assetPath": asset.assetPath,
                "assetRole": "test"
            }
            headers = {'Content-Type': 'application/json'}

            response = requests.put(blockchain_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    payload_str = response_data.get('payload', '{}')
                    payload_data = json.loads(payload_str)

                    # 解析时间（兼容任意格式）
                    tx_time_str = payload_data.get('txTime', '')
                    try:
                        tx_time = parser.parse(tx_time_str)  # 自动解析
                        if not timezone.is_aware(tx_time):
                            tx_time = timezone.make_aware(tx_time)  # 默认时区
                    except:
                        tx_time = timezone.now()  # 失败时用当前时间

                    # 更新存证记录
                    record.end_status = '未上传'
                    record.txTime = tx_time
                    record.txID = payload_data.get('txID', '')
                    record.txHash = payload_data.get('txHash', '')
                    record.save()


                    messages.success(request, '数据资产和存证记录已成功创建！')
                    return redirect('data_asset_list')

                except Exception as e:
                    logger.error(f"解析区块链响应失败: {str(e)}")
                    record.end_status = '上传失败'
                    record.save()
                    asset.delete()
                    messages.error(request, '区块链响应解析失败，数据已回滚。')
                    return render(request, 'data_asset_add.html')

            else:
                logger.error(f"区块链上传失败，状态码: {response.status_code}")
                record.end_status = '上传失败'
                record.save()
                asset.delete()
                messages.error(request, '区块链上传失败，数据已回滚。')
                return render(request, 'data_asset_add.html')

        except Exception as e:
            if 'asset' in locals():
                asset.delete()
            if 'record' in locals():
                record.delete()
            logger.error(f"操作失败: {str(e)}")
            messages.error(request, f'操作失败: {str(e)}')
            return render(request, 'data_asset_add.html')

    return render(request, 'data_asset_add.html')

# def edit_data_asset(request, asset_id):
#     asset = get_object_or_404(DataAsset, assetID=asset_id)
#     if request.method == 'POST':
#         # 更新数据资产字段
#         asset.assetName = request.POST.get('assetName')
#         asset.assetOwner = request.POST.get('assetOwner')
#         asset.description = request.POST.get('description')
#         asset.assetFormat = request.POST.get('assetFormat')
#         asset.assetLevel = request.POST.get('assetLevel')
#         asset.status = request.POST.get('status')
#         asset.assetPath = request.POST.get('assetPath')
#         asset.save()
#
#
#         return redirect('/data_asset_list/')
#     return render(request, 'data_asset_edit.html', {'asset': asset})
#
# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_protect
#
# @require_http_methods(["POST"])
# @csrf_protect
# def batch_delete_data_asset(request):
#     try:
#         selected_ids = list(map(int, request.POST.getlist('selected_assets')))
#         DataAsset.objects.filter(assetID__in=selected_ids).delete()
#         return JsonResponse({'status': 'success'})
#     except ValueError:
#         return JsonResponse({'status': 'error', 'message': '无效的ID格式'}, status=400)
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def edit_data_asset(request, asset_id):
    asset = get_object_or_404(DataAsset, assetID=asset_id)
    if request.method == 'POST':
        try:
            # 保存旧状态
            old_status = asset.status
            old_asset_name = asset.assetName  # 可选：记录其他旧值

            # 更新数据资产字段
            asset.assetName = request.POST.get('assetName')
            asset.assetOwner = request.POST.get('assetOwner')
            asset.description = request.POST.get('description')
            asset.assetFormat = request.POST.get('assetFormat')
            asset.assetLevel = request.POST.get('assetLevel')
            # asset.status = request.POST.get('status')
            # asset.assetPath = request.POST.get('assetPath')
            asset.save()

            # 创建存证记录（不调用区块链）
            AssetRecord.objects.create(
                assetName=asset.assetName,
                assetOwner=asset.assetOwner,
                assetFormat=asset.assetFormat,
                assetLevel=asset.get_assetLevel_display(),
                assetPath='无',
                star_status='已上传数据资产项',  # 旧状态
                end_status='未上传数据',  # 新状态
                operation='编辑数据资产项',
                txTime=timezone.now(),  # 本地时间
                txID='N/A',  # 无区块链操作
                txHash='N/A'
            )

            return redirect('/data_asset_list/')

        except Exception as e:
            # 可以添加日志记录或错误提示
            print(f"编辑操作失败: {str(e)}")
            return render(request, 'data_asset_edit.html', {'asset': asset, 'error': str(e)})

    return render(request, 'data_asset_edit.html', {'asset': asset})


#批量删除
from django.db import transaction

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
@require_http_methods(["POST"])
@csrf_protect
def batch_delete_data_asset(request):
    try:
        selected_ids = list(map(int, request.POST.getlist('selected_assets')))
        assets = DataAsset.objects.filter(assetID__in=selected_ids)

        with transaction.atomic():  # 事务保证操作原子性
            for asset in assets:
                # 为每个资产创建存证记录
                AssetRecord.objects.create(
                    assetName=asset.assetName,
                    assetOwner=asset.assetOwner,
                    assetFormat=asset.assetFormat,
                    assetLevel=asset.get_assetLevel_display(),
                    assetPath='无',
                    star_status='已上传数据资产项',
                    end_status='未上传数据',
                    operation='删除数据资产项',
                    txTime=timezone.now(),  # 本地时间
                    txID='N/A',
                    txHash='N/A'
                )
                asset.delete()  # 逐个删除

            return JsonResponse({'status': 'success'})

    except ValueError:
        return JsonResponse({'status': 'error', 'message': '无效的ID格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)





@login_required
def asset_field_dimension(request, asset_id):
    # 获取数据资产
    asset = get_object_or_404(DataAsset, assetID=asset_id, assetOwner=request.user.com)

    # 获取所有机构列表（排除当前用户所属机构）
    companies = LoginUser.objects.exclude(com=request.user.com).values_list('com', flat=True).distinct()

    # 获取该资产的所有维度设置
    dimensions = AssetDimension.objects.filter(asset=asset)
    dimension_details = AssetDimensionDetail.objects.filter(asset=asset)

    # 获取所有字段名（从现有维度设置中提取）
    field_names = set(dimensions.values_list('field_name', flat=True))

    return render(request, 'asset_field_dimension.html', {
        'asset': asset,
        'companies': companies,
        'field_names': sorted(field_names),
        'dimensions': dimensions,
        'dimension_details': dimension_details
    })


@csrf_exempt
@login_required
def get_dimension_detail(request, dimension_id):
    try:
        dimension = AssetDimension.objects.get(id=dimension_id)
        # 检查权限
        if dimension.asset.assetOwner != request.user.com:
            return JsonResponse({'success': False, 'message': '没有权限'})

        # 获取时间维度明细
        time_detail = AssetDimensionDetail.objects.filter(
            asset=dimension.asset,
            target_company=dimension.target_company,
            field_name=dimension.field_name,
            sub_dimension='time'
        ).first()

        # 获取空间维度明细
        space_detail = AssetDimensionDetail.objects.filter(
            asset=dimension.asset,
            target_company=dimension.target_company,
            field_name=dimension.field_name,
            sub_dimension='space'
        ).first()

        return JsonResponse({
            'success': True,
            'dimension': {
                'id': dimension.id,
                'field_name': dimension.field_name,
                'target_company': dimension.target_company,
                'security_dimension': dimension.security_dimension,
                'time_dimension': dimension.time_dimension,
                'space_dimension': dimension.space_dimension,
                'business_dimension': dimension.business_dimension,
            },
            'time_detail': time_detail.sub_dimension_detail if time_detail else '',
            'space_detail': space_detail.sub_dimension_detail if space_detail else ''
        })
    except AssetDimension.DoesNotExist:
        return JsonResponse({'success': False, 'message': '维度设置不存在'})

@csrf_exempt
@login_required
def save_dimension(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asset = get_object_or_404(DataAsset, assetID=data.get('asset_id'))
            # 检查权限
            if asset.assetOwner != request.user.com:
                return JsonResponse({'success': False, 'message': '没有权限'})

            # 如果是编辑现有维度
            if data.get('dimension_id'):
                dimension = AssetDimension.objects.get(id=data.get('dimension_id'))
                # 检查权限
                if dimension.asset.assetOwner != request.user.com:
                    return JsonResponse({'success': False, 'message': '没有权限'})

                # 检查目标机构是否改变
                old_target_company = dimension.target_company
                new_target_company = data.get('target_company')

                # 如果目标机构改变，需要删除旧的明细记录
                if old_target_company != new_target_company:
                    AssetDimensionDetail.objects.filter(
                        asset=asset,
                        target_company=old_target_company,
                        field_name=dimension.field_name
                    ).delete()
            else:
                # 创建新维度
                dimension = AssetDimension(
                    asset=asset,
                    user=request.user,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name')
                )

            # 更新维度字段
            dimension.target_company = data.get('target_company')  # 确保更新目标机构
            dimension.security_dimension = data.get('security_dimension')
            dimension.time_dimension = data.get('time_dimension')
            dimension.space_dimension = data.get('space_dimension')
            dimension.business_dimension = data.get('business_dimension')
            dimension.save()

            # 处理时间维度明细
            time_detail = data.get('time_detail')
            if time_detail and data.get('time_dimension'):
                # 删除旧的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='time'
                ).delete()

                # 创建新的明细记录
                AssetDimensionDetail.objects.create(
                    asset=asset,
                    user=request.user,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='time',
                    sub_dimension_detail=time_detail
                )
            elif not data.get('time_dimension'):
                # 如果没有选择时间维度，删除相关的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='time'
                ).delete()

            # 处理空间维度明细
            space_detail = data.get('space_detail')
            if space_detail and data.get('space_dimension'):
                # 删除旧的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='space'
                ).delete()

                # 创建新的明细记录
                AssetDimensionDetail.objects.create(
                    asset=asset,
                    user=request.user,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='space',
                    sub_dimension_detail=space_detail
                )
            elif not data.get('space_dimension'):
                # 如果没有选择空间维度，删除相关的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='space'
                ).delete()

            return JsonResponse({'success': True, 'message': '保存成功'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '无效的请求方法'})

@csrf_exempt
@login_required
def delete_dimension(request, dimension_id):
    if request.method == 'POST':
        try:
            dimension = AssetDimension.objects.get(id=dimension_id)
            # 检查权限
            if dimension.asset.assetOwner != request.user.com:
                return JsonResponse({'success': False, 'message': '没有权限'})

            # 删除相关的明细记录
            AssetDimensionDetail.objects.filter(
                asset=dimension.asset,
                target_company=dimension.target_company,
                field_name=dimension.field_name
            ).delete()

            # 删除主记录
            dimension.delete()

            return JsonResponse({'success': True, 'message': '删除成功'})
        except AssetDimension.DoesNotExist:
            return JsonResponse({'success': False, 'message': '维度设置不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '无效的请求方法'})


# 添加字段的视图
@csrf_exempt
@login_required
def add_field(request, asset_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asset = get_object_or_404(DataAsset, assetID=asset_id)
            # 检查权限
            if asset.assetOwner != request.user.com:
                return JsonResponse({'success': False, 'message': '没有权限'})

            field_name = data.get('field_name')

            # 检查字段是否已存在
            if field_name in set(AssetDimension.objects.filter(asset=asset).values_list('field_name', flat=True)):
                return JsonResponse({'success': False, 'message': '字段已存在'})

            # 返回成功，字段会在前端动态添加
            return JsonResponse({
                'success': True,
                'message': '字段添加成功',
                'field_name': field_name
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '无效的请求方法'})

@login_required(login_url='/login/')
def asset_record_list(request):
    current_user = request.user

    try:
        # 检查用户是否有 com 字段
        if not hasattr(current_user, 'com'):
            return render(request, 'data_asset_record.html', {
                'error': '用户信息异常，缺少所属公司字段',
                'records': [],
                'current_user': current_user
            })

        # 按用户所属公司 (com) 过滤资产记录的 assetOwner
        records = AssetRecord.objects.filter(assetOwner=current_user.com)

    except Exception as e:
        # 处理数据库查询异常
        return render(request, 'data_asset_record.html', {
            'error': f'数据库查询失败: {str(e)}',
            'records': [],
            'current_user': current_user
        })

    return render(request, 'data_asset_record.html', {
        'records': records,
        'current_user': current_user  # 传递完整的用户对象到模板
    })

#查找存证信息
def search_notarization(request):
    #新增限制条件：当前登录用户必须为数据需求方或者所有方
    currentUser = request.user
    assetDemander = currentUser.com
    assetOwner = currentUser.com
    condition = f"(assetDemander='{assetDemander}' OR assetOwner='{assetOwner}')"
    notarizationlist = selecttable(
        "project_notarization",
        "id, projectName, assetDemander, assetOwner, assetName, status, assetLevel, assetSharingType, tranasctionId, tranasctionTime, hashDigest",
        condition, '', '', ''
    )
    return JsonResponse({'status': 0, 'data': notarizationlist, 'msg': 'success'})

#根据项目名称查找存证信息
def search_notarization_by_projectname(request):
    # 新增限制条件：当前登录用户必须为数据需求方或者所有方
    currentUser = request.user
    assetDemander = currentUser.com
    assetOwner = currentUser.com
    project_name = request.GET.get('project_name', '')

    base_condition = f"(assetDemander='{assetDemander}' OR assetOwner='{assetOwner}')"

    if project_name:
        # 模糊查询 + 权限校验
        search_condition = f"(projectName LIKE '%{project_name}%') AND {base_condition}"
        notarizationlist = selecttable(
            "project_notarization",
            "id, projectName, assetDemander, assetOwner, assetName, status, assetLevel, assetSharingType, tranasctionId, tranasctionTime, hashDigest",
            search_condition, '', '', ''
        )
    else:
        # 直接使用权限校验条件
        notarizationlist = selecttable(
            "project_notarization",
            "id, projectName, assetDemander, assetOwner, assetName, status, assetLevel, assetSharingType, tranasctionId, tranasctionTime, hashDigest",
            base_condition, '', '', ''
        )
    return JsonResponse({'status': 0, 'data': notarizationlist, 'msg': 'success'})

@csrf_exempt
def create_project(request):
        try:
            proobj = request.body
            projs = json.loads(proobj)
            projectName = projs['projectName']
            dataDemand = projs['dataDemand']
            dataOwner = projs['dataOwner']
            dataAsset = projs['dataAsset']
            dataSecurity = projs['dataSecurity']
            shareWay = projs['shareWay']
            isDeleted = 'N'
            currentStatus = '0'

            print(projectName)

            # 调用 inserttable 函数插入数据到 pb8_ProjectAdd 表
            pro_js = "'" + projectName + "','" + dataDemand + "','" + dataOwner + "','" + dataAsset + "','" + dataSecurity + "','" + shareWay + "','" + isDeleted + "','" + currentStatus +"'"
            inserttable(pro_js, tablename="pb8_ProjectAdd",
                        con1="projectName,dataDemand,dataOwner,dataAsset,dataSecurity,shareWay,isDeleted,currentStatus")

            print('项目新增成功,状态更新成功')
            return JsonResponse({'status': '0', 'message': '新增成功'})
        except Exception as e:
            return JsonResponse({'status': '1', 'message': f'出现错误: {str(e)}'})

def get_status_description(currentStatus):
    status_mapping = {
        "0": "发起",
        "1": "待审核",
        "2": "审核通过",
        "3": "审核不通过",
        "4": "正在进行",
        "5": "已完成"
    }
    return status_mapping.get(currentStatus, "已删除")


def submit_project_toblockchain(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        data_demander = request.POST.get('data_demander')
        data_owner = request.POST.get('data_owner')
        data_asset = request.POST.get('data_asset')
        security_level = request.POST.get('security_level')
        trans_mode = request.POST.get('trans_mode')

        constr = ""
        conditions = []
        if project_name:
            conditions.append(f"projectName = '{project_name}'")
        if data_demander:
            conditions.append(f"dataDemand = '{data_demander}'")
        if data_owner:
            conditions.append(f"dataOwner = '{data_owner}'")
        if data_asset:
            conditions.append(f"dataAsset = '{data_asset}'")
        if security_level:
            conditions.append(f"dataSecurity = '{security_level}'")
        if trans_mode:
            conditions.append(f"shareWay = '{trans_mode}'")

        if conditions:
            constr = " AND ".join(conditions)

        fields = 'ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus'
        order = 'ID DESC'
        result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr, order=order, limit=1)

        if result:
            ID, project_name, data_demander, data_owner, data_asset, security_level, trans_mode, currentStatus = result[0]

            blockchainData = {
                'transactionID': ID,
                'projectName': project_name,
                'assetName': data_asset,
                'assetOwner': data_owner,
                'assetDemander': data_demander,
                'assetLevel': security_level,
                'assetSharingType': trans_mode,
                'ipfs': ''
            }
            blockchainDataStr = json.dumps(blockchainData)

            try:
                response = requests.put('http://192.168.1.135:8080/datasharing/addRaw', data=blockchainDataStr, headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    print("区块链接口响应:", response.json())
                    # 解析区块链返回的 payload
                    payload = json.loads(response.json().get('payload', '{}'))
                    tx_time = payload.get('txTime')
                    tx_id = payload.get('txID')
                    tx_hash = payload.get('txHash')

                    # 获取状态描述
                    status = get_status_description(currentStatus)

                    # 构建插入数据的字符串
                    pro_js = f"'{ID}','{project_name}','{data_demander}','{data_owner}','{data_asset}','{status}','{security_level}','{trans_mode}','{tx_time}','{tx_id}','{tx_hash}'"
                    # 调用 inserttable 函数插入数据到 project_notarization 表
                    inserttable(pro_js, tablename="project_notarization",
                                con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType, tranasctionTime,tranasctionId,hashDigest")

                    return JsonResponse({'status': 'ok','message': '区块链接口调用成功，数据已存入项目存证表'})
                else:
                    print("区块链接口调用失败:", response.text)
                    return JsonResponse({'status': 'error','message': '区块链接口调用失败，请稍后重试'})
            except requests.RequestException as e:
                print("请求异常:", e)
                return JsonResponse({'status': 'error','message': '请求区块链接口时发生异常，请稍后重试'})
        else:
            print("数据库查询无结果")
            return JsonResponse({'status': 'error','message': '数据库查询无结果'})
    return JsonResponse({'status': 'error','message': '无效的请求方法'})


def get_project_data(request):
    try:
        currentUser = request.user
        dataDemand = currentUser.com
        dataOwner = currentUser.com
        # 构建查询条件
        constr = f"isDeleted != 'Y' AND (dataDemand = '{dataDemand}' OR (dataOwner = '{dataOwner}' AND currentStatus = '2'))"
        fields = "ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus"
        result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr)

        if result:
            data_list = []
            for row in result:
                row_data = {
                    'ID': row[0],
                    'projectName': row[1],
                    'dataDemand': row[2],
                    'dataOwner': row[3],
                    'dataAsset': row[4],
                    'dataSecurity': row[5],
                   'shareWay': row[6],
                    'currentStatus': row[7]
                }
                data_list.append(row_data)
            return JsonResponse({'status': '0', 'data': data_list})
        else:
            return JsonResponse({'status': '1','message': '未查询到符合条件的数据'})
    except Exception as e:
        return JsonResponse({'status': '1','message': f'查询数据时出现错误: {str(e)}'})

def get_pending_project_data(request):
    try:
        currentUser = request.user
        dataOwner = currentUser.com
        # 构建查询条件
        constr = f"isDeleted != 'Y' AND currentStatus != '0' AND dataOwner = '{dataOwner}'"
        fields = "ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus"
        result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr)

        if result:
            data_list = []
            for row in result:
                row_data = {
                    'ID': row[0],
                    'projectName': row[1],
                    'dataDemand': row[2],
                    'dataOwner': row[3],
                    'dataAsset': row[4],
                    'dataSecurity': row[5],
                   'shareWay': row[6],
                    'currentStatus': row[7]
                }
                data_list.append(row_data)
            return JsonResponse({'status': '0', 'data': data_list})
        else:
            return JsonResponse({'status': '1','message': '未查询到符合条件的数据'})
    except Exception as e:
        return JsonResponse({'status': '1','message': f'查询数据时出现错误: {str(e)}'})

def delete_project(request):
    if request.method == 'POST':
        projectName = request.POST.get('projectName')
        dataDemand = request.POST.get('dataDemand')
        dataOwner = request.POST.get('dataOwner')
        dataAsset = request.POST.get('dataAsset')
        id = request.POST.get('id')  # 获取 ID 参数

        if projectName and dataDemand and dataOwner and dataAsset and id:
            # 构建删除条件时添加 ID
            updatstr = "isDeleted = 'Y'"
            constr = f"projectName = '{projectName}' and dataDemand = '{dataDemand}' and dataOwner = '{dataOwner}' and dataAsset = '{dataAsset}' and ID = '{id}'"
            result = updatetable('pb8_ProjectAdd', updatstr, constr)
            if result == 1:
                # 获取项目相关信息，查询条件同样添加 ID
                fields = 'ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus'
                order = 'ID DESC'
                project_result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr, order=order, limit=1)

                if project_result:
                    ID, project_name, data_demander, data_owner, data_asset, security_level, trans_mode, currentStatus = project_result[0]

                    blockchainData = {
                        'transactionID': ID,
                        'projectName': project_name,
                        'assetName': data_asset,
                        'assetOwner': data_owner,
                        'assetDemander': data_demander,
                        'assetLevel': security_level,
                        'assetSharingType': trans_mode,
                        'ipfs': ''
                    }
                    blockchainDataStr = json.dumps(blockchainData)

                    try:
                        response = requests.put('http://192.168.1.135:8080/datasharing/addRaw', data=blockchainDataStr, headers={'Content-Type': 'application/json'})
                        if response.status_code == 200:
                            print("区块链接口响应:", response.json())
                            # 解析区块链返回的 payload
                            payload = json.loads(response.json().get('payload', '{}'))
                            tx_time = payload.get('txTime')
                            tx_id = payload.get('txID')
                            tx_hash = payload.get('txHash')

                            # 获取状态描述
                            status = get_status_description(currentStatus)

                            # 构建插入数据的字符串
                            pro_js = f"'{ID}','{project_name}','{data_demander}','{data_owner}','{data_asset}','已删除','{security_level}','{trans_mode}','{tx_time}','{tx_id}','{tx_hash}'"
                            # 调用 inserttable 函数插入数据到 project_notarization 表
                            inserttable(pro_js, tablename="project_notarization",
                                        con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType, tranasctionTime,tranasctionId,hashDigest")

                            return JsonResponse({'status': '0', 'message': '删除成功，区块链接口调用成功，数据已存入项目存证表'})
                        else:
                            print("区块链接口调用失败:", response.text)
                            return JsonResponse({'status': '1', 'message': '删除成功，但区块链接口调用失败，请稍后重试'})
                    except requests.RequestException as e:
                        print("请求异常:", e)
                        return JsonResponse({'status': '1', 'message': '删除成功，但请求区块链接口时发生异常，请稍后重试'})
                else:
                    print("数据库查询无结果")
                    return JsonResponse({'status': '1', 'message': '删除成功，但数据库查询无结果'})
            else:
                return JsonResponse({'status': '1', 'message': '删除失败'})
        else:
            return JsonResponse({'status': '1', 'message': '缺少必要的参数'})
    else:
        return JsonResponse({'status': '1', 'message': '请求方法错误，仅支持POST请求'})


def update_project(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            projectName = request.POST.get('projectName')
            dataDemand = request.POST.get('dataDemand')
            dataOwner = request.POST.get('dataOwner')
            dataAsset = request.POST.get('dataAsset')
            dataSecurity = request.POST.get('dataSecurity')
            shareWay = request.POST.get('shareWay')

            # 构建更新字符串
            update_str_list = []
            if projectName is not None:
                update_str_list.append(f"projectName = '{projectName}'")
            if dataDemand is not None:
                update_str_list.append(f"dataDemand = '{dataDemand}'")
            if dataOwner is not None:
                update_str_list.append(f"dataOwner = '{dataOwner}'")
            if dataAsset is not None:
                update_str_list.append(f"dataAsset = '{dataAsset}'")
            if dataSecurity is not None:
                update_str_list.append(f"dataSecurity = '{dataSecurity}'")
            if shareWay is not None:
                update_str_list.append(f"shareWay = '{shareWay}'")

            if not update_str_list:
                return JsonResponse({'status': '1', 'message': '没有提供需要更新的字段'})

            update_str = ", ".join(update_str_list)
            condition_str = f"id = {id}"

            # 调用 updatetable 方法
            result = updatetable("pb8_ProjectAdd", update_str, condition_str)

            if result == 1:
                return JsonResponse({'status': '0', 'message': '修改成功'})
            else:
                return JsonResponse({'status': '1', 'message': '修改失败'})

    except Exception as e:
        return JsonResponse({'status': '1', 'message': f'出现错误: {str(e)}'})
def audit_project(request):
    try:
        if request.method == 'POST':
            # 从 POST 请求中获取项目 ID 和要更新的状态
            id = request.POST.get('id')
            currentStatus = request.POST.get('currentStatus')

            # 检查是否提供了必要的参数
            if id is None or currentStatus is None:
                return JsonResponse({'status': '1','message': '缺少必要参数'})

            # 构建更新字符串
            update_str = f"currentStatus = '{currentStatus}'"
            condition_str = f"id = {id}"

            # 调用 updatetable 方法
            result = updatetable("pb8_ProjectAdd", update_str, condition_str)

            if result == 1:
                # 获取项目相关信息
                fields = 'ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus'
                order = 'ID DESC'
                project_result = selecttable('pb8_ProjectAdd', fields=fields, constr=condition_str, order=order, limit=1)

                if project_result:
                    ID, project_name, data_demander, data_owner, data_asset, security_level, trans_mode, currentStatus = project_result[0]

                    blockchainData = {
                        'transactionID': ID,
                        'projectName': project_name,
                        'assetName': data_asset,
                        'assetOwner': data_owner,
                        'assetDemander': data_demander,
                        'assetLevel': security_level,
                        'assetSharingType': trans_mode,
                        'ipfs': ''
                    }
                    blockchainDataStr = json.dumps(blockchainData)

                    try:
                        response = requests.put('http://192.168.1.135:8080/datasharing/addRaw', data=blockchainDataStr, headers={'Content-Type': 'application/json'})
                        if response.status_code == 200:
                            print("区块链接口响应:", response.json())
                            # 解析区块链返回的 payload
                            payload = json.loads(response.json().get('payload', '{}'))
                            tx_time = payload.get('txTime')
                            tx_id = payload.get('txID')
                            tx_hash = payload.get('txHash')

                            # 获取状态描述
                            status = get_status_description(currentStatus)

                            # 构建插入数据的字符串
                            pro_js = f"'{ID}','{project_name}','{data_demander}','{data_owner}','{data_asset}','{status}','{security_level}','{trans_mode}','{tx_time}','{tx_id}','{tx_hash}'"
                            # 调用 inserttable 函数插入数据到 project_notarization 表
                            inserttable(pro_js, tablename="project_notarization",
                                        con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType, tranasctionTime,tranasctionId,hashDigest")

                            return JsonResponse({'status': '0','message': '审核状态更新成功，区块链接口调用成功，数据已存入项目存证表'})
                        else:
                            print("区块链接口调用失败:", response.text)
                            return JsonResponse({'status': '1','message': '审核状态更新成功，但区块链接口调用失败，请稍后重试'})
                    except requests.RequestException as e:
                        print("请求异常:", e)
                        return JsonResponse({'status': '1','message': '审核状态更新成功，但请求区块链接口时发生异常，请稍后重试'})
                else:
                    print("数据库查询无结果")
                    return JsonResponse({'status': '1','message': '审核状态更新成功，但数据库查询无结果'})
            else:
                return JsonResponse({'status': '1','message': '审核状态更新失败'})
    except Exception as e:
        return JsonResponse({'status': '1','message': f'出现错误: {str(e)}'})

def submit_project(request):
    try:
        if request.method == 'POST':
            # 从 POST 请求中获取项目 ID
            id = request.POST.get('id')
            # 设定提交后的状态为 1
            currentStatus = '1'

            # 检查是否提供了必要的参数
            if id is None:
                return JsonResponse({'status': '1','message': '缺少必要参数: id'})

            # 构建更新字符串
            update_str = f"currentStatus = '{currentStatus}'"
            condition_str = f"id = {id}"

            # 调用 updatetable 方法
            result = updatetable("pb8_ProjectAdd", update_str, condition_str)

            if result == 1:
                # 获取项目相关信息
                fields = 'ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus'
                order = 'ID DESC'
                project_result = selecttable('pb8_ProjectAdd', fields=fields, constr=condition_str, order=order, limit=1)

                if project_result:
                    ID, project_name, data_demander, data_owner, data_asset, security_level, trans_mode, currentStatus = project_result[0]

                    blockchainData = {
                        'transactionID': ID,
                        'projectName': project_name,
                        'assetName': data_asset,
                        'assetOwner': data_owner,
                        'assetDemander': data_demander,
                        'assetLevel': security_level,
                        'assetSharingType': trans_mode,
                        'ipfs': ''
                    }
                    blockchainDataStr = json.dumps(blockchainData)

                    try:
                        response = requests.put('http://192.168.1.135:8080/datasharing/addRaw', data=blockchainDataStr, headers={'Content-Type': 'application/json'})
                        if response.status_code == 200:
                            print("区块链接口响应:", response.json())
                            # 解析区块链返回的 payload
                            payload = json.loads(response.json().get('payload', '{}'))
                            tx_time = payload.get('txTime')
                            tx_id = payload.get('txID')
                            tx_hash = payload.get('txHash')

                            # 获取状态描述
                            status = get_status_description(currentStatus)

                            # 构建插入数据的字符串
                            pro_js = f"'{ID}','{project_name}','{data_demander}','{data_owner}','{data_asset}','{status}','{security_level}','{trans_mode}','{tx_time}','{tx_id}','{tx_hash}'"
                            # 调用 inserttable 函数插入数据到 project_notarization 表
                            inserttable(pro_js, tablename="project_notarization",
                                        con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType, tranasctionTime,tranasctionId,hashDigest")

                            return JsonResponse({'status': '0','message': '项目提交成功，区块链接口调用成功，数据已存入项目存证表'})
                        else:
                            print("区块链接口调用失败:", response.text)
                            return JsonResponse({'status': '1','message': '项目提交成功，但区块链接口调用失败，请稍后重试'})
                    except requests.RequestException as e:
                        print("请求异常:", e)
                        return JsonResponse({'status': '1','message': '项目提交成功，但请求区块链接口时发生异常，请稍后重试'})
                else:
                    print("数据库查询无结果")
                    return JsonResponse({'status': '1','message': '项目提交成功，但数据库查询无结果'})
            else:
                return JsonResponse({'status': '1','message': '项目提交失败'})

    except Exception as e:
        return JsonResponse({'status': '1','message': f'出现错误: {str(e)}'})

from django.http import JsonResponse

def search_project_data(request):
    try:
        currentUser = request.user
        dataDemand = currentUser.com

        # 从请求中获取查询参数
        projectName = request.POST.get('projectName', '')
        dataOwner = request.POST.get('dataOwner', '')
        dataAsset = request.POST.get('dataAsset', '')
        securityLevel = request.POST.get('securityLevel', '')
        status = request.POST.get('status', '')

        # 构建查询条件列表
        conditions = [f"isDeleted != 'Y'", f"dataDemand = '{dataDemand}'"]

        if projectName:
            conditions.append(f"projectName LIKE '%{projectName}%'")
        if dataOwner:
            conditions.append(f"dataOwner = '{dataOwner}'")
        if dataAsset:
            conditions.append(f"dataAsset LIKE '%{dataAsset}%'")
        if securityLevel:
            conditions.append(f"dataSecurity = '{securityLevel}'")
        if status:
            conditions.append(f"currentStatus = '{status}'")

        # 组合查询条件
        constr = " AND ".join(conditions)

        fields = "ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus"
        result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr)

        if result:
            data_list = []
            for row in result:
                row_data = {
                    'ID': row[0],
                    'projectName': row[1],
                    'dataDemand': row[2],
                    'dataOwner': row[3],
                    'dataAsset': row[4],
                    'dataSecurity': row[5],
                    'shareWay': row[6],
                    'currentStatus': row[7]
                }
                data_list.append(row_data)
            return JsonResponse({'status': '0', 'data': data_list})
        else:
            return JsonResponse({'status': '1','message': '未查询到符合条件的数据'})
    except Exception as e:
        return JsonResponse({'status': '1','message': f'查询数据时出现错误: {str(e)}'})

from django.http import JsonResponse

def search_pending_project_data(request):
    try:
        # 假设这里获取当前用户相关信息，后续用于筛选条件
        currentUser = request.user
        dataOwner = currentUser.com

        # 从请求中获取查询参数
        projectName = request.POST.get('projectName', '')
        dataDemandFilter = request.POST.get('dataDemand', '')
        status = request.POST.get('status', '')

        # 构建查询条件列表，默认筛选未删除且当前状态为待处理（这里假设待处理状态为 '1'）
        conditions = [f"isDeleted != 'Y'", f"currentStatus != '0'",f"dataOwner = '{dataOwner}'"]
        if projectName:
            conditions.append(f"projectName LIKE '%{projectName}%'")
        if dataDemandFilter:
            conditions.append(f"dataDemand = '{dataDemandFilter}'")
        if status:
            conditions.append(f"currentStatus = '{status}'")

        # 组合查询条件
        constr = " AND ".join(conditions)

        # 定义要查询的字段
        fields = "ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus"
        # 调用自定义的 selecttable 函数进行数据查询
        result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr)

        if result:
            data_list = []
            for row in result:
                row_data = {
                    'ID': row[0],
                    'projectName': row[1],
                    'dataDemand': row[2],
                    'dataOwner': row[3],
                    'dataAsset': row[4],
                    'dataSecurity': row[5],
                    'shareWay': row[6],
                    'currentStatus': row[7]
                }
                data_list.append(row_data)
            return JsonResponse({'status': '0', 'data': data_list})
        else:
            return JsonResponse({'status': '1','message': '未查询到符合条件的待处理项目数据'})
    except Exception as e:
        return JsonResponse({'status': '1','message': f'查询待处理项目数据时出现错误: {str(e)}'})








#------------------------------------------------------------------------------------------
# IP追踪
# myapp/views.py

import logging
from django.shortcuts import render
from django.http import JsonResponse
from cryptography.fernet import Fernet
import json
from datetime import datetime
import base64
import openpyxl
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# 设置日志记录
logging.basicConfig(level=logging.INFO)

# 允许访问的 IP 列表
ALLOWED_IPS = ['192.168.1.141', '10.61.222.249', '0.0.0.0']

# 存储 IP 地址的文件路径
IP_HISTORY_FILE = 'ip_history.txt'

# 生成密钥
def generate_key():
    return Fernet.generate_key()

# 加密数据
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# 创建数据包
def create_data_packet(encrypted_data, key, client_ip, user_agent, timestamp, url, query_params):
    return {
        'encrypted_data': base64.b64encode(encrypted_data).decode(),
        'key': base64.b64encode(key).decode(),
        'client_ip': client_ip,
        'user_agent': user_agent,
        'timestamp': timestamp,
        'url': url,
        'query_params': query_params
    }

# 生成数据
def generate_data():
    data = []
    excel_file_path = 'D:\\testdata\\data\\test.xlsx'
    # 打开 Excel 文件
    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active  # 获取活动的工作表
    # 遍历工作表中的每一行，并将数据添加到列表中
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    return data

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # 取第一个 IP 地址作为客户端 IP
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # 如果没有 HTTP_X_FORWARDED_FOR 头信息，就使用 REMOTE_ADDR
        ip = request.META.get('REMOTE_ADDR')
    return ip

def read_ip_history():
    try:
        with open(IP_HISTORY_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def write_ip_history(ip_list):
    with open(IP_HISTORY_FILE, 'w') as file:
        for ip in ip_list:
            file.write(ip + '\n')

@csrf_exempt
def get_data(request):
    try:
        if request.method == 'GET':
            # 优先从请求头获取客户端 IP
            client_ip = request.headers.get('X-Client-IP')
            if not client_ip:
                # 如果请求头没有，从请求的元数据中获取
                client_ip = get_client_ip(request)

            # 检查客户端 IP 是否在允许的 IP 列表中
            if client_ip not in ALLOWED_IPS:
                return JsonResponse({"status": "error", "message": "Access denied"}, status=403)

            # 获取客户端的 User-Agent
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
            # 获取请求的时间戳
            timestamp = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            # 获取请求的 URL 和查询参数
            url = request.build_absolute_uri()
            query_params = request.GET.dict()
            # 生成数据
            data = generate_data()
            # 将数据转换为 JSON 字符串
            data_str = json.dumps(data, ensure_ascii=False)
            # 生成密钥
            key = generate_key()
            # 加密数据
            encrypted_data = encrypt_data(data_str, key)

            # 若客户端 IP 不是 0.0.0.0，则更新 IP 历史记录
            if client_ip != '0.0.0.0':
                ip_history = read_ip_history()
                if client_ip not in ip_history:
                    ip_history.append(client_ip)
                write_ip_history(ip_history)

            # 获取 IP 历史记录
            ip_history = read_ip_history()
            # 取最新的非 0.0.0.0 的 IP 地址，如果没有则显示默认信息
            latest_non_local_ip = ip_history[-1] if ip_history else 'No recent non - local clients'
            print(ip_history)
            # 创建数据包
            data_packet = create_data_packet(encrypted_data, key, latest_non_local_ip, user_agent, timestamp, url, query_params)

            # 在日志中记录客户端 IP 和请求的时间
            logging.info(f"Received request from IP: {client_ip}")
            # 返回 HTML 模板，同时传递 IP 历史记录
            return render(request, 'data_view1.html', {'data_packet': data_packet, 'ip_history': ip_history})
        else:
            return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def show_latest_ip(request):
    latest_client_ip = request.session.get('latest_client_ip', 'No recent clients')
    return render(request, 'show_latest_ip.html', {'latest_client_ip': latest_client_ip})

def data_model(request):
    return render(request, 'data_view1.html')


# 数据确权相关视图函数AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from datetime import datetime, date
import requests
from .myjob import selecttable, updatetable, inserttable
from django.db import models

from .models import (
    DataRightApplication,
    DataRightRecord,
    DataRightApplicationHistory,
    DATA_SOURCE_CHOICES,
    #BUSINESS_STAGE_CHOICES
)

def get_company_code_from_name(company_name):
    """
    将中文公司名称转换为英文代码
    """
    # 创建反向映射字典：中文名称 -> 英文代码
    name_to_code_mapping = {
        name: code for code, name in DATA_SOURCE_CHOICES
    }

    # 查找对应的英文代码
    company_code = name_to_code_mapping.get(company_name)
    return company_code


def get_user_company_code(user):
    """
    获取用户对应的公司英文代码
    """
    if not hasattr(user, 'com') or not user.com:
        return None

    company_code = get_company_code_from_name(user.com)
    return company_code


@login_required(login_url='/login/')
def data_right_application_add(request):
    """数据权利申请页面"""

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 创建申请记录
                application = DataRightApplication(
                    applicant=request.POST.get('applicant'),
                    target_data_holder=request.POST.get('target_data_holder'),
                    target_data_name=request.POST.get('target_data_name'),
                    target_business_stage=request.POST.get('target_business_stage'),  # 改回原字段名

                    # 申请的权利类型
                    resource_holding_right='resource_holding_right' in request.POST,
                    processing_use_right='processing_use_right' in request.POST,
                    reauthorization_right='reauthorization_right' in request.POST,
                    redistribution_right='redistribution_right' in request.POST,
                    view_right='view_right' in request.POST,

                    application_reason=request.POST.get('application_reason'),
                    intended_use=request.POST.get('intended_use'),
                    intended_duration_start=request.POST.get('intended_duration_start'),
                    intended_duration_end=request.POST.get('intended_duration_end') if request.POST.get(
                        'intended_duration_end') else None,
                    is_permanent='is_permanent' in request.POST,

                    contact_person=request.POST.get('contact_person'),
                    contact_phone=request.POST.get('contact_phone'),
                    contact_email=request.POST.get('contact_email'),
                )
                application.save()

                # 记录申 请历史
                DataRightApplicationHistory.objects.create(
                    application=application,
                    action_type='submit',
                    action_user=request.user.username if hasattr(request.user, 'username') else '系统用户',
                    action_comments='提交申请'
                )
                messages.success(request, f'申请提交成功！申请编号：{application.application_id}')
                return redirect('data_confirmation_list')

        except Exception as e:
            messages.error(request, f'申请提交失败：{str(e)}')

    context = {
        'data_source_choices': DATA_SOURCE_CHOICES,
        'current_time': timezone.now(),
    }
    return render(request, 'data-confirmation-add.html', context)


@login_required(login_url='/login/')
def data_right_application_review(request, application_id):
    """数据权利申请审核页面"""
    application = get_object_or_404(DataRightApplication, application_id=application_id)

    # 权限检查：普通用户只能审核向自己申请的记录或查看自己的申请
    if not request.user.is_superuser:
        user_company_code = get_user_company_code(request.user)
        if user_company_code and (
                application.target_data_holder != user_company_code and application.applicant != user_company_code):
            raise Http404("您没有权限查看此申请")
        elif not user_company_code:
            raise Http404("用户公司信息异常")

    # 获取审核历史记录
    history_records = DataRightApplicationHistory.objects.filter(
        application=application
    ).exclude(action_type='submit')

    if request.method == 'POST':
        # 只有数据持有方或超级用户才能审核
        user_company_code = get_user_company_code(request.user)
        if not request.user.is_superuser and application.target_data_holder != user_company_code:
            messages.error(request, '您没有权限审核此申请')
            return redirect('data_right_application_list')

        try:
            with transaction.atomic():
                review_decision = request.POST.get('review_decision')
                review_comments = request.POST.get('review_comments')
                reviewer = request.user.username if hasattr(request.user, 'username') else '系统用户'

                if review_decision == 'approve':
                    application.status = 'approved'
                elif review_decision == 'reject':
                    application.status = 'rejected'
                else:
                    raise ValueError("无效的审核决定")

                application.reviewer = reviewer
                application.review_time = timezone.now()
                application.review_comments = review_comments
                application.save()

                DataRightApplicationHistory.objects.create(
                    application=application,
                    action_type='approve' if review_decision == 'approve' else 'reject',
                    action_user=reviewer,
                    action_comments=review_comments
                )

                record_status = 'active' if review_decision == 'approve' else 'rejected'

                data_right_record = DataRightRecord(
                    original_application=application,
                    data_name=application.target_data_name,
                    data_holder=application.target_data_holder,
                    right_recipient=application.applicant,
                    business_stage=application.target_business_stage,

                    granted_resource_holding_right=application.resource_holding_right if review_decision == 'approve' else False,
                    granted_processing_use_right=application.processing_use_right if review_decision == 'approve' else False,
                    granted_reauthorization_right=application.reauthorization_right if review_decision == 'approve' else False,
                    granted_redistribution_right=application.redistribution_right if review_decision == 'approve' else False,
                    granted_view_right=application.view_right if review_decision == 'approve' else False,

                    usage_start_date=application.intended_duration_start,
                    usage_end_date=application.intended_duration_end,
                    is_permanent_usage=application.is_permanent,

                    status=record_status,
                    approver=reviewer,
                    approval_time=timezone.now(),
                    approval_comments=review_comments,
                )
                data_right_record.save()

                # ========== 在messages之前添加状态同步代码 ==========
                # 同步更新项目表中的状态
                try:
                    if review_decision == 'approve':
                        project_status = '2'  # 审核通过
                        status_text = '审核通过'
                    elif review_decision == 'reject':
                        project_status = '3'  # 审核不通过
                        status_text = '审核不通过'
                    else:
                        project_status = None

                    if project_status:
                        # 使用项目名称和数据资产名称进行匹配
                        project_name = application.target_business_stage  # 项目名称
                        data_asset = application.target_data_name  # 数据资产名称

                        print(f"=== 同步项目状态 ===")
                        print(f"项目名称: '{project_name}'")
                        print(f"数据资产: '{data_asset}'")
                        print(f"目标状态: '{project_status}' ({status_text})")

                        # 构建匹配条件：项目名称 + 数据资产名称 + 待审核状态
                        query_str = f"projectName = '{project_name}' AND dataAsset = '{data_asset}'"
                        print(f"查询条件: {query_str}")

                        # 查询匹配的待审核项目
                        fields = "ID, projectName, dataDemand, dataOwner, dataAsset, currentStatus"
                        result = selecttable("pb8_ProjectAdd", fields=fields, constr=query_str)

                        if result:
                            print(f"找到 {len(result)} 个匹配的待审核项目:")
                            for i, row in enumerate(result):
                                print(
                                    f"  项目{i + 1}: ID={row[0]}, 项目名='{row[1]}', 申请方='{row[2]}', 持有方='{row[3]}', 资产='{row[4]}', 状态={row[5]}")

                            # 更新项目状态
                            update_str = f"currentStatus = '{project_status}'"
                            update_result = updatetable("pb8_ProjectAdd", update_str, query_str)

                            if update_result and update_result > 0:
                                print(f"✓ 成功更新 {update_result} 个项目状态为: {status_text}")
                                # =================== 在这里添加以下代码 ===================
                                # 同步更新 project_notarization 表
                                try:

                                    # 获取项目相关信息
                                    fields = 'ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay, currentStatus'
                                    order = 'ID DESC'
                                    project_result = selecttable('pb8_ProjectAdd', fields=fields, constr=query_str,
                                                                 order=order, limit=1)

                                    if project_result:
                                        ID, project_name, data_demander, data_owner, data_asset, security_level, trans_mode, currentStatus = project_result[0]

                                    anydata = {
                                        "data": "anydata"
                                    }

                                    response = requests.put('http://192.168.1.135:8080/datasharing/addRaw',
                                                            data=json.dumps(anydata),
                                                            headers={'Content-Type': 'application/json'})

                                    if response.status_code == 200:
                                        print("区块链接口响应:", response.json())
                                        # 解析区块链返回的 payload
                                        payload = json.loads(response.json().get('payload', '{}'))
                                        tx_time = payload.get('txTime')
                                        tx_id = payload.get('txID')
                                        tx_hash = payload.get('txHash')



                                        # 构建插入数据的字符串
                                        pro_js = f"'{ID}','{project_name}','{data_demander}','{data_owner}','{data_asset}','{status_text}','{security_level}','{trans_mode}','{tx_time}','{tx_id}','{tx_hash}'"
                                        # 调用 inserttable 函数插入数据到 project_notarization 表
                                        inserttable(pro_js, tablename="project_notarization",
                                                    con1="projectId,projectName,assetDemander,assetOwner,assetName,status,assetLevel,assetSharingType, tranasctionTime,tranasctionId,hashDigest")


                                except Exception as e:
                                    print(f"❌ 同步存证表状态失败: {str(e)}")
                                    import traceback
                                    traceback.print_exc()
                                # =================== 添加代码结束 ===================

                            else:
                                print(f"⚠️ 更新失败，返回值: {update_result}")

                        else:
                            print("❌ 没有找到匹配的待审核项目")

                            # 显示相关的项目数据用于调试
                            print(f"\n=== 查找相关项目（忽略状态） ===")
                            debug_query = f"projectName = '{project_name}' AND dataAsset = '{data_asset}' AND isDeleted != 'Y'"
                            debug_result = selecttable("pb8_ProjectAdd", fields=fields, constr=debug_query)

                            if debug_result:
                                print("找到相同项目名称和数据资产的项目:")
                                for row in debug_result:
                                    print(f"  ID={row[0]}, 状态={row[5]} (需要状态=1)")
                            else:
                                print("没有找到相同项目名称和数据资产的项目")

                                # 显示最近的项目用于对比
                                print(f"\n=== 最近的项目记录 ===")
                                recent_result = selecttable("pb8_ProjectAdd",
                                                            fields="ID, projectName, dataAsset, currentStatus",
                                                            constr="isDeleted != 'Y' ORDER BY ID DESC LIMIT 5")
                                if recent_result:
                                    for row in recent_result:
                                        print(f"  ID={row[0]}, 项目='{row[1]}', 资产='{row[2]}', 状态={row[3]}")

                except Exception as e:
                    print(f"❌ 同步项目状态失败: {str(e)}")
                    import traceback
                    traceback.print_exc()
                # =============================================

                if review_decision == 'approve':
                    messages.success(request, f'审核通过！已生成数据确权记录：{data_right_record.record_id}')
                else:
                    messages.success(request, f'审核已拒绝！已生成拒绝记录：{data_right_record.record_id}')

                return redirect('data_confirmation_list')

        except Exception as e:
            messages.error(request, f'审核失败：{str(e)}')

    # 将choices转换为字典
    data_source_dict = dict(DATA_SOURCE_CHOICES)

    context = {
        'application': application,
        'history_records': history_records,
        'data_source_choices': DATA_SOURCE_CHOICES,
        'data_source_dict': data_source_dict,
        'current_user': request.user.username if hasattr(request.user, 'username') else '系统用户',
        'current_time': timezone.now(),
        'is_superuser': request.user.is_superuser,
        'can_review': request.user.is_superuser or application.target_data_holder == get_user_company_code(
            request.user),
    }
    return render(request, 'data-right-application-review.html', context)



@login_required(login_url='/login/')
def data_confirmation_list(request):
    """数据确权记录列表页面"""

    # 根据用户权限获取记录
    if request.user.is_superuser:
        # 超级用户可以看到所有记录
        records = DataRightRecord.objects.all()
    else:
        # 普通用户只能看到自己相关的记录
        user_company_code = get_user_company_code(request.user)

        if user_company_code:
            from django.db.models import Q
            records = DataRightRecord.objects.filter(
                Q(right_recipient=user_company_code) | Q(data_holder=user_company_code)
            )
        else:
            records = DataRightRecord.objects.none()

    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        records = records.filter(data_name__icontains=search_query)

    # 状态过滤
    status_filter = request.GET.get('status', '')
    if status_filter:
        records = records.filter(status=status_filter)

    # 数据持有方过滤
    holder_filter = request.GET.get('holder', '')
    if holder_filter:
        records = records.filter(data_holder=holder_filter)

    # 权利获得方过滤
    recipient_filter = request.GET.get('recipient', '')
    if recipient_filter:
        records = records.filter(right_recipient=recipient_filter)

    # 更新过期状态
    for record in records:
        if record.is_expired() and record.status == 'active':
            record.status = 'expired'
            record.save()

    # 分页
    paginator = Paginator(records, 10)  # 每页显示10条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 将choices转换为字典
    data_source_dict = dict(DATA_SOURCE_CHOICES)
    #business_stage_dict = dict(BUSINESS_STAGE_CHOICES)
    record_status_dict = dict(DataRightRecord.RECORD_STATUS_CHOICES)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'holder_filter': holder_filter,
        'recipient_filter': recipient_filter,
        'data_source_choices': DATA_SOURCE_CHOICES,
        #'business_stage_choices': BUSINESS_STAGE_CHOICES,
        'record_status_choices': DataRightRecord.RECORD_STATUS_CHOICES,
        # 添加字典版本供模板使用
        'data_source_dict': data_source_dict,
        #'business_stage_dict': business_stage_dict,
        'record_status_dict': record_status_dict,
        # 添加用户权限信息
        'is_superuser': request.user.is_superuser,
        'current_user': request.user,
    }
    return render(request, 'data-confirmation.html', context)

@login_required(login_url='/login/')
def data_confirmation_detail(request, record_id):
    """数据确权记录详情页面"""
    record = get_object_or_404(DataRightRecord, record_id=record_id)

    # 权限检查：普通用户只能查看自己相关的记录
    if not request.user.is_superuser:
        user_company_code = get_user_company_code(request.user)
        if user_company_code and (
                record.right_recipient != user_company_code and record.data_holder != user_company_code):
            raise Http404("您没有权限查看此记录")
        elif not user_company_code:
            raise Http404("用户公司信息异常")

    # 获取原始申请的历史记录
    application_history = DataRightApplicationHistory.objects.filter(
        application=record.original_application
    )

    context = {
        'record': record,
        'application_history': application_history,
        'data_source_choices': dict(DATA_SOURCE_CHOICES),
        #'business_stage_choices': dict(BUSINESS_STAGE_CHOICES),
        'current_user': request.user,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'data-confirmation-detail.html', context)


@login_required(login_url='/login/')
def data_right_application_list(request):
    """数据权利申请列表页面（用于审核人员查看待审核申请）"""

    # 根据用户权限获取申请记录
    if request.user.is_superuser:
        # 超级用户可以看到所有申请
        applications = DataRightApplication.objects.all()
    else:
        # 普通用户只能看到相关的申请
        user_company_code = get_user_company_code(request.user)

        if user_company_code:
            from django.db.models import Q
            applications = DataRightApplication.objects.filter(
                Q(target_data_holder=user_company_code) |  # 向自己申请的（需要审核的）
                Q(applicant=user_company_code)  # 自己提交的申请
            )
        else:
            applications = DataRightApplication.objects.none()

    # 状态过滤，默认显示待审核的申请
    status_filter = request.GET.get('status', 'pending')
    if status_filter:
        applications = applications.filter(status=status_filter)

    # 申请方过滤
    applicant_filter = request.GET.get('applicant', '')
    if applicant_filter:
        applications = applications.filter(applicant=applicant_filter)

    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(target_data_name__icontains=search_query)

    # 分页
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'applicant_filter': applicant_filter,
        'data_source_choices': DATA_SOURCE_CHOICES,
        'application_status_choices': DataRightApplication.APPLICATION_STATUS_CHOICES,
        # 添加用户权限信息
        'is_superuser': request.user.is_superuser,
        'current_user': request.user,
    }
    return render(request, 'data-right-application-list.html', context)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def delete_data_confirmation_record(request, record_id):
    """删除数据确权记录"""
    try:
        record = get_object_or_404(DataRightRecord, record_id=record_id)

        # 权限检查：普通用户只能删除自己相关的记录
        if not request.user.is_superuser:
            user_company_code = get_user_company_code(request.user)
            if not user_company_code:
                return JsonResponse({
                    'success': False,
                    'message': '用户公司信息异常'
                }, status=403)

            if record.right_recipient != user_company_code and record.data_holder != user_company_code:
                return JsonResponse({
                    'success': False,
                    'message': '您没有权限删除此记录'
                }, status=403)

        # 移除状态限制 - 现在允许删除所有状态的记录
        # 可选：根据不同状态给出不同的提示
        status_messages = {
            'active': '生效中的确权记录',
            'expired': '已过期的确权记录',
            'revoked': '已撤销的确权记录',
            'rejected': '被拒绝的确权记录'
        }

        record_status_desc = status_messages.get(record.status, '确权记录')

        # 记录被删除的信息用于日志
        record_info = f"{record.record_id} - {record.data_name} ({record_status_desc})"

        # 删除记录
        record.delete()

        messages.success(request, f'已成功删除{record_status_desc}：{record.data_name}')
        return JsonResponse({
            'success': True,
            'message': f'成功删除{record_status_desc}'
        })

    except DataRightRecord.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '记录不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败：{str(e)}'
        }, status=500)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def batch_delete_data_confirmation_records(request):
    """批量删除数据确权记录"""
    try:
        selected_records = request.POST.getlist('selected_records')
        if not selected_records:
            return JsonResponse({
                'success': False,
                'message': '未选择要删除的记录'
            }, status=400)

        user_company_code = get_user_company_code(request.user)
        deleted_count = 0
        failed_records = []

        for record_id in selected_records:
            try:
                record = get_object_or_404(DataRightRecord, record_id=record_id)

                # 权限检查
                if not request.user.is_superuser:
                    if not user_company_code:
                        failed_records.append(f"{record_id}(权限异常)")
                        continue

                    if record.right_recipient != user_company_code and record.data_holder != user_company_code:
                        failed_records.append(f"{record_id}(无权限)")
                        continue

                # 删除记录（不再检查状态）
                record.delete()
                deleted_count += 1

            except DataRightRecord.DoesNotExist:
                failed_records.append(f"{record_id}(不存在)")
            except Exception as e:
                failed_records.append(f"{record_id}(删除失败)")

        message = f'成功删除 {deleted_count} 条记录'
        if failed_records:
            message += f'，失败 {len(failed_records)} 条：{", ".join(failed_records)}'

        messages.success(request, message)
        return JsonResponse({
            'success': True,
            'message': message,
            'deleted_count': deleted_count,
            'failed_count': len(failed_records)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'批量删除失败：{str(e)}'
        }, status=500)

# AJAX接口函数
@login_required(login_url='/login/')
def get_application_detail(request, application_id):
    """获取申请详情的AJAX接口"""
    try:
        application = DataRightApplication.objects.get(application_id=application_id)

        # 计算使用期限显示
        if application.is_permanent:
            usage_period = "永久使用"
        elif application.intended_duration_end:
            usage_period = f"{application.intended_duration_start} 至 {application.intended_duration_end}"
        else:
            usage_period = f"自 {application.intended_duration_start} 起"

        data = {
            'application_id': application.application_id,
            'applicant': application.get_applicant_display(),
            'target_data_holder': application.get_target_data_holder_display(),
            'target_data_name': application.target_data_name,
            'target_business_stage': application.get_target_business_stage_display(),
            'applied_rights': application.get_applied_rights_display(),
            'application_reason': application.application_reason,
            'intended_use': application.intended_use,
            'usage_period': usage_period,
            'contact_person': application.contact_person,
            'contact_phone': application.contact_phone,
            'contact_email': application.contact_email,
            'status': application.get_status_display(),
            'created_at': application.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        return JsonResponse({'success': True, 'data': data})
    except DataRightApplication.DoesNotExist:
        return JsonResponse({'success': False, 'message': '申请不存在'})
# 数据确权相关视图函数AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
@login_required
def asset_field_dimension(request, asset_id):
    # 获取数据资产
    asset = get_object_or_404(DataAsset, assetID=asset_id, assetOwner=request.user.com)

    # 获取所有机构列表（排除当前用户所属机构）
    companies = LoginUser.objects.exclude(com=request.user.com).values_list('com', flat=True).distinct()

    # 获取该资产的所有维度设置
    dimensions = AssetDimension.objects.filter(asset=asset)
    dimension_details = AssetDimensionDetail.objects.filter(asset=asset)

    # 获取所有字段名（从现有维度设置中提取）
    field_names = set(dimensions.values_list('field_name', flat=True))

    return render(request, 'asset_field_dimension.html', {
        'asset': asset,
        'companies': companies,
        'field_names': sorted(field_names),
        'dimensions': dimensions,
        'dimension_details': dimension_details
    })


@csrf_exempt
@login_required
def get_dimension_detail(request, dimension_id):
    try:
        dimension = AssetDimension.objects.get(id=dimension_id)
        # 检查权限
        if dimension.asset.assetOwner != request.user.com:
            return JsonResponse({'success': False, 'message': '没有权限'})

        # 获取时间维度明细
        time_detail = AssetDimensionDetail.objects.filter(
            asset=dimension.asset,
            target_company=dimension.target_company,
            field_name=dimension.field_name,
            sub_dimension='time'
        ).first()

        # 获取空间维度明细
        space_detail = AssetDimensionDetail.objects.filter(
            asset=dimension.asset,
            target_company=dimension.target_company,
            field_name=dimension.field_name,
            sub_dimension='space'
        ).first()

        return JsonResponse({
            'success': True,
            'dimension': {
                'id': dimension.id,
                'field_name': dimension.field_name,
                'target_company': dimension.target_company,
                'security_dimension': dimension.security_dimension,
                'time_dimension': dimension.time_dimension,
                'space_dimension': dimension.space_dimension,
                'business_dimension': dimension.business_dimension,
            },
            'time_detail': time_detail.sub_dimension_detail if time_detail else '',
            'space_detail': space_detail.sub_dimension_detail if space_detail else ''
        })
    except AssetDimension.DoesNotExist:
        return JsonResponse({'success': False, 'message': '维度设置不存在'})

@csrf_exempt
@login_required
def save_dimension(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asset = get_object_or_404(DataAsset, assetID=data.get('asset_id'))
            # 检查权限
            if asset.assetOwner != request.user.com:
                return JsonResponse({'success': False, 'message': '没有权限'})

            # 如果是编辑现有维度
            if data.get('dimension_id'):
                dimension = AssetDimension.objects.get(id=data.get('dimension_id'))
                # 检查权限
                if dimension.asset.assetOwner != request.user.com:
                    return JsonResponse({'success': False, 'message': '没有权限'})

                # 检查目标机构是否改变
                old_target_company = dimension.target_company
                new_target_company = data.get('target_company')

                # 如果目标机构改变，需要删除旧的明细记录
                if old_target_company != new_target_company:
                    AssetDimensionDetail.objects.filter(
                        asset=asset,
                        target_company=old_target_company,
                        field_name=dimension.field_name
                    ).delete()
            else:
                # 创建新维度
                dimension = AssetDimension(
                    asset=asset,
                    user=request.user,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name')
                )

            # 更新维度字段
            dimension.target_company = data.get('target_company')  # 确保更新目标机构
            dimension.security_dimension = data.get('security_dimension')
            dimension.time_dimension = data.get('time_dimension')
            dimension.space_dimension = data.get('space_dimension')
            dimension.business_dimension = data.get('business_dimension')
            dimension.save()

            # 处理时间维度明细
            time_detail = data.get('time_detail')
            if time_detail and data.get('time_dimension'):
                # 删除旧的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='time'
                ).delete()

                # 创建新的明细记录
                AssetDimensionDetail.objects.create(
                    asset=asset,
                    user=request.user,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='time',
                    sub_dimension_detail=time_detail
                )
            elif not data.get('time_dimension'):
                # 如果没有选择时间维度，删除相关的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='time'
                ).delete()

            # 处理空间维度明细
            space_detail = data.get('space_detail')
            if space_detail and data.get('space_dimension'):
                # 删除旧的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='space'
                ).delete()

                # 创建新的明细记录
                AssetDimensionDetail.objects.create(
                    asset=asset,
                    user=request.user,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='space',
                    sub_dimension_detail=space_detail
                )
            elif not data.get('space_dimension'):
                # 如果没有选择空间维度，删除相关的明细记录
                AssetDimensionDetail.objects.filter(
                    asset=asset,
                    target_company=data.get('target_company'),
                    field_name=data.get('field_name'),
                    sub_dimension='space'
                ).delete()

            return JsonResponse({'success': True, 'message': '保存成功'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '无效的请求方法'})

@csrf_exempt
@login_required
def delete_dimension(request, dimension_id):
    if request.method == 'POST':
        try:
            dimension = AssetDimension.objects.get(id=dimension_id)
            # 检查权限
            if dimension.asset.assetOwner != request.user.com:
                return JsonResponse({'success': False, 'message': '没有权限'})

            # 删除相关的明细记录
            AssetDimensionDetail.objects.filter(
                asset=dimension.asset,
                target_company=dimension.target_company,
                field_name=dimension.field_name
            ).delete()

            # 删除主记录
            dimension.delete()

            return JsonResponse({'success': True, 'message': '删除成功'})
        except AssetDimension.DoesNotExist:
            return JsonResponse({'success': False, 'message': '维度设置不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '无效的请求方法'})


# 添加字段的视图
@csrf_exempt
@login_required
def add_field(request, asset_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asset = get_object_or_404(DataAsset, assetID=asset_id)
            # 检查权限
            if asset.assetOwner != request.user.com:
                return JsonResponse({'success': False, 'message': '没有权限'})

            field_name = data.get('field_name')

            # 检查字段是否已存在
            if field_name in set(AssetDimension.objects.filter(asset=asset).values_list('field_name', flat=True)):
                return JsonResponse({'success': False, 'message': '字段已存在'})

            # 返回成功，字段会在前端动态添加
            return JsonResponse({
                'success': True,
                'message': '字段添加成功',
                'field_name': field_name
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '无效的请求方法'})
