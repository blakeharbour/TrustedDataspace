# serverA.py

import torch
import os
import pickle
from server import Server
from splitNN import SyNet_client, SyNet_server_co
from utils import compute_prior, resample_data, get_train_with_positive_half, EarlyStopping
from evaluator import PUEvaluator
from plot import draw_losses_test_data, draw_precision_recall, draw_error_test_data
from PULoss import PULoss, nnPUSBloss, ImPULoss, ImnnPUSBloss
from data_loader import load_dataset, vertical_split_datasets, vertical_split_testset, load_container_dataset, \
    reconstruct_data, process_data
from client import Client
from torch.utils.data import DataLoader
from torch.nn.utils import parameters_to_vector, vector_to_parameters

if __name__ == '__main__':
    # ... (原始main文件的前半部分代码)
    # 设置设备，尝试使用GPU进行训练
    DEVICE = torch.device("cuda")
    torch.manual_seed(42)

    # 定义损失函数关键字列表
    loss_keys = ["nnPUSB", "nnPU"]
    imbalanced = True

    # 如果数据不平衡，更新损失函数关键字列表
    if imbalanced:
        loss_keys = ["imbalancednnPUSB", "imbalancednnPU"]

    # 初始化两个结果列表，用于存储不同损失函数的结果
    nnPU_result = [[], [], [], [], []]
    nnPUSB_result = [[], [], [], [], []]

    # 存储客户端对象的列表
    Clients = []

    # 数据集名称
    data_name = 'container'

    # 初始化训练、验证和测试集列表
    train_left_sets, val_left_sets, test_left_sets = [], [], []
    train_right_sets, val_right_sets, test_right_sets = [], [], []
    prior = None

    # 根据数据集名称加载相应的数据
    if data_name == 'minst':
        labeled = 1000
        unlabeled = 59000
        NUM_CLIENTS = 1
        trainset, testset, prior = load_dataset(labeled, unlabeled)
        train_left_sets, val_left_sets, train_right_sets, val_right_sets = vertical_split_datasets(NUM_CLIENTS,
                                                                                                   trainset)
        test_left_sets, test_right_sets = vertical_split_testset(NUM_CLIENTS, testset)
        print(data_name + " load completed")
        print("prior: " + str(prior))
    elif data_name == 'container':
        train_left_sets, train_right_sets, val_left_sets, val_right_sets, test_left_sets, test_right_sets = load_container_dataset()
        print(data_name + " load completed")

    # 遍历每个训练集、验证集和测试集
    for train_set, val_set, test_set in zip(train_left_sets, val_left_sets, test_right_sets):
        client = Client(None, train_set, val_set, test_set, DEVICE)
        Clients.append(client)

    # 初始化服务器客户端
    server_client = Server(None, None, train_right_sets, val_right_sets, test_right_sets, DEVICE, None)

    print("Server A is ready")

    # 定义数据类型列表
    data_types = ["train", "val", "test"]

    # 为每个客户端设置数据加载器
    for client in Clients:
        for dtype in data_types:
            ids = client.get_data_ids(is_train=dtype)
            inter_ids = server_client.data_intersection(ids, is_train=dtype)
            client.set_dataloader(inter_ids, is_train=dtype)

    # 初始化损失函数字典
    loss_funcs = {"nnPU": PULoss(prior),
                  "nnPUSB": nnPUSBloss(prior)}

    # 如果先验值小于0.45且是不平衡数据集
    if prior < 0.45 and imbalanced:
        # 重建并重采样数据
        xy_data = reconstruct_data(train_left_sets[0], train_right_sets)
        xy_data_re = resample_data(xy_data)

        # 获取 ISPOTIENTIAL = -1 的数据
        negative_data = xy_data_re[xy_data_re['ISPOTIENTIAL'] == -1]
        # 获取 ISPOTIENTIAL = 1 的所有数据
        positive_data = xy_data_re[xy_data_re['ISPOTIENTIAL'] == 1]
        # 合并这两部分数据
        train_data_re = get_train_with_positive_half(negative_data, positive_data)
        # 处理重采样后的数据
        x_tr = train_data_re[train_data_re.columns.difference(['ISPOTIENTIAL'])]
        y_tr = train_data_re["ISPOTIENTIAL"]
        # 分割左右数据
        left_sets, right_sets = process_data(x_tr, y_tr)
        # 设置服务器的训练集为右侧数据集
        server_client.set_train_set(right_sets)

        print("Server A training completed")

    # 保存模型和结果
    path_to_save = "./result/"
    os.makedirs(path_to_save, exist_ok=True)
    torch.save(server_client.model.state_dict(), path_to_save + "server_model.pth")
    torch.save(server_client.top_model.state_dict(), path_to_save + "server_top_model.pth")

    # 使用 parameters_to_vector 将模型参数转换为向量
    server_model_parameters = parameters_to_vector(server_client.model.parameters())
    server_top_model_parameters = parameters_to_vector(server_client.top_model.parameters())

    # 保存转换后的参数向量
    torch.save(server_model_parameters, path_to_save + "server_model_parameters.pth")
    torch.save(server_top_model_parameters, path_to_save + "server_top_model_parameters.pth")

    with open(path_to_save + 'test_result_server_A.pkl', 'wb') as f:
        pickle.dump({"nnPU": nnPU_result, "nnPUSB": nnPUSB_result}, f)

    # 画图展示结果
    draw_losses_test_data(data_name, nnPU_result[4], nnPUSB_result[4])
    draw_losses_test_data(data_name, nnPU_result[3], nnPUSB_result[3], is_train="Test")
    draw_error_test_data(data_name, nnPU_result[2], nnPUSB_result[2])
    draw_precision_recall(
        data_name, nnPU_result[0], nnPU_result[1], nnPUSB_result[0], nnPUSB_result[1])
