import torch
# -*- coding:utf-8 -*-
import json
import subprocess

import corsheaders
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from huggingface_hub.utils import parse_datetime
from sqlalchemy.sql.functions import current_user

from .models import LoginUser, AssetRecord
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

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

@login_required(login_url='/login/')
def interface_add(request):
    return render(request, 'interface-add.html')

@login_required(login_url='/login/')
def interface_edit(request):
    return render(request, 'interface-edit.html')

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
    return render(request, 'establish-project.html')
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
    return render(request, 'project_notarization.html')

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
    # 从请求体中获取数据
    # data = json.loads(request.body)
    # print(data)
    webName = request.body.decode('utf-8')  # 转换为字符串
    # projs = json.loads(proobj)
    # webName = projs[0]["webName"]
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

    # 在asset_record这个表里新建一条记录
    asset_js = "'" + assetName + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + assetPath + "','已上传','已完成','调用数据接口','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(asset_js, tablename="asset_record",
                con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")
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
    asset_js = "'" + assetName + "','" + assetOwner + "','" + assetFormat + "','" + assetLevel + "','" + assetPath + "','未上传','已上传','上传数据接口','" + tx_time + "','" + tx_id + "','" + tx_hash + "'"
    inserttable(asset_js, tablename="asset_record", con1="assetName,assetOwner,assetFormat,assetLevel,assetPath,star_status,end_status,operation,txTime,txID,txHash")
    # 在webinterface这个表里新建一条记录
    pro_js = "'" + webname + "','" + weburl + "','" + webprotocol + "','" + webtype + "','" + datatype + "','" + comallowed + "','" + projectName + "'"
    inserttable(pro_js, tablename="webinterface", con1="webname,weburl,webprotocol,webtype,datatype,comallowed,projectName")
    return JsonResponse({'status': 0})

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
from django.contrib import messages





#
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import DataAsset
# import requests
# import json
# import logging
#


# def add_data_asset(request):
#     if request.method == 'POST':
#         try:
#             # 创建数据资产
#             asset = DataAsset.objects.create(
#                 assetName=request.POST['assetName'],
#                 assetOwner=request.POST['assetOwner'],
#                 description=request.POST['description'],
#                 assetFormat=request.POST['assetFormat'],
#                 assetLevel=request.POST['assetLevel'],
#                 status=request.POST['status'],
#                 assetPath=request.POST['assetPath'],
#             )
#
#             # 上传到区块链
#             blockchain_url = "http://202.112.151.253:8080/datasharing/addRaw"
#             payload = {
#                 "assetID": str(asset.assetID),
#                 "assetName": asset.assetName,
#                 "assetOwner": asset.assetOwner,
#                 "assetField": asset.description,
#                 "assetFormat": asset.assetFormat,
#                 "assetLevel": asset.assetLevel,
#                 "assetPath": asset.assetPath,
#                 "assetRole": "test"  # 根据需求调整
#             }
#             headers = {'Content-Type': 'application/json'}
#
#             response = requests.put(blockchain_url, data=json.dumps(payload), headers=headers)
#             if response.status_code == 200:
#                 # 区块链上传成功
#                 messages.success(request, '数据资产已成功添加并上传到区块链！')
#                 return redirect('data_asset_list')  # 修正：使用 URL 名称
#             else:
#                 # 区块链上传失败，删除已创建的数据资产
#                 asset.delete()
#                 logger.error(f"区块链上传失败，状态码: {response.status_code}, 响应内容: {response.text}")
#                 messages.error(request, f'区块链上传失败，状态码: {response.status_code}, 响应内容: {response.text}')
#                 return render(request, 'data_asset_add.html')
#         except Exception as e:
#             # 区块链请求异常，删除已创建的数据资产
#             if 'asset' in locals():
#                 asset.delete()
#             logger.error(f"区块链请求失败: {str(e)}")
#             messages.error(request, f'区块链请求失败: {str(e)}')
#             return render(request, 'data_asset_add.html')
#
#     return render(request, 'data_asset_add.html')
from django.utils import timezone

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
                status=request.POST['status'],
                assetPath=request.POST['assetPath'],
            )

            # 创建初始存证记录（状态：无 → 未上传）
            record = AssetRecord.objects.create(
                assetName=asset.assetName,
                assetOwner=asset.assetOwner,
                assetFormat=asset.assetFormat,
                assetLevel=asset.assetLevel,
                assetPath=asset.assetPath,
                star_status='无',
                end_status='未上传',
                operation='新增数据资产项',
                txTime=None,
                txID='',
                txHash=''
            )

            # 上传到区块链
            blockchain_url = "http://202.112.151.253:8080/datasharing/addRaw"
            payload = {
                "assetID": str(asset.assetID),
                "assetName": asset.assetName,
                "assetOwner": asset.assetOwner,
                # "assetField": asset.description,
                "assetFormat": asset.assetFormat,
                "assetLevel": asset.assetLevel,
                "assetPath": asset.assetPath,
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
            asset.status = request.POST.get('status')
            asset.assetPath = request.POST.get('assetPath')
            asset.save()

            # 创建存证记录（不调用区块链）
            AssetRecord.objects.create(
                assetName=asset.assetName,
                assetOwner=asset.assetOwner,
                assetFormat=asset.assetFormat,
                assetLevel=asset.assetLevel,
                assetPath=asset.assetPath,
                star_status='无',  # 旧状态
                end_status='未上传',  # 新状态
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
                    assetLevel=asset.assetLevel,
                    assetPath=asset.assetPath,
                    star_status='无',
                    end_status='未上传',
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
# def fetch_and_save_asset_data(request):
#
#     # 接口地址
#     url = "http://202.112.151.253:8080/datasharing/addRaw"
#     # headers = {
#     #     "Authorization": "your_auth_token",  # 替换为实际的授权令牌
#     #     "Content-Type": "application/json"
#     # }
#     headers = {'Content-Type': 'application/json'}
#
#     # 发送请求到接口
#     response = requests.put(url, headers=headers)
#     logger.info("Sending PUT request to URL: %s", url)
#     logger.info("Response status code: %s", response.status_code)
#     logger.info("Response data: %s", response.json())
#     if response.status_code == 200:
#         response_data = response.json()
#
#         # 假设接口返回的数据是一个列表
#         for item in response_data:
#             # 解析每条数据
#             tx_time = datetime.strptime(item.get("txTime"), "%Y-%m-%d %H:%M:%S")  # 解析时间
#             asset_record = AssetRecord(
#                 assetName=item.get("assetName"),
#                 assetOwner=item.get("assetOwner"),
#                 assetField=item.get("assetField"),
#                 assetFormat=item.get("assetFormat"),
#                 assetLevel=item.get("assetLevel"),
#                 assetPath=item.get("assetPath"),
#                 txTime=tx_time,
#                 txID=item.get("txID"),
#                 txHash=item.get("txHash"),
#                 status=item.get("status")
#             )
#             asset_record.save()  # 保存到数据库
#
#         return JsonResponse({"status": "success", "message": "数据已成功获取并保存"})
#     else:
#         return JsonResponse({"status": "error", "message": "无法从接口获取数据"}, status=400)
@login_required(login_url='/login/')
# def asset_record_list(request):
#     # 从数据库中获取所有资产记录
#     current_user=request.user
#     records = AssetRecord.objects.filter(assetOwner=current_user)
#     # 渲染模板并传递数据
#     # return render(request, 'data_asset_record.html', {'records': records})
#     return render(request, 'data_asset_record.html', {
#         'records': records,
#         'current_user': request.user  # 传递用户对象到模板
#     })
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
    notarizationlist = selecttable("project_notarization", "id, projectName, assetDemander, assetOwner, assetName, status, assetLevel, assetSharingType, operations,tranasctionId, tranasctionTime, hashDigest", '', '', '', '')
    print('查找成功')
    print(notarizationlist)
    return JsonResponse({'status': 0, 'data': notarizationlist, 'msg': 'success'})

#根据项目名称查找存证信息
def search_notarization_by_projectname(request):
    # 获取查询参数
    project_name = request.GET.get('project_name', '')

    # 按项目名称模糊查询
    if project_name:
        # 构造查询条件
        condition = f"projectName LIKE '%{project_name}%'"
        notarizationlist = selecttable(
            "project_notarization",
            "id, projectName, assetDemander, assetOwner, assetName, status, assetLevel, assetSharingType, operations, tranasctionId, tranasctionTime, hashDigest",
            condition,  # 添加查询条件
            '',
            '',
            ''
        )
    else:
        # 如果没有输入项目名称，返回所有数据
        notarizationlist = selecttable(
            "project_notarization",
            "id, projectName, assetDemander, assetOwner, assetName, status, assetLevel, assetSharingType, operations, tranasctionId, tranasctionTime, hashDigest",
            '',
            '',
            '',
            ''
        )

    print('查找成功')
    print(notarizationlist)
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

def submit_project(request):
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

        fields = 'ID, projectName, dataDemand, dataOwner, dataAsset, dataSecurity, shareWay'
        order = 'ID DESC'
        result = selecttable('pb8_ProjectAdd', fields=fields, constr=constr, order=order, limit=1)

        if result:
            ID, project_name, data_demander, data_owner, data_asset, security_level, trans_mode = result[0]

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
                response = requests.put('http://202.112.151.253:8080/datasharing/addRaw', data=blockchainDataStr, headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    print("区块链接口响应:", response.json())
                    return JsonResponse({'status': 'ok','message': '区块链接口调用成功'})
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
        # 构建查询条件
        constr = f"isDeleted != 'Y' AND dataDemand = '{dataDemand}'"
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

        if projectName and dataDemand and dataOwner and dataAsset:
            updatstr = "isDeleted = 'Y'"
            constr = f"projectName = '{projectName}' and dataDemand = '{dataDemand}' and dataOwner = '{dataOwner}' and dataAsset = '{dataAsset}'"
            result = updatetable('pb8_ProjectAdd', updatstr, constr)
            if result == 1:
                return JsonResponse({'status': '0','message': '删除成功'})
            else:
                return JsonResponse({'status': '1','message': '删除失败'})
        else:
            return JsonResponse({'status': '1','message': '缺少必要的参数'})
    else:
        return JsonResponse({'status': '1','message': '请求方法错误，仅支持POST请求'})


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
                return JsonResponse({'status': '1', 'message': '缺少必要参数'})

            # 构建更新字符串
            update_str = f"currentStatus = '{currentStatus}'"
            condition_str = f"id = {id}"

            # 调用 updatetable 方法
            result = updatetable("pb8_ProjectAdd", update_str, condition_str)

            if result == 1:
                return JsonResponse({'status': '0', 'message': '审核状态更新成功'})
            else:
                return JsonResponse({'status': '1', 'message': '审核状态更新失败'})

    except Exception as e:
        return JsonResponse({'status': '1', 'message': f'出现错误: {str(e)}'})

def submit_project(request):
    try:
        if request.method == 'POST':
            # 从 POST 请求中获取项目 ID
            id = request.POST.get('id')
            # 设定提交后的状态为 1
            currentStatus = '1'

            # 检查是否提供了必要的参数
            if id is None:
                return JsonResponse({'status': '1', 'message': '缺少必要参数: id'})

            # 构建更新字符串
            update_str = f"currentStatus = '{currentStatus}'"
            condition_str = f"id = {id}"

            # 调用 updatetable 方法
            result = updatetable("pb8_ProjectAdd", update_str, condition_str)

            if result == 1:
                return JsonResponse({'status': '0', 'message': '项目提交成功'})
            else:
                return JsonResponse({'status': '1', 'message': '项目提交失败'})

    except Exception as e:
        return JsonResponse({'status': '1', 'message': f'出现错误: {str(e)}'})

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
