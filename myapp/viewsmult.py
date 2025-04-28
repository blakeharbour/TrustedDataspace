# -*- coding:utf-8 -*-
import paramiko
import torch
import requests
import socket
import pickle

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from io import BytesIO
from torch.utils.tensorboard import SummaryWriter
import os
import json
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from sklearn.datasets import load_iris
import pandas as pd
from sklearn.model_selection import train_test_split
from django.views.decorators.csrf import csrf_exempt
import base64

from django.forms.models import *
import pymysql


# from hotel import settings
from . import models
from .fed_PU_sci1203 import maincf

from .myjob import *
from .service import TensorBoardService
import numpy as np
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import corsheaders

from myapp.fed_PU_sci1203.splitNN import SyNet_client_coleft, SyNet_client_coright, SyNet_server_co

# 参与者列表
def multguest_list(request):
    return render(request, 'multguest-list.html')


# 参与者添加
def multguest_add(request):
    return render(request, 'multguest-add.html')


# 创建参与者
def createmultguest(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    ip = projs[0]["ip"]
    remark = projs[0]["remark"]
    agreement = projs[0]["agreement"]
    # username = "lucy"
    # password = "123456"
    # phone="12345687"
    # remark=""
    # print(res_dict)
    # 在userlist这个表里新建一条记录
    pro_js = "'" + guest + "','" + ip + "','" + remark + "','" + agreement + "'"
    inserttable(pro_js, tablename="multguest_list", con1="guest,ip,remark,agreement")

    print('xinzengchenggong')
    return JsonResponse({'status': 0})


# 查找参与者
def searchmultguest(request):
    guestlist = selecttable("multguest_list", "id,guest,ip,remark,agreement,testtime,statu", '', '', '', '')
    print('查找成功')
    print(guestlist)
    return JsonResponse({'status': 0, 'data': guestlist, 'msg': 'success'})


def multmodel_application_result_search(request):
    resultlist = selecttable("multmodel_result", "id,model,modeldes,resultoutpath,resultpltpath,predictlabel", '', '',
                             '', '')
    print('模型应用结果')
    print(resultlist)
    return JsonResponse({'status': 0, 'data': resultlist, 'msg': 'success'})


def editmultguest(guestlist):
    # userid=None
    # username='lusd'
    # password = "123456"
    # phone="12345687"
    # remark=""
    result = 0
    print(guestlist)
    pro_js = "statu=" + "'" + guestlist[5] + "',testtime=" + "'" + guestlist[4] + "'"
    filterstr = "id=" + "'" + str(guestlist[0]) + "'"
    result = updatetable("multguest_list", pro_js, filterstr)
    if result == 1:
        print('xiugaichenggong')
    if result == 0:
        print('xiugaishibai')
    return result


# 测试参与者

def multpingtest(request):
    print('开始')

    if request.method == 'POST':
        proobj = request.body
        projs = json.loads(proobj)
        id = projs[0]["id"]
        print(id)
        guestlist = selecttable("multguest_list", "id,guest,ip,remark,agreement,testtime,statu", "id=" + "'" + id + "'",
                                '', '', '')

        print('ping查找成功')
        print(guestlist)
        ip_address = guestlist[0][2]
        # ip_address='192.168.1.121'
        print(ip_address)
        # 执行ping命令
        # 执行 ping 命令
        guestlist_list = []
        try:
            print('开始')
            subprocess.run(['ping', '-c', '4', ip_address], check=True)
            print('结束')

            # subprocess.run(['ping', '-n', '4', ip_address], check=True)
            print(guestlist[0][0])
            guestlist_list.append(guestlist[0][0])
            guestlist_list.append(guestlist[0][1])
            guestlist_list.append(guestlist[0][2])
            guestlist_list.append(guestlist[0][3])
            guestlist_list.append(str(datetime.now().time()))  # Append the current time as a string
            guestlist_list.append("success")

            result_edit = editmultguest(guestlist_list)
            if result_edit == 1:
                return JsonResponse({'status': '0', 'data': 'success！', 'msg': 'success'})
            if result_edit == 0:
                return JsonResponse({'status': '1', 'data': 'fail！', 'msg': 'fail'})

        except subprocess.CalledProcessError:
            guestlist_list.append(guestlist[0][0])
            guestlist_list.append(guestlist[0][1])
            guestlist_list.append(guestlist[0][2])
            guestlist_list.append(guestlist[0][3])
            guestlist_list.append(str(datetime.now().time()))  # Append the current time as a string
            guestlist_list.append("fail")
            editmultguest(guestlist_list)
            return JsonResponse({'status': '2', 'data': 'fail！', 'msg': 'fail'})

    return JsonResponse({'status': '2', 'data': 'fail！', 'msg': 'fail'})


# 查找公共协议
def getagreement(request):
    if request.method == 'POST':
        proobj = request.body
        projs = json.loads(proobj)
        ip = projs[0]["ip"]
        if ip:
            # 调用港口虚拟机的方法
            # agreement = '同态加密,秘密分享'
            # print(agreement)
            result=call_port_method(ip)
            agreement = result["agreement"]
            guest='rail'
            railagreementlist = selecttable("multguest_list", "agreement", "guest=" + "'" + guest + "'", '', '', '')
            # 从元组中提取字符串
            if railagreementlist:
                railagreement = railagreementlist[0][0]  # 获取第一行

            # 将字符串分割为列表
            agreement_list = agreement.split(',')
            print(agreement_list)
            railagreement_list = railagreement.split(',')
            print(railagreement_list)
            # # 使用集合操作计算交集
            intersection = set(agreement_list) & set(railagreement_list)
            #
            if intersection:
                # 存在交集
                intersection_str = ','.join(intersection)
                pro_js = "agreement=" + "'" + intersection_str + "'"
                filterstr = "ip=" + "'" + ip + "'"
                updatetable("multguest_list", pro_js, filterstr)
                print("共有协议为:", intersection_str)
                return JsonResponse({'agreement': intersection_str})
            else:
                # 不存在交集
                print("没有共有协议")
                return JsonResponse({'agreement': '没有共有协议，无法添加外部协作者'})
            # 将交集转换为逗号分隔的字符串
    return JsonResponse({'agreement': '0'})


def call_port_method(ip):
    harbor_port = 8000

    url = f'http://{ip}:{harbor_port}/port_method/'
    data = {"ip": ip}  # 你需要根据实际情况传递的数据
    json_data = json.dumps(data, ensure_ascii=False)
    response = requests.post(url, json=json_data)

    result = response.json()  # 处理港口虚拟机返回的结果

    return result

@csrf_exempt
def port_method(request):
    # data = json.loads(request.body)
    # ip = data.get("ip")
    # query = f"ip = {ip}"
    data = '同态加密,秘密分享'
    print(data)
    if data:
        return JsonResponse({'agreement': data})
    else:
        return JsonResponse({'agreement': '未输入正确ip'})


def getMultInfoById(request):
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    id = projs.get("id")

    filterstr = "id= " + "'" + id + "'"
    Infolist = selecttable("multguest_list", "id,guest,ip,remark,agreement,testtime,statu"
                               , filterstr, '', '', '')
    print(Infolist)
    # (('123',),)
    if Infolist != ():
        return JsonResponse(Infolist)
    else:
        return JsonResponse([])


def multguestedit(request):
    return render(request, 'multguestedit.html')


# 查找模型
def searchmultmodel(request):
    modellist = selecttable("multmodel_list",
                            "id,guest,model,goal,status,agreement,applicationsta,preci,recall1,error1,val_loss,modelurl,preci_url,recall1_url,error1_url,val_loss_url",
                            '', '', '', '')
    print('查找成功')
    print(modellist)
    return JsonResponse({'status': 0, 'data': modellist, 'msg': 'success'})


# 查找模型_appl
def searchmultmodel_appl(request):
    modellist = selecttable("multmodel_list", "id,guest,model,goal,applicationsta,agreement", '', '', '', '')
    print('查找成功')
    print(modellist)
    return JsonResponse({'status': 0, 'data': modellist, 'msg': 'success'})


# 模型搜索
def multmodel_list(request):
    return render(request, 'multmodel-list.html')


# 增加模型
def multmodel_add(request):
    return render(request, 'multmodel-add.html')


# 模型应用
def multmodel_main(request):
    return render(request, 'multmodel_main.html')


def multapplication_result(request):
    return render(request, 'multapplication_result.html')


def multmodel_application(request):
    return render(request, 'multmodel_application.html')


# 查找公共协议
def getmodelagreement(request):
    if request.method == 'POST':
        proobj = request.body
        projs = json.loads(proobj)
        guestList = projs[0]["guest"].split(",")
        ipList = []
        for i in range (len(guestList)):
            guest = guestList[i]
            filterstr = "guest= " + "'" + guest + "'"
            Infolist = selecttable("multguest_list", "agreement"
                                   , filterstr, '', '', '')
            ipList.append(Infolist[0][0])

        # 将每个字符串拆分成小元素并创建包含所有元素的列表
        all_elements = [set(s.split(',')) for s in ipList]

        # 找到所有元素的交集
        intersection = set.intersection(*all_elements)

        # 打印结果
        print("每个字符串中的元素:", all_elements)
        print("交集:", intersection)
        resultList = ",".join(intersection)

        print('查找成功')
        if ipList:
            return JsonResponse({'agreement': resultList})
    return JsonResponse({'agreement': '无公共算法协议'})


def createmultmodel(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    model = projs[0]["model"]
    goal = projs[0]["goal"]
    agreement = projs[0]["agreement"]
    status = "未申请"
    pro_js = "'" + guest + "','" + model + "','" + goal + "','" + agreement + "','" + status + "'"
    inserttable(pro_js, tablename="multmodel_list", con1="guest,model,goal,agreement,status")
    print('模型新增成功')
    return JsonResponse({'status': 0})


def createmultmodelapply(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    model = projs[0]["model"]
    datapath = projs[0]["datapath"]
    datastatus = "未提供"
    pro_js = "'" + guest + "','" + model + "','" + datapath + "','" + datastatus + "'"
    inserttable(pro_js, tablename="multmodel_apply", con1="guest,model,datapath,datastatus")
    print('数据申请明细新增成功')
    return JsonResponse({'status': 0})


def multmodel_apply_list(request):
    modelapplylist = selecttable("multmodel_apply", "id,guest,model,datapath,datastatus", '', '', '', '')
    print('数据申请明细查找成功')
    print(modelapplylist)
    return JsonResponse({'status': 0, 'data': modelapplylist, 'msg': 'success'})


def multmodeldel_list(request, parameter):
    context = {'parameter': parameter}
    return render(request,'multmodeldel-list.html', context)

def multmodeldel_add(request):
    return render(request,'multmodeldel-add.html')
def searchmultmodeldel(request):
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    modelid = projs[0]["modelid"]
    modeldellist = selecttable("multmodeldel_list", "id,modelid,guest,dataurl,status", "modelid='"+modelid+"'", '', '', '')
    # modeldellist = selecttable("multmodeldel_list", "id,modelid,guest,dataurl,status", "id='" + modelid + "'", '', '',
    #                            '')
    print('查找成功')
    print(modeldellist)
    return JsonResponse({'status': 0, 'data': modeldellist, 'msg': 'success'})


def getmultmodel_apply(request):
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    modelid = projs[0]["modelid"]
    modeldellist = selecttable("multmodeldel_apply", "id,guest,model,datapath,datastatus", "modelid='" + modelid + "'",
                               '', '', '')
    print('数据申请明细查找成功')
    print(modeldellist)
    return JsonResponse({'status': 0, 'data': modeldellist, 'msg': 'success'})


def runModel(request):
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    modelid = projs[0]["modelid"]
    modeldellist = selecttable("multmodeldel_list", "id,modelid,guest,dataurl,status", "id='" + modelid + "'", '', '',
                               '')
    print('查找成功')
    print(modeldellist)
    return JsonResponse({'status': 0, 'data': modeldellist, 'msg': 'success'})

def createmultmodeldel(request):
    proobj = request.body
    projs = json.loads(proobj)
    guest = projs[0]["guest"]
    modelid = projs[0]["modelid"]
    dataurl = projs[0]["dataurl"]
    status = "未申请"
    pro_js = "'" + guest + "','" + modelid + "','" + dataurl + "','"  + status + "'"
    inserttable(pro_js, tablename="multmodeldel_list", con1="guest,modelid,dataurl,status")
    print('模型明细新增成功')
    return JsonResponse({'status': 0})




def searchmultmodelall(id):
    modelalllist = selecttable("multmodel_list,multmodeldel_list",
                               "multmodeldel_list.id,multmodeldel_list.modelid,multmodeldel_list.guest,multmodeldel_list.dataurl,multmodeldel_list.status,"
                               "multmodel_list.model,multmodel_list.goal", "multmodeldel_list.modelid=multmodel_list.id and multmodeldel_list.id='"+id+"'", '', '', '')
    print('查找成功')
    print(modelalllist)
    # return JsonResponse({'status': 0, 'data': modelalllist, 'msg': 'success'})
    return modelalllist


def updatemultmodeldel1(request):
    data_dict = json.loads(request)
    id = data_dict["id"]
    modelid = data_dict["modelid"]
    guest = data_dict["guest"]
    dataurl = data_dict["dataurl"]
    status = "申请中"
    pro_js = "status=" + "'" + status + "',modelid="+"'"+str(modelid)+"',guest="+"'"+guest+"',dataurl="+"'"+dataurl+"'"
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("multmodeldel_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})
def updatemultmodel1(request):
    data_dict = json.loads(request)
    print(data_dict)
    id = data_dict["id"]
    guest = data_dict["guest"]
    model = data_dict["model"]
    goal = data_dict["goal"]
    status = "申请中"
    pro_js = "status=" + "'" + status + "',model="+"'"+model+"',guest="+"'"+guest+"',goal="+"'"+goal+"'"
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("multmodel_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})

def upload_multmodelapply(request):
    print("------开始传输------")
    proobj = request.body
    projs = json.loads(proobj)
    print(projs)
    id = projs[0]["id"]
    # upload_to_remote_server(request)
    data=searchmultmodelall(id)
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
    data_test={"id": 2, "modelid": 4, "guest": "port", "dataurl": "", "status": "未申请", "model": "pulearning", "goal": "潜在货源挖掘","status_check": "1"}
    updatemultmodeldel1(modeldel_json)
    updatemultmodel1(model_json)
    # upload_modelinfo(data)

    guest = data[0][2]
    filterstr = "guest= " + "'" + guest + "'"
    Infolist = selecttable("multguest_list", "ip"
                           , filterstr, '', '', '')
    print(Infolist)
    ip = Infolist[0][0].split(",")[0]
    url = f'http://{ip}:8000/check_apply_re/'
    print(url)
    # response = requests.post(url, json=data_test)
    editmultmodelall(modeldel_json)
    # print(response)
    return JsonResponse({'status': 0, 'msg': 'success'})

def upload_mult_to_remote_server(request):
    print("开始传输文件")
    # 修改为你的目标虚拟机的IP地址、用户名和密码
    # projs = json.loads(request)
    # print(projs)
    # ip = projs[0]["ip"]
    host = '127.17.109.106'
    port = 22
    username = 'ywj'
    password = 'ywj'

    # 连接到目标虚拟机
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port, username, password)

    # 上传文件到目标虚拟机
    sftp = ssh_client.open_sftp()
    local_path = './myapp/fed_PU_sci1203/share_data/tr.txt'
    remote_path = '/home/ywj/xiangmu/myapp/mount_point/tr.txt' # 修改为目标虚拟机上的目标路径
    sftp.put(local_path, remote_path)
    sftp.close()

    # 关闭SSH连接
    ssh_client.close()
    print("结束传输文件")
    # return JsonResponse({'status': 0, 'msg': 'success'})
def multmodel_test(request):
    data_dict = json.loads(request.body)

    print("数据是", data_dict)
    id = data_dict[0].get("modelid")
    print('开始执行')
    maincf.main(id)
    print('执行成功')
    return JsonResponse({'status': 0, 'msg': 'success'})


def editmultmodelall(request):
    # proobj = request.body
    # print(proobj)
    # # 将字节串解码为字符串
    # proobj_str = request.decode('utf-8')
    # # 将字符串解析为字典
    # data_dict = json.loads(proobj_str)

    data_dict = json.loads(request)

    print("数据是",data_dict)
    id = data_dict.get("id")
    print(id)
    modelid = data_dict["modelid"]
    # guest = data_dict["guest"]
    # dataurl = data_dict["dataurl"]
    # status = data_dict["status"]
    # model = data_dict["model"]
    # goal = data_dict["goal"]
    # status_check = data_dict["status_check"]
    status_check = '1'
    if(status_check=='1'):
        status='同意申请'
    else:
        status = '拒绝申请'
    pro_js = "status="+"'"+status+"'"
    filterstr="id="+"'"+str(id)+"'"
    updatetable("multmodeldel_list",pro_js, filterstr)
    count=count_searchmultmodelall(modelid)
    print('count',count)
    if (count == 0):
        status_Z = '申请成功'
        pro_js = "status=" + "'" + status_Z + "'"
        filterstr = "id=" + "'" + str(modelid) + "'"
        updatetable("multmodel_list", pro_js, filterstr)
    else:
        status = '未申请'
    print('xiugaichenggong')
    return JsonResponse({'status': 0})

def count_searchmultmodelall(id):
    modelalllist = selecttable("multmodel_list,multmodeldel_list",
                               "count(id)",
                               "multmodeldel_list.modelid=multmodel_list.id and and multmodeldel_list.status in ('拒绝申请','申请中') and multmodeldel_list.modelid='"+str(id)+"'",
                               '', '', '')
    print('查找成功')
    print(modelalllist)
    # return JsonResponse({'status': 0, 'data': modelalllist, 'msg': 'success'})
    return modelalllist


def updatemultmodel_level(request,id):
    data_dict = json.loads(request)
    print("data_dict",data_dict)
    preci = data_dict['preci']
    recall1 = data_dict['recall']
    error1 = data_dict['error']
    loss1 = data_dict['loss']
    model_url = data_dict['model_url']
    png_url = data_dict['png_url']
    preci_url = png_url + "precision_recall.png"
    recall1_url = png_url + "precision_recall.png"
    error1_url = png_url + "error_rate.png"
    val_loss_url = png_url + "loss_Test.png"
    pro_js = ("preci=" + "'" + str(preci) + "',recall1="+"'"+str(recall1)
              +"',error1="+"'"+str(error1)+"',val_loss="+"'"+str(loss1)
              +"',preci_url="+"'"+str(preci_url)+ "',recall1_url=" + "'" + str(recall1_url)
              + "',error1_url=" + "'" + str(error1_url) + "',val_loss_url=" + "'" + str(val_loss_url)
              +"',modelurl="+"'"+str(model_url)+"'")
    filterstr = "id=" + "'" + str(id) + "'"
    updatetable("multmodel_list", pro_js, filterstr)
    print('xiugaichenggong')
    return JsonResponse({'status': 0})




def multmodel_applyadd(request):
    return render(request, 'multmodel_applyadd.html')


def open_file_manager(path):
    try:
        # 使用 xdg-open 命令打开文件资源管理器
        absolute_path = path
        print(absolute_path)
        os.startfile(absolute_path)
        subprocess.run(['xdg-open'])
        # subprocess.run(["xdg-open", absolute_path])

        # 返回成功的 JSON 响应
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # 返回错误的 JSON 响应，包含错误信息
        return JsonResponse({'status': 'error', 'message': str(e)})

def predict_with_density_threshold(f_x, prior):
    density_ratio = f_x / prior
    # ascending sort
    sorted_density_ratio = np.sort(density_ratio)
    size = len(density_ratio)

    n_pi = int(size * prior)
    # print("size: ", size)
    # print("density_ratio shape: ", density_ratio.shape)
    # print("n in test data: ", n_pi)
    # print("n in real data: ", (target == 1).sum())
    threshold = (sorted_density_ratio[size - n_pi] + sorted_density_ratio[size - n_pi - 1]) / 2
    # print("threshold:", threshold)
    h = np.sign(density_ratio - threshold).astype(np.int32)
    return h


import logging
import pandas as pd
import numpy as np
import torch
import requests
from django.http import JsonResponse
import os
from datetime import datetime

logger = logging.getLogger(__name__)


def multimodel_predict(request):
    try:
        logger.info("========== 开始执行模型预测 ==========")

        # 1. 配置参数
        MODELS = ["imPUSB"]
        DATA_PATH = os.path.join("myapp", "fed_PU_sci1203", "dataset", "result_in_1123.csv")
        RESULT_ROOT = os.path.join("myapp", "fed_PU_sci1203", "result", "result_in_1123")
        COLUMNS_SET2 = ['JFLC', 'COST', 'TIME', 'DISCOUNT', 'FREIGHT_95306']
        PORT_API_URL = "http://127.0.0.1:8000/model_predict_port/"
        DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 2. 加载数据
        try:
            if not os.path.exists(DATA_PATH):
                raise FileNotFoundError(f"数据文件不存在: {DATA_PATH}")

            df = pd.read_csv(DATA_PATH)
            if df.empty:
                raise ValueError("加载的数据为空")

            features_2 = df[COLUMNS_SET2].values
            labels = df["ISPOTIENTIAL"].values
            logger.info(f"数据加载成功，样本数: {len(labels)}")

        except Exception as e:
            logger.error(f"数据加载失败: {str(e)}", exc_info=True)
            return JsonResponse({'status': 1, 'error': f'数据加载失败: {str(e)}'}, status=500)

        # 3. 数据预处理
        try:
            data2 = torch.tensor(features_2, dtype=torch.float32).to(DEVICE)
            target = torch.tensor(labels, dtype=torch.float32)
            logger.info("数据预处理完成")
        except Exception as e:
            logger.error(f"数据预处理失败: {str(e)}", exc_info=True)
            return JsonResponse({'status': 1, 'error': f'数据预处理失败: {str(e)}'}, status=500)

        # 4. 模型预测
        result_df = df.copy()
        for model in MODELS:
            model_start_time = datetime.now()
            try:
                # 4.1 加载模型
                model_dir = os.path.join(RESULT_ROOT, model)
                if not os.path.exists(model_dir):
                    raise FileNotFoundError(f"模型目录不存在: {model_dir}")

                # 加载客户端模型
                client_model_path = os.path.join(model_dir, "server_model.pth")
                if not os.path.exists(client_model_path):
                    raise FileNotFoundError(f"客户端模型文件不存在: {client_model_path}")

                model_coright = SyNet_client_coright()
                model_coright.load_state_dict(
                    torch.load(client_model_path, map_location=DEVICE)
                )
                model_coright = model_coright.to(DEVICE)

                # 加载顶层模型
                top_model_path = os.path.join(model_dir, "server_top_model.pth")
                if not os.path.exists(top_model_path):
                    raise FileNotFoundError(f"顶层模型文件不存在: {top_model_path}")

                top_model = SyNet_server_co()
                top_model.load_state_dict(
                    torch.load(top_model_path, map_location=DEVICE)
                )
                top_model = top_model.to(DEVICE)
                logger.info(f"模型 {model} 加载成功")

                # 4.2 调用端口API
                try:
                    api_start_time = datetime.now()
                    response = requests.post(
                        PORT_API_URL,
                        json={"model": model},
                        timeout=30  # 30秒超时
                    )
                    api_duration = (datetime.now() - api_start_time).total_seconds()

                    if response.status_code != 200:
                        raise ValueError(
                            f"API返回状态码 {response.status_code}, 响应: {response.text[:200]}"
                        )

                    if not response.text.strip():
                        raise ValueError("API返回空响应")

                    response_data = response.json()
                    output1 = torch.Tensor(response_data['output1']).to(DEVICE)
                    logger.info(f"API调用成功，耗时 {api_duration:.2f}秒")

                except requests.exceptions.RequestException as e:
                    logger.error(f"API请求失败: {str(e)}", exc_info=True)
                    return JsonResponse(
                        {'status': 1, 'error': f'API请求失败: {str(e)}'},
                        status=500
                    )

                # 4.3 模型推理
                with torch.no_grad():
                    model_coright.eval()
                    top_model.eval()

                    output2 = model_coright(data2)
                    output = torch.cat((output1, output2), 1)
                    final_output = top_model(output)

                    # 结果处理
                    h = np.reshape(final_output.detach().cpu().numpy(), len(target))
                    if model == "imbalancednnPUSB":
                        prior = 0.3758
                        h = predict_with_density_threshold(h, prior)
                    else:
                        h = np.where(
                            torch.sigmoid(final_output).detach().cpu().numpy() > 0.5,
                            1, -1
                        ).astype(np.int32)

                # 4.4 保存结果
                result_df[f"{model}_predictions"] = h
                output_dir = os.path.join(model_dir, "predictions")
                os.makedirs(output_dir, exist_ok=True)

                output_path = os.path.join(output_dir, "result_in_1123output.csv")
                result_df.to_csv(output_path, index=False)
                logger.info(f"预测结果已保存到 {output_path}")

                model_duration = (datetime.now() - model_start_time).total_seconds()
                logger.info(f"模型 {model} 处理完成，总耗时 {model_duration:.2f}秒")

            except Exception as e:
                logger.error(f"模型 {model} 处理失败: {str(e)}", exc_info=True)
                return JsonResponse(
                    {'status': 1, 'error': f'模型处理失败: {str(e)}'},
                    status=500
                )

        logger.info("========== 模型预测执行成功 ==========")
        return JsonResponse({
            'status': 0,
            'msg': 'success',
            'output_path': output_path  # 返回结果文件路径
        })

    except Exception as e:
        logger.critical(f"未处理的异常: {str(e)}", exc_info=True)
        return JsonResponse(
            {'status': 1, 'error': f'服务器内部错误: {str(e)}'},
            status=500
        )

# def multimodel_predict(request):
#     print('开始执行')
#     MODELS = ["imPUSB"]
#
#     # 1. 加载数据
#     data_path = "./myapp/fed_PU_sci1203/dataset/result_in_1123.csv"
#     df = pd.read_csv(data_path)
#
#     COLUMNS_SET2 = ['JFLC', 'COST', 'TIME', 'DISCOUNT', 'FREIGHT_95306']  # 第二组要分割的列名 5
#
#     # 2. 按列分开数据
#     # 假设df有两列: "feature" 和 "label"
#     features_2 = df[COLUMNS_SET2].values
#     labels = df["ISPOTIENTIAL"].values
#
#     # 3. 数据预处理
#     # 假设feature和label都是一维数据
#     data2 = torch.tensor(features_2, dtype=torch.float32)
#     target = torch.tensor(labels, dtype=torch.float32)
#
#     DEVICE = torch.device("cpu")
#
#     data2 = data2.to(DEVICE)
#     result_df = None
#     root = "./myapp/fed_PU_sci1203/result/result_in_1123/"
#     for model in MODELS:
#         model_path = root + model + "/server_model.pth"
#         model_coright = SyNet_client_coright()
#         model_coright.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
#
#         model_path = root + model + "/server_top_model.pth"
#         top_model = SyNet_server_co()
#         top_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
#
#         model_coright = model_coright.to(DEVICE)
#         top_model = top_model.to(DEVICE)
#         with torch.no_grad():
#             model_coright.eval()
#             top_model.eval()
#
#             size = len(target)
#             model_dict = {"model": model}
#             print(model_dict)
#             response_from_port = requests.post("http://127.17.109.105:8000/model_predict_port/", json=model_dict)
#             response_data = response_from_port.json()
#             output1 = response_data['output1']
#             print(output1[:10000])
#             output1_tensor = torch.Tensor(output1)
#
#             output2 = model_coright(data2)
#
#             output = torch.cat((output1_tensor, output2), 1)
#
#             final_output = top_model(output)
#
#             h = np.reshape(final_output.detach().cpu().numpy(), size)
#
#             if model == "imbalancednnPUSB":
#                 prior = 0.3758
#                 h = predict_with_density_threshold(h, prior)
#             else:
#                 h = np.reshape(torch.sigmoid(
#                     final_output).detach().cpu().numpy(), size)
#                 h = np.where(h > 0.5, 1, -1).astype(np.int32)
#
#         # 4. Combine into DataFrame
#         h_df = pd.DataFrame(h, columns=[model + "_predictions"])
#         # df = df.reset_index(drop=True)
#         result_df = pd.concat([df, h_df], axis=1)
#         result_df.to_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv',
#                          index=False)  # encoding='utf-8-sig'
#
#     print('执行成功')
#     return JsonResponse({'status': 0, 'msg': 'success'})


def multmodel_predict_port(request):
    print('开始执行port')
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data = json.loads(request.body)
            print("jsondata:",data)
            model_name = data.get('model')

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON model_name"}, status=400)
    MODELS = [model_name]#"imPUSB"


    # 1. 加载数据
    data_path = "./myapp/fed_PU_sci1203/dataset/result_in_1123.csv"
    df = pd.read_csv(data_path)

    COLUMNS_SET1 = ['CARGOWGT', 'ARRIVAL_INTERVAL', 'WAIT_INTERVAL', 'WORK_INTERVAL', 'LEAVE_INTERVAL',
                    'TRANS_INTERVAL', 'STACK_INTERVAL', 'ISHIGH',
                    'ISREFRIGERATED', 'ISCOMPLETED', 'ISTANK', 'TJFLC', 'TTIME', 'TOIL', 'TCOST', 'TPASSBY',
                    'CNTRSIZCOD_20',
                    'CNTRSIZCOD_40', 'IMTRADEMARK_D',
                    'IMTRADEMARK_F']  # 第一组要分割的列名 20

    # 2. 按列分开数据
    # 假设df有两列: "feature" 和 "label"
    features_1 = df[COLUMNS_SET1].values
    # labels = df["ISPOTIENTIAL"].values

    # 3. 数据预处理
    # 假设feature和label都是一维数据
    data1 = torch.tensor(features_1, dtype=torch.float32)
    # target = torch.tensor(labels, dtype=torch.float32)

    DEVICE = torch.device("cpu")

    data1 = data1.to(DEVICE)
    result_df = None
    root = "./myapp/fed_PU_sci1203/result/result_in_1123/"
    for model in MODELS:

        model_path = root + model + "/client_model.pth"
        model_coleft = SyNet_client_coleft()
        model_coleft.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        model_coleft = model_coleft.to(DEVICE)
        with torch.no_grad():
            model_coleft.eval()

            # size = len(target)

            output1 = model_coleft(data1)
            output_list = output1.cpu().numpy().tolist()
            output_list_dict = {'output1': output_list}
    print('执行成功')
    return JsonResponse(output_list_dict)


def application_result_analysis(request):
    # 加载CSV文件
    df = pd.read_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv')

    # 创建数据透视表
    pivot_table = df.pivot_table(index=['FZHZM', 'imbalancednnPUSB_predictions', 'DZHZM'],
                                 aggfunc='size')

    # 重命名索引以更易于理解
    pivot_table.index.names = ['发站站名', '预测结果', '到站站名']

    # 将数据透视表转换为DataFrame并重置索引
    pivot_table_df = pivot_table.reset_index(name='计数')

    # 筛选出imbalancednnPUSB_predictions为1的数据
    filtered_data = df[df["imbalancednnPUSB_predictions"] == 1]

    # 获取不同的FZHZM值
    unique_fzhzm_values = filtered_data["FZHZM"].unique()

    # 设置合适的字体，例如SimHei，用于显示汉字
    font = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', size=12)  # 替换为你的汉字字体文件路径
    pie_charts = []

    # 遍历不同的FZHZM值，为每个值生成饼图
    for fzhzm_value in unique_fzhzm_values:
        # 筛选出特定FZHZM值的数据
        fzhzm_data = filtered_data[filtered_data["FZHZM"] == fzhzm_value]

        # 计算DZHZM的计数
        dzhzm_counts = fzhzm_data["DZHZM"].value_counts()

        # 绘制饼图
        fig, ax = plt.subplots(figsize=(12, 6))
        wedges, texts, autotexts = ax.pie(dzhzm_counts, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # 使饼图为圆形

        # 手动添加标签
        labels = [f"{label}\n({count})" for label, count in zip(dzhzm_counts.index, dzhzm_counts)]
        ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),prop = font)

        plt.title(f"发站为{fzhzm_value}时各到站潜在箱源预测数量", fontproperties=font)

        # 将图像数据转换为base64编码
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        data_uri = base64.b64encode(buf.read()).decode('utf-8')
        pie_charts.append(data_uri)
        plt.close()

    # 将数据透视表DataFrame传递给模板
    return render(request, 'multpivot_table.html',
                  {'pivot_table_df': pivot_table_df,'pie_charts': pie_charts})


# def multmodel_application_result_analysis(request):
#     # 加载CSV文件
#     df = pd.read_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv')
#
#     # 创建数据透视表
#     pivot_table = df.pivot_table(index=['FZHZM', 'imbalancednnPUSB_predictions', 'DZHZM'],
#                                  aggfunc='size')
#
#     # 重命名索引以更易于理解
#     pivot_table.index.names = ['发站站名', '预测结果', '到站站名']
#
#     # 将数据透视表转换为DataFrame并重置索引
#     pivot_table_df = pivot_table.reset_index(name='计数')
#
#     # 筛选出imbalancednnPUSB_predictions为1的数据
#     filtered_data = df[df["imbalancednnPUSB_predictions"] == 1]
#
#     # 获取不同的FZHZM值
#     unique_fzhzm_values = filtered_data["FZHZM"].unique()
#
#     # 设置合适的字体，例如SimHei，用于显示汉字
#     font = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', size=12)  # 替换为你的汉字字体文件路径
#     pie_charts = []
#
#     # 遍历不同的FZHZM值，为每个值生成饼图
#     for fzhzm_value in unique_fzhzm_values:
#         # 筛选出特定FZHZM值的数据
#         fzhzm_data = filtered_data[filtered_data["FZHZM"] == fzhzm_value]
#
#         # 计算DZHZM的计数
#         dzhzm_counts = fzhzm_data["DZHZM"].value_counts()
#
#         # 绘制饼图
#         fig, ax = plt.subplots(figsize=(12, 6))
#         wedges, texts, autotexts = ax.pie(dzhzm_counts, autopct='%1.1f%%', startangle=90)
#         ax.axis('equal')  # 使饼图为圆形
#
#         # 手动添加标签
#         labels = [f"{label}\n({count})" for label, count in zip(dzhzm_counts.index, dzhzm_counts)]
#         ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),prop = font)
#
#         plt.title(f"发站为{fzhzm_value}时各到站潜在箱源预测数量", fontproperties=font)
#
#         # 将图像数据转换为base64编码
#         buf = BytesIO()
#         plt.savefig(buf, format="png")
#         buf.seek(0)
#         data_uri = base64.b64encode(buf.read()).decode('utf-8')
#         pie_charts.append(data_uri)
#         plt.close()
#
#     # 将数据透视表DataFrame传递给模板
#     return render(request, 'multpivot_table.html',
#                   {'pivot_table_df': pivot_table_df,'pie_charts': pie_charts})
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties
import pandas as pd
import base64
from io import BytesIO

# 设置默认字体路径
try:
    # font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"  # macOS
    font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"  # Linux
    font = FontProperties(fname=font_path, size=12)
except:
    font = None  # 如果找不到字体，则不使用自定义字体

def multmodel_application_result_analysis(request):
    df = pd.read_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv')

    pivot_table = df.pivot_table(index=['FZHZM', 'imPUSB_predictions', 'DZHZM'], aggfunc='size')
    pivot_table.index.names = ['发站站名', '预测结果', '到站站名']
    pivot_table_df = pivot_table.reset_index(name='计数')

    filtered_data = df[df["imPUSB_predictions"] == 1]
    unique_fzhzm_values = filtered_data["FZHZM"].unique()

    pie_charts = []
    for fzhzm_value in unique_fzhzm_values:
        fzhzm_data = filtered_data[filtered_data["FZHZM"] == fzhzm_value]
        dzhzm_counts = fzhzm_data["DZHZM"].value_counts()

        fig, ax = plt.subplots(figsize=(12, 6))
        wedges, texts, autotexts = ax.pie(dzhzm_counts, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        labels = [f"{label}\n({count})" for label, count in zip(dzhzm_counts.index, dzhzm_counts)]
        ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop=font)

        plt.title(f"发站为{fzhzm_value}时各到站潜在箱源预测数量", fontproperties=font)

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        data_uri = base64.b64encode(buf.read()).decode('utf-8')
        pie_charts.append(data_uri)
        plt.close()

    return render(request, 'multpivot_table.html', {'pivot_table_df': pivot_table_df, 'pie_charts': pie_charts})

def editMultModelApplicationStatus(request):
    modelsaveid = request.GET.get('mid',None)
    print(modelsaveid)
    pro_js = "datastatus="+"'已提供'"
    print(pro_js)
    filterstr="id="+"'"+str(modelsaveid)+"'"
    print(filterstr)
    result=updatetable("multmodel_apply",pro_js, filterstr)
    if result==1:
        print('申请成功，等待参与者提供数据')
        return JsonResponse({'status': 1})
    if result==0:
        print('申请失败')
        return JsonResponse({'status': 0})


def sample_alignment(request):
    return render(request, 'multsample-alignment.html')


def searchSampleAlignment(request):
    userlist = selecttable("sample_alignment", "ID,SAMPLE_NUM,SAMPLE_NUM_SUCCESS", '', '', '', '')
    print('查找成功')
    print(userlist)
    return JsonResponse({'status': 0, 'data': userlist, 'msg': 'success'})


def train_model(request):
    return render(request, 'multmodel_training.html')