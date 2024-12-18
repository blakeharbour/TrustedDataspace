# -*- coding:utf-8 -*-
import json
import subprocess

from django.http import HttpResponse
import torch

import json

import pandas as pd

from matplotlib.font_manager import FontProperties
from io import BytesIO
import base64
from django.http import JsonResponse
from django.shortcuts import render

from .myjob import *

import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt


from myapp.fed_PU_sci1203.splitNN import SyNet_client_coleft, SyNet_client_coright, SyNet_server_co


def model_application(request):
    return render(request, 'modelapphtmls/model_application.html')

def searchModelApplication(request):
    modellist = selecttable("model_save",
                            "ID,GUEST,MODELNAME,MODELDESC,DATASTATUS,TRAINFRE,"
                            "STORAGPATH,MODEL_LOSS,MODEL_ACCURACY,MODEL_PRECISION,MODEL_RECALL,MODELID",
                            '', '', '', '')
    print('查找成功')
    print(modellist)
    return JsonResponse({'status': 0, 'data': modellist, 'msg': 'success'})

def editModelApplicationStatus(request):
    modelsaveid = request.GET.get('mid',None)
    guest = request.GET.get('guest',None)
    print(modelsaveid)
    pro_js = "datastatus="+"'等待中'"
    print(pro_js)
    filterstr="id="+"'"+str(modelsaveid)+"'"
    print(filterstr)
    result=updatetable("model_save",pro_js, filterstr)
    model_dict = {"model": modelsaveid}
    print('model_dictL:', model_dict)
    guest_ip = getip(guest)
    print(guest_ip)
    url = "http://" + guest_ip + ":8000/application_status_modify-port/"
    print(url)
    response_from_port = requests.post(url, json=model_dict)
    response_data = response_from_port.json()
    result1 = response_data['status']
    if result==1:
        print('申请成功，等待参与者提供数据')
        if result1 == 1:
            print('参与方已接收请求，待审核提供')
            return JsonResponse({'status': 2})
        if result1 == 0:
            print('参与方接收请求失败')
            return JsonResponse({'status': 3})
        # return JsonResponse({'status': 1})
    if result==0:
        print('申请失败')
        return JsonResponse({'status': 0})



def editModelOfferStatus(request):
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data = json.loads(request.body)
            print("jsondata:",data)
            modelsaveid = data.get('model')

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON model_name"}, status=400)
    # modelsaveid = request.GET.get('mid',None)
    print(modelsaveid)
    pro_js = "datastatus="+"'已提供'"
    print(pro_js)
    filterstr="id="+"'"+str(modelsaveid)+"'"
    print(filterstr)
    result=updatetable("model_save",pro_js, filterstr)
    if result==1:
        print('参与者已提供数据梯度')
        return JsonResponse({'status': 1})
    if result==0:
        print('参与者提供数据失败')
        return JsonResponse({'status': 0})

def model_main(request):
    return render(request,'modelapphtmls/model-main.html')
def searchmodel(request):
    modellist = selecttable("model_list", "id,guest,model,goal,applicationsta", '', '', '', '')
    print('查找成功')
    print(modellist)
    return JsonResponse({'status': 0, 'data': modellist, 'msg': 'success'})

def application_result(request):
    return render(request,'modelapphtmls/application_result.html')
def searchapplication_result(request):
    modellist = selecttable("application_result", "id,modelname,modelid,modeldes,resultoutpath,resultpltpath,predictlabel", '', '', '', '')
    print('查找成功')
    print(modellist)
    return JsonResponse({'status': 0, 'data': modellist, 'msg': 'success'})

def application_result_shappng(request,i):
    shappng_dic = request.GET.get('pngpath', None)
    print(shappng_dic)
    with open(shappng_dic,'rb') as f:
        return HttpResponse(f.read(),content_type="image/png")

def application_result_analysis(request):
    # 加载CSV文件
    df = pd.read_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv')

    # 创建数据透视表
    pivot_table = df.pivot_table(index=['FZHZM', 'imPUSB_predictions', 'DZHZM'],
                                 aggfunc='size')

    # 重命名索引以更易于理解
    pivot_table.index.names = ['发站站名', '预测结果', '到站站名']

    # 将数据透视表转换为DataFrame并重置索引
    pivot_table_df = pivot_table.reset_index(name='计数')

    # 筛选出imbalancednnPUSB_predictions为1的数据
    filtered_data = df[df["imPUSB_predictions"] == 1]

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

    zzt_TCOST = draw_sta_png('TCOST')
    # print('zzt_TCOST',zzt_TCOST)
    zzt_TCOST_total = draw_sta_png_total('TCOST')
    zzt_TJFLC = draw_sta_png('TJFLC')
    # print('zzt_TCOST',zzt_TCOST)
    zzt_TJFLC_total = draw_sta_png_total('TJFLC')

    # 将数据透视表DataFrame传递给模板
    return render(request, 'modelapphtmls/pivot_table.html',
                  {'pivot_table_df': pivot_table_df, 'pie_charts': pie_charts,
                   'zzt_TCOST': zzt_TCOST, 'zzt_TCOST_total': zzt_TCOST_total,
                   'zzt_TJFLC': zzt_TJFLC, 'zzt_TJFLC_total': zzt_TJFLC_total})

def draw_sta_png(label):
    zzt = []
    # 加载CSV文件
    df = pd.read_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv')
    # 设置合适的字体，例如SimHei，用于显示汉字
    font = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', size=12)  # 替换为你的汉字字体文件路径

    # 根据条件筛选记录
    filtered_df = df[(df['imPUSB_predictions'] == 1)]

    sns.histplot(filtered_df[label])
    plt.ylabel("潜在箱源箱数", fontproperties=font)  # 修改纵轴标签
    plt.xlabel(label, fontproperties=font)  # 修改纵轴标签

    # matplotlib.rcParams['font.family'] = 'SimHei'  # 例如，使用中文字体：SimHei
    # 将图像数据转换为base64编码
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    data_uri = base64.b64encode(buf.read()).decode('utf-8')
    zzt.append(data_uri)
    plt.close()
    return zzt

def draw_sta_png_total(label):
    zzt_total = []
    # 加载CSV文件
    df = pd.read_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv')
    # 设置合适的字体，例如SimHei，用于显示汉字
    font = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', size=12)  # 替换为你的汉字字体文件路径
    # 根据条件筛选记录
    filtered_df = df[(df['imPUSB_predictions'] == 1)]
    filtered_df1 = df[(df['ISPOTIENTIAL'] == 1)]

    # 生成一些示例数据
    data1 = df[label]  # 第一个直方图的数据
    data2 = filtered_df[label]  # 第二个直方图的数据
    data3 = filtered_df1[label]  # 第二个直方图的数据
    # 画直方图
    plt.hist(data1, bins=30, alpha=0.5, label='整体样本')  # alpha参数控制透明度
    plt.hist(data2, bins=30, alpha=0.5, label='潜在箱源')
    plt.hist(data3, bins=30, alpha=0.5, label='原铁路箱源')

    # 添加标签和标题
    plt.ylabel("箱数", fontproperties=font)  # 修改纵轴标签
    plt.xlabel(label, fontproperties=font)  # 修改纵轴标签
    # plt.title('两个直方图')

    # 添加图例
    plt.legend(prop = font)
    # 将图像数据转换为base64编码
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    data_uri = base64.b64encode(buf.read()).decode('utf-8')
    zzt_total.append(data_uri)
    plt.close()
    return zzt_total

def open_file_manager(request):
    try:
        # 使用 xdg-open 命令打开文件资源管理器
        absolute_path='/home/ysshfj/sfjg/myapp/application_result/csv/'
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
def model_predict(request):
    print('开始执行')
    MODELS = ["imPUSB"]


    # 1. 加载数据
    data_path = "./myapp/fed_PU_sci1203/dataset/result_in_1123.csv"
    df = pd.read_csv(data_path)

    COLUMNS_SET2 = ['JFLC', 'COST', 'TIME', 'DISCOUNT', 'FREIGHT_95306']  # 第二组要分割的列名 5

    # 2. 按列分开数据
    # 假设df有两列: "feature" 和 "label"
    features_2 = df[COLUMNS_SET2].values
    labels = df["ISPOTIENTIAL"].values

    # 3. 数据预处理
    # 假设feature和label都是一维数据
    data2 = torch.tensor(features_2, dtype=torch.float32)
    target = torch.tensor(labels, dtype=torch.float32)

    DEVICE = torch.device("cpu")

    data2 = data2.to(DEVICE)
    result_df = None
    root = "./myapp/fed_PU_sci1203/result/result_in_1123/"
    for model in MODELS:
        model_path = root + model + "/server_model.pth"
        print("model_path",model_path)
        model_coright = SyNet_client_coright()
        model_coright.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        model_path = root + model + "/server_top_model.pth"
        top_model = SyNet_server_co()
        top_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        model_coright = model_coright.to(DEVICE)
        top_model = top_model.to(DEVICE)
        with torch.no_grad():
            model_coright.eval()
            top_model.eval()

            size = len(target)
            model_dict = {"model": model}
            guest_ip = getip("port")
            print(guest_ip)
            url = "http://" + guest_ip + ":8000/model_predict_port/"
            print(url)
            response_from_port = requests.post(url, json=model_dict)
            response_data = response_from_port.json()
            output1 = response_data['output1']
            print(output1[:10000])
            output1_tensor = torch.Tensor(output1)

            output2 = model_coright(data2)

            output = torch.cat((output1_tensor, output2), 1)

            final_output = top_model(output)

            h = np.reshape(final_output.detach().cpu().numpy(), size)

            if model == "imbalancednnPUSB":
                prior = 0.3758
                h = predict_with_density_threshold(h, prior)
            else:
                h = np.reshape(torch.sigmoid(
                    final_output).detach().cpu().numpy(), size)
                h = np.where(h > 0.5, 1, -1).astype(np.int32)

        # 4. Combine into DataFrame
        h_df = pd.DataFrame(h, columns=[model + "_predictions"])
        # df = df.reset_index(drop=True)
        result_df = pd.concat([df, h_df], axis=1)
        result_df.to_csv('./myapp/fed_PU_sci1203/result/result_in_1123/imPUSB/result_in_1123output.csv', index=False)  # encoding='utf-8-sig'

    print('执行成功')
    return JsonResponse({'status': 0, 'msg': 'success'})

def getip (guest):
    guestlist = selecttable("guest_list", "id,guest,ip,remark,testtime,statu", "guest=" + "'" + guest + "'", '', '', '')
    print(guestlist)
    ip_address = guestlist[0][2]
    return ip_address