import numpy as np
import pandas as pd
import torch

from splitNN import SyNet_client_coleft, SyNet_client_coright, SyNet_server_co

MODELS = ["imbalancednnPUSB"]


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


# 1. 加载数据
data_path = "./dataset/container_JFLC_1500.csv"
df = pd.read_csv(data_path)

COLUMNS_SET1 = ['ARRIVAL_INTERVAL', 'WAIT_INTERVAL', 'WORK_INTERVAL', 'LEAVE_INTERVAL',
                'STACK_INTERVAL',  'TPASSBY',]  # 第一组要分割的列名
COLUMNS_SET2 = ['JFLC', 'COST', 'TIME', 'DISCOUNT', 'FREIGHT_95306', 'FREIGHT_REAL']



# 2. 按列分开数据
# 假设df有两列: "feature" 和 "label"
features_1 = df[COLUMNS_SET1].values
features_2 = df[COLUMNS_SET2].values
labels = df["ISPOTIENTIAL"].values

# 3. 数据预处理
# 假设feature和label都是一维数据
data1 = torch.tensor(features_1, dtype=torch.float32)
data2 = torch.tensor(features_2, dtype=torch.float32)
target = torch.tensor(labels, dtype=torch.float32)

DEVICE = torch.device("cuda")

data1 = data1.to(DEVICE)
data2 = data2.to(DEVICE)
result_df = None
root = "./result/"
for model in MODELS:

    model_path = root + model + "/client_model.pth"
    model_coleft = SyNet_client_coleft()
    model_coleft.load_state_dict(torch.load(model_path))

    model_path = root + model + "/server_model.pth"
    model_coright = SyNet_client_coright()
    model_coright.load_state_dict(torch.load(model_path))

    model_path = root + model + "/server_top_model.pth"
    top_model = SyNet_server_co()
    top_model.load_state_dict(torch.load(model_path))

    model_coleft = model_coleft.to(DEVICE)
    model_coright = model_coright.to(DEVICE)
    top_model = top_model.to(DEVICE)
    with torch.no_grad():
        model_coleft.eval()
        model_coright.eval()
        top_model.eval()

        size = len(target)

        output1 = model_coleft(data1)

        output2 = model_coright(data2)

        output = torch.cat((output1, output2), 1)

        final_output = top_model(output)

        h = np.reshape(final_output.detach().cpu().numpy(), size)

        if model == "imbalancednnPUSB":
            prior = 0.5
            h = predict_with_density_threshold(h, prior)
        else:
            h = np.reshape(torch.sigmoid(
                final_output).detach().cpu().numpy(), size)
            h = np.where(h > 0.5, 1, -1).astype(np.int32)

    # 4. Combine into DataFrame
    h_df = pd.DataFrame(h, columns=[model + "_predictions"])
    df = df.reset_index(drop=True)
    result_df = pd.concat([df, h_df], axis=1)
    result_df.to_csv('predict_result_JFLC.csv', index=False, encoding='utf-8-sig')

