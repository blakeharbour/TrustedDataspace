import numpy as np
import pandas as pd
import torch
from sklearn.datasets import fetch_openml
from torch.utils.data import Dataset
from torch.utils.data import random_split

from .utils import get_train_with_positive

COLUMNS_SET1 = ['CARGOWGT', 'ARRIVAL_INTERVAL', 'WAIT_INTERVAL', 'WORK_INTERVAL', 'LEAVE_INTERVAL',
                'TRANS_INTERVAL', 'STACK_INTERVAL', 'ISHIGH',
                'ISREFRIGERATED', 'ISCOMPLETED', 'ISTANK', 'TJFLC', 'TTIME', 'TOIL', 'TCOST', 'TPASSBY',
                'CNTRSIZCOD_20',
                'CNTRSIZCOD_40', 'IMTRADEMARK_D',
                'IMTRADEMARK_F']  # 第一组要分割的列名
# COLUMNS_SET2 = ['JFLC', 'COST', 'TIME', 'DISCOUNT', 'FREIGHT_95306',
#                 'distance_difference', 'cost_difference', 'time_difference',
#        'distance_relative', 'cost_relative', 'time_relative']  # 第二组要分割的列名
COLUMNS_SET2 = ['JFLC', 'COST', 'TIME', 'DISCOUNT', 'FREIGHT_95306']  # 第二组要分割的列名



def get_mnist():
    mnist = fetch_openml('mnist_784', data_home="./dataset")

    x = mnist.data
    y = mnist.target
    # reshape to (#data, #channel, width, height)
    x = np.reshape(x, (x.shape[0], 1, 12, 12)) / 255.
    x_tr = np.asarray(x[:60000], dtype=np.float32)
    y_tr = np.asarray(y[:60000], dtype=np.int32)
    x_te = np.asarray(x[60000:], dtype=np.float32)
    y_te = np.asarray(y[60000:], dtype=np.int32)
    return (x_tr, y_tr), (x_te, y_te)


def get_container():
    container = pd.read_csv("/home/bjdtd/TrustedDataspace/myapp/fed_PU_sci1203/dataset/result_out_1123.csv", encoding="utf8")
    container['DATADATE'] = pd.to_datetime(container['DATADATE'])
    train_mask = (container['DATADATE'] < '2023-05-01')
    test_mask = (container['DATADATE'] >= '2023-05-01')

    med_data = container[train_mask]

    # 获取 ISPOTIENTIAL = -1 的数据，并只保留前1万条
    negative_data = med_data[med_data['ISPOTIENTIAL'] == -1]
    # 获取 ISPOTIENTIAL = 1 的所有数据
    positive_data = med_data[med_data['ISPOTIENTIAL'] == 1]
    # 合并这两部分数据
    train_data = get_train_with_positive(negative_data, positive_data)

    x_tr = train_data[train_data.columns.difference(['ISPOTIENTIAL', 'DATADATE'])]
    y_tr = train_data["ISPOTIENTIAL"]

    med_data_test = container[test_mask]

    # 获取 ISPOTIENTIAL = -1 的数据，并只保留前1万条
    negative_data = med_data_test[med_data_test['ISPOTIENTIAL'] == -1]
    # 获取 ISPOTIENTIAL = 1 的所有数据
    positive_data = med_data_test[med_data_test['ISPOTIENTIAL'] == 1]
    # 合并这两部分数据

    test_data = pd.concat([negative_data, positive_data]).sample(
        frac=1).reset_index(drop=True)

    x_te = test_data[test_data.columns.difference(['ISPOTIENTIAL', 'DATADATE'])]
    y_te = test_data["ISPOTIENTIAL"]

    return (x_tr, y_tr), (x_te, y_te)


def binarize_mnist_class(y_train, y_test):
    y_train_bin = np.ones(len(y_train), dtype=np.int32)
    y_train_bin[y_train % 2 == 1] = -1
    y_test_bin = np.ones(len(y_test), dtype=np.int32)
    y_test_bin[y_test % 2 == 1] = -1
    return y_train_bin, y_test_bin


def make_dataset(dataset, n_labeled, n_unlabeled):
    def make_pu_dataset_from_binary_dataset(x, y, labeled=n_labeled, unlabeled=n_unlabeled):
        labels = np.unique(y)
        positive, negative = labels[1], labels[0]
        x, y = np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.int32)
        assert (len(x) == len(y))
        perm = np.random.permutation(len(y))
        x, y = x[perm], y[perm]
        n_p = (y == positive).sum()
        n_lp = labeled
        n_n = (y == negative).sum()
        n_u = unlabeled
        if labeled + unlabeled == len(x):
            n_up = n_p - n_lp
        elif unlabeled == len(x):
            n_up = n_p
        else:
            raise ValueError("Only support |P|+|U|=|X| or |U|=|X|.")
        _prior = float(n_up) / float(n_u)
        xlp = x[y == positive][:n_lp]
        xup = np.concatenate((x[y == positive][n_lp:], xlp), axis=0)[:n_up]
        xun = x[y == negative]
        x = np.asarray(np.concatenate((xlp, xup, xun), axis=0), dtype=np.float32)
        print(x.shape)
        y = np.asarray(np.concatenate((np.ones(n_lp), -np.ones(n_u))), dtype=np.int32)
        perm = np.random.permutation(len(y))
        x, y = x[perm], y[perm]
        return x, y, _prior

    def make_pn_dataset_from_binary_dataset(x, y):
        labels = np.unique(y)
        positive, negative = labels[1], labels[0]
        X, Y = np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.int32)
        n_p = (Y == positive).sum()
        n_n = (Y == negative).sum()
        Xp = X[Y == positive][:n_p]
        Xn = X[Y == negative][:n_n]
        X = np.asarray(np.concatenate((Xp, Xn)), dtype=np.float32)
        Y = np.asarray(np.concatenate((np.ones(n_p), -np.ones(n_n))), dtype=np.int32)
        perm = np.random.permutation(len(Y))
        X, Y = X[perm], Y[perm]
        return X, Y

    (x_train, y_train), (x_test, y_test) = dataset
    x_train, y_train, prior = make_pu_dataset_from_binary_dataset(x_train, y_train)
    x_test, y_test = make_pn_dataset_from_binary_dataset(x_test, y_test)
    print("training:{}".format(x_train.shape))
    print("test:{}".format(x_test.shape))
    return list(zip(x_train, y_train)), list(zip(x_test, y_test)), prior


def vertical_split_testset(num_clients, testset):
    testset = get_datasets(num_clients, testset)
    test_left_sets = []
    test_right_sets = []

    for ds in testset:
        test_left_set, test_right_set = split_dataset(ds)
        test_left_sets.append(test_left_set)
        test_right_sets = test_right_sets + test_right_set
    return test_left_sets, test_right_sets


def vertical_split_datasets(num_clients, trainset):
    len_val = len(trainset) // 10  # 10 % validation set
    len_train = len(trainset) - len_val
    lengths = [len_train, len_val]

    trainset, valset = random_split(trainset, lengths, torch.Generator().manual_seed(42))

    trainset = get_datasets(num_clients, trainset)

    valset = get_datasets(num_clients, valset)

    train_left_sets = []
    val_left_sets = []

    train_right_sets = []
    val_right_sets = []
    for ds in trainset:
        train_left_set, train_right_set = split_dataset(ds)
        train_left_sets.append(train_left_set)
        train_right_sets = train_right_sets + train_right_set

    for ds_val in valset:
        val_left_set, val_right_set = split_dataset(ds_val)
        val_left_sets.append(val_left_set)

        val_right_sets = val_right_sets + val_right_set

    return train_left_sets, val_left_sets, train_right_sets, val_right_sets


def split_dataset(ds):
    left_set = []
    right_set = []
    for item in ds:
        (images, ids), label = item
        left, right = images
        left_set.append((left, ids))
        right_set.append((right, label, ids))
    return left_set, right_set


def get_datasets(num_clients, dataset):
    # 纵向划分 MNIST 数据集，假设我们将其划分为左半部分和右半部分
    vertical_split_idx = dataset[0][0].shape[-1] // 2
    # 为每个数据点分配唯一的 ID
    data_ids = list(range(len(dataset)))
    # 创建纵向划分的数据集
    vertical_mnist_data = VerticalMNISTDataset(dataset, vertical_split_idx, data_ids)
    partition_size = len(vertical_mnist_data) // num_clients
    lengths = [partition_size] * num_clients
    datasets = random_split(vertical_mnist_data, lengths, torch.Generator().manual_seed(42))
    return datasets


class VerticalMNISTDataset(Dataset):
    def __init__(self, mnist_data, vertical_split_idx, ids):
        self.mnist_data = mnist_data
        self.vertical_split_idx = vertical_split_idx
        self.ids = ids

    def __len__(self):
        return len(self.mnist_data)

    def __getitem__(self, idx):
        image, label = self.mnist_data[idx]
        image = image[:, :, :self.vertical_split_idx], image[:, :, self.vertical_split_idx:]
        return (image, self.ids[idx]), label


def process_data(x_data, y_data, columns_set1=None, columns_set2=None):
    if columns_set2 is None:
        columns_set2 = COLUMNS_SET2
    if columns_set1 is None:
        columns_set1 = COLUMNS_SET1
    xy_data = pd.concat([x_data, y_data], axis=1)

    left_sets = xy_data[columns_set1]
    right_sets = xy_data[columns_set2]
    labels = xy_data['ISPOTIENTIAL'].values
    ids = xy_data.index

    left_set = list(zip(left_sets.values, ids))
    right_set = list(zip(right_sets.values, labels, ids))

    return left_set, right_set


def reconstruct_data(left_set, right_set, columns_set1=None, columns_set2=None):
    # Unzipping data from sets
    if columns_set2 is None:
        columns_set2 = COLUMNS_SET2
    if columns_set1 is None:
        columns_set1 = COLUMNS_SET1
    left_values, left_ids = zip(*left_set)
    right_values, labels, right_ids = zip(*right_set)

    # Convert the unzipped values to DataFrames
    left_df = pd.DataFrame(left_values, columns=columns_set1, index=left_ids)
    right_df = pd.DataFrame(right_values, columns=columns_set2,
                            index=right_ids)
    right_df['ISPOTIENTIAL'] = labels

    # Ensure that both DataFrames are sorted by index
    left_df = left_df.sort_index()
    right_df = right_df.sort_index()

    # Concatenate DataFrames to get the complete data
    xy_data = pd.concat([left_df, right_df], axis=1)

    return xy_data


def load_dataset(n_labeled, n_unlabeled):
    (x_train, y_train), (x_test, y_test) = get_mnist()
    y_train, y_test = binarize_mnist_class(y_train, y_test)
    xy_train, xy_test, prior = make_dataset(((x_train, y_train), (x_test, y_test)), n_labeled, n_unlabeled)
    return xy_train, xy_test, prior


def load_container_dataset():
    (x_train, y_train), (x_test, y_test) = get_container()

    # # Assuming x_test and y_test are NumPy arrays or lists
    # df_test = pd.DataFrame(x_test)
    # df_test['target'] = y_test
    #
    # # Save to CSV
    # df_test.to_csv('.\\dataset\\test_data.csv', index=False)

    scaler = ['CARGOWGT', 'ARRIVAL_INTERVAL', 'WAIT_INTERVAL', 'WORK_INTERVAL', 'LEAVE_INTERVAL',
              'TRANS_INTERVAL', 'STACK_INTERVAL', 'TJFLC', 'TTIME', 'TCOST', 'JFLC', 'COST', 'TIME']

    # 处理训练集数据
    train_left, train_right = process_data(x_train, y_train, COLUMNS_SET1, COLUMNS_SET2)

    # # 将train_left和train_right拆分为训练集和验证集
    # train_left, val_left, _, _ = train_test_split(train_left, y_train, test_size=0.2, random_state=42)
    # train_right, val_right, train_labels, val_labels = train_test_split(train_right, y_train, test_size=0.2,
    #                                                                     random_state=42)

    # 处理测试集数据
    test_left, test_right = process_data(x_test, y_test, COLUMNS_SET1, COLUMNS_SET2)

    return [train_left], train_right, [train_left], train_right, [test_left], test_right
