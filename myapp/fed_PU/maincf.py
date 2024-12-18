import torch
from myapp.fed_PU_sci1203 import *
from .PULoss import PULoss, nnPUSBloss, ImPULoss, ImnnPUSBloss
from .client import Client
from .data_loader_port import load_dataset, vertical_split_datasets, vertical_split_testset, load_container_dataset, \
    reconstruct_data, process_data
from .evaluator import PUEvaluator
from .plot import draw_losses_test_data, draw_precision_recall, draw_error_test_data
from .server import Server
from .splitNN import SyNet_client, SyNet_server, SyNet_client_coleft, SyNet_client_coright, SyNet_server_co
from .utils import compute_prior, resample_data, get_train_with_positive_half, EarlyStopping
from ..views import updatemodel_level
import pickle
import os
import json


def main():
    # DEVICE = torch.device("cuda")  # Try "cuda" to train on GPU
    # torch.manual_seed(42)
    DEVICE = torch.device("cpu")  # 使用 "cpu" 以确保在 CPU 上运行
    torch.manual_seed(42)
    loss_keys = ["nnPU"]  # "nnPUSB","nnPU"
    imbalanced = False
    nnPU_result = [[], [], [], [], []]
    nnPUSB_result = [[], [], [], [], []]

    Clients = []

    data_name = 'container'
    train_left_sets, val_left_sets, test_left_sets = [], [], []
    train_right_sets, val_right_sets, test_right_sets = [], [], []
    prior = None
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
        print("类型",type(train_left_sets))
        print(train_left_sets)
        train_left_sets.to_csv('.\\dataset\\train.csv', index=False)
        print(data_name + " load completed")

    for train_set, val_set, test_set in zip(train_left_sets, val_left_sets, test_left_sets):
        client = Client(None, train_set, val_set, test_set, DEVICE)
        Clients.append(client)

    server_client = Server(None, None, train_right_sets, val_right_sets, test_right_sets, DEVICE, None)

    print("Clients and server are ready")

    data_types = ["train", "val", "test"]

    for client in Clients:
        for dtype in data_types:
            ids = client.get_data_ids(is_train=dtype)
            inter_ids = server_client.data_intersection(ids, is_train=dtype)
            client.set_dataloader(inter_ids, is_train=dtype)

    loss_funcs = {}
    if data_name == 'minst':
        loss_funcs = {"nnPU": PULoss(prior),
                      "nnPUSB": nnPUSBloss(prior)}

    elif data_name == 'container':
        # prior = compute_prior(server_client, Clients)
        # prior = 0.3776 container_1017
        # container_1018 prior = 0.3602
        # container_stack_1500 prior = 0.366

        # prior = 0.4094 #container_JFLC_1500
        # container_E_1112 prior = 0.3253
        prior = 0.3747
        print("final prior:" + str(prior))

        loss_funcs = {"nnPU": PULoss(prior),
                      "nnPUSB": nnPUSBloss(prior)}

        if prior < 0.4 and imbalanced:
            xy_data = reconstruct_data(train_left_sets[0], train_right_sets)
            xy_data_re = resample_data(xy_data)

            # 获取 ISPOTIENTIAL = -1 的数据，并只保留前1万条
            negative_data = xy_data_re[xy_data_re['ISPOTIENTIAL'] == -1]
            # 获取 ISPOTIENTIAL = 1 的所有数据
            positive_data = xy_data_re[xy_data_re['ISPOTIENTIAL'] == 1]
            # 合并这两部分数据
            train_data_re = get_train_with_positive_half(negative_data, positive_data)

            x_tr = train_data_re[train_data_re.columns.difference(['ISPOTIENTIAL'])]
            y_tr = train_data_re["ISPOTIENTIAL"]

            left_sets, right_sets = process_data(x_tr, y_tr)

            server_client.set_train_set(right_sets)

            client = Clients[0]
            client.set_train_set(left_sets)
            ids = client.get_data_ids(is_train="train")
            inter_ids = server_client.data_intersection(ids, is_train="train")
            client.set_dataloader(inter_ids, is_train="train")

            # prior_ = compute_prior(server_client, Clients)
            # prior_ = 0.4458 container_1017
            # container_1018 prior_ = 0.4494
            # container_stack_1500  prior_ = 0.5127
            # container_E_1112 prior_ =  0.5409
            prior_ = 0.4437

            print("resample prior:" + str(prior_))
            loss_funcs["imbalancednnPU"] = ImPULoss(prior, prior_)
            loss_funcs["imbalancednnPUSB"] = ImnnPUSBloss(prior, prior_)
            loss_keys = ["imbalancednnPU"]  # "imbalancednnPUSB","imbalancednnPU"

    # Extract labels from right_set
    labels_from_right_set = [item[1] for item in test_right_sets]
    count_ones = labels_from_right_set.count(1)
    # prior_test = round(count_ones / len(test_right_sets), 4)
    # prior_test = compute_prior(server_client, Clients, is_train=False)
    prior_test = 0.4045
    print("test prior:" + str(prior_test))
    for loss_key in loss_keys:

        for client in Clients:
            model = None
            if data_name == 'minst':
                model = SyNet_client()
                client.set_model(model, 0.001, 0.001)
            elif data_name == 'container':
                model = SyNet_client_coleft()
                client.set_model(model, 0.001, 0.001)

        model = None
        top_model = None

        if data_name == 'minst':
            model = SyNet_client()
            top_model = SyNet_server()
            server_client.set_model(model, top_model, 0.001, 0.001)
        elif data_name == 'container':
            model = SyNet_client_coright()
            top_model = SyNet_server_co()
            server_client.set_model(model, top_model, 0.01, 0.01)

        server_client.set_criterion(loss_funcs[loss_key])

        for epoch in range(100):
            train_loss_ = []
            result = []
            client = Clients[0]
            for data1, (data2, target, _) in zip(client.train_loader, server_client.train_loader):
                client.optimizer.zero_grad()
                server_client.optimizer.zero_grad()
                server_client.top_optimizer.zero_grad()

                data1 = data1.reshape(data1.shape[0], -1).to(DEVICE).float()

                output1 = client.model(data1)

                data2 = data2.reshape(data2.shape[0], -1).to(DEVICE).float()
                target = target.to(DEVICE)

                output2 = server_client.model(data2)

                output = torch.cat((output1, output2), 1)

                final_output = server_client.top_model(output)

                target = target.view(-1, 1).float()

                loss = server_client.criterion(final_output, target)
                train_loss_.append(loss.item())
                # 现在是更新了整个梯度，然后用这一个梯度去更新三个模型
                # 但是我们想要的是分别更新梯度，分别更新三个模型
                output.retain_grad()
                loss.backward(retain_graph=True)
                print("开始测试乱七八糟")

                grad = output.grad
                output1_grad = grad[:, :output1.size(1)]

                client.optimizer.zero_grad()
                output1.backward(output1_grad)

                # 使用优化器进行参数更新
                client.optimizer.step()

                # 打印服务器客户端模型的结构
                # print("Server-Client Model Structure:")
                # for name, param in server_client.model.named_parameters():
                #     print(f'{name}: {param.size()}')

                # # 获取模型参数===============================
                # model_parameters = [param for param in client.model.parameters()]
                # # 获取计算得到的梯度
                # client_gradients = [param.grad for param in model_parameters]
                # client.update_parameters(output1_grad, client.optimizer)
                # # After loss.backward()
                #
                # server_client_gradients = [param.grad for param in server_client.model.parameters()]
                # # 打印梯度的大小
                # # print("\nGradients:")
                # # for gradient in server_client_gradients:
                # #     print(f'Gradient size: {gradient.size()}')
                # server_client.update_parameters(server_client_gradients, server_client.optimizer)
                #
                # # After another loss.backward() (if needed)
                # top_gradients = [param.grad for param in server_client.top_model.parameters()]
                # server_client.top_model.update_parameters(top_gradients, server_client.top_optimizer)
                # =====================================================================================
                # 打印客户端模型的参数梯度
                # print("Client Model Gradients:")
                # for name, param in client.model.named_parameters():
                #     if param.grad is not None:
                #         print(f"{name}: {param.grad}")
                #     else:
                #         print(f"{name}: No gradient")

                # client.optimizer.step()
                # server_client.optimizer.step()
                # server_client.top_optimizer.step()

                print(f"Epoch: {epoch + 1}")
                print(f"Client Loss: {loss.item()}")
                # 保存客户端和服务端模型***********************************888
                # path_to_save_client_model = "./result/" + loss_key + "/client_model.pth"
                # path_to_save_server_model = "./result/" + loss_key + "/server_model.pth"
                # path_to_save_server_top_model = "./result/" + loss_key + "/server_top_model.pth"
                #
                # os.makedirs(os.path.dirname(path_to_save_client_model), exist_ok=True)
                # os.makedirs(os.path.dirname(path_to_save_server_model), exist_ok=True)
                # os.makedirs(os.path.dirname(path_to_save_server_top_model), exist_ok=True)
                #
                # torch.save(client.model.state_dict(), path_to_save_client_model)
                # torch.save(server_client.model.state_dict(), path_to_save_server_model)
                # torch.save(server_client.top_model.state_dict(), path_to_save_server_top_model)
                #
                # print(f"客户端模型已保存至: {path_to_save_client_model}")
                # print(f"服务端模型已保存至: {path_to_save_server_model}")
                # print(f"服务端顶层模型已保存至: {path_to_save_server_top_model}")
                #     *****************************************************************************8
                # -------------------------------------------------------------------------
                # for epoch in range(10):
                #     train_loss_ = []
                #     result = []
                #     client = Clients[0]
                #     for data1, (data2, target, _) in zip(client.train_loader, server_client.train_loader):
                #         client.optimizer.zero_grad()
                #         server_client.optimizer.zero_grad()
                #         server_client.top_optimizer.zero_grad()
                #
                #         data1 = data1.reshape(data1.shape[0], -1).to(DEVICE).float()
                #
                #         output1 = client.model(data1)
                #
                #         data2 = data2.reshape(data2.shape[0], -1).to(DEVICE).float()
                #         target = target.to(DEVICE)
                #
                #         output2 = server_client.model(data2)
                #
                #         output = torch.cat((output1, output2), 1)
                #
                #         final_output = server_client.top_model(output)
                #
                #         target = target.view(-1, 1).float()
                #
                #         # 计算client模型的损失
                #         client_loss = server_client.criterion(final_output, target)
                #
                #         # 计算server_client模型的损失
                #         server_client_loss = server_client.criterion(final_output, target)
                #
                #         # 计算top_model模型的损失
                #         top_model_loss = server_client.criterion(final_output, target)
                #
                #         # 进行各自的反向传播
                #         client_loss.backward(retain_graph=True)
                #         server_client_loss.backward(retain_graph=True)
                #         top_model_loss.backward(retain_graph=True)
                #
                #         # 各自更新梯度
                #         client.optimizer.step()
                server_client.optimizer.step()
                server_client.top_optimizer.step()
            #
            #         # 记录train_loss
            #         train_loss_.append(server_client_loss.item())
            #
            #         print(f"Epoch: {epoch + 1}")
            #         print(f"Client Loss: {client_loss.item()}")
            #         print(f"Server Client Loss: {server_client_loss.item()}")
            #         print(f"Top Model Loss: {top_model_loss.item()}")
            #         print(f"Average Train Loss: {sum(train_loss_) / len(train_loss_)}")
            # 在这里你可以记录每个epoch的平均train_loss等等
            # -------------------------------------------------------------------
            # evaluator_train = MultiPUEvaluator(prior, client.model, server_client.model, server_client.top_model,
            #                                    client.train_loader, server_client.train_loader, DEVICE)
            # computed_summary_train = evaluator_train.evaluate()
            #
            # evaluator_val = MultiPUEvaluator(prior, client.model, server_client.model, server_client.top_model,
            #                                  client.val_loader, server_client.val_loader, DEVICE)
            # computed_summary_val = evaluator_val.evaluate()
            #
            # print(f"Epoch: {epoch + 1}")
            # print(computed_summary_train)
            # print(computed_summary_val)
            train_loss = sum(train_loss_) / len(train_loss_)

            evaluator_test = PUEvaluator(prior_test, client.model, server_client.model, server_client.top_model,
                                         client.test_loader, server_client.test_loader, server_client.criterion, DEVICE)

            if "nnPUSB" in loss_key:
                result.extend(evaluator_test.evaluate())
                nnPUSB_result[0].append(result[0])
                nnPUSB_result[1].append(result[1])
                nnPUSB_result[2].append(result[2])
                nnPUSB_result[3].append(result[3])
                nnPUSB_result[4].append(train_loss)

            else:
                result.extend(evaluator_test.error(is_logistic=True))
                nnPU_result[0].append(result[0])
                nnPU_result[1].append(result[1])
                nnPU_result[2].append(result[2])
                nnPU_result[3].append(result[3])
                nnPU_result[4].append(train_loss)

            print(f"Epoch: {epoch + 1} " + loss_key)
            print(
                "{0}\tprecision: {1:-8}\t recall: {2:-8}\t error: {3:-8}\t train_loss: {4:-8} \t val_loss: {5:-8}".format(
                    epoch + 1, round(result[0], 4), round(result[1], 4), round(result[2], 4), round(train_loss, 4),
                    round(result[3], 4)))

            if (epoch + 1) == 100:
                level_dict = {
                    "preci": round(result[0], 4),
                    "recall": round(result[1], 4),
                    "error": round(result[2], 4),
                    "loss": round(result[3], 4),
                    "model_url": "./myapp/fed_PU_sci1203/result/nnPU/"
                }
                level_json = json.dumps(level_dict, ensure_ascii=False)
                updatemodel_level(level_json)
                path_to_save = "./result/" + loss_key + "/"
                os.makedirs(os.path.dirname(path_to_save), exist_ok=True)

                torch.save(client.model.state_dict(), path_to_save + "client_model.pth")
                torch.save(server_client.model.state_dict(), path_to_save + "server_model.pth")
                torch.save(server_client.top_model.state_dict(), path_to_save + "server_top_model.pth")

                with open(path_to_save + 'test_result.pkl', 'wb') as f:
                    if "nnPUSB" in loss_key:
                        pickle.dump(nnPUSB_result, f)
                    else:
                        pickle.dump(nnPU_result, f)

    draw_losses_test_data(data_name, nnPU_result[4], nnPUSB_result[4])
    print("loss", nnPU_result[4])
    print(len(nnPU_result[4]))
    draw_losses_test_data(data_name, nnPU_result[3], nnPUSB_result[3], is_train="Test")
    print(nnPU_result[3])
    draw_error_test_data(data_name, nnPU_result[2], nnPUSB_result[2])
    draw_precision_recall(
        data_name, nnPU_result[0], nnPU_result[1], nnPUSB_result[0], nnPUSB_result[1])

# 训练结束后保存全局模型
# path_to_save_global_model = "./result/global_model.pth"
# torch.save(server_client.top_model.state_dict(), path_to_save_global_model)
# print(f"Global model saved to: {path_to_save_global_model}")
