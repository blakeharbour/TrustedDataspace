# -*- coding:utf-8 -*-
import torch

import json
import pandas as pd
from django.http import JsonResponse
from myapp.fed_PU_sci1203.splitNN import SyNet_client_coleft, SyNet_client_coright, SyNet_server_co

def model_predict_port(request):
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