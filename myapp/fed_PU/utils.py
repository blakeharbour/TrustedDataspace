from collections import OrderedDict
from typing import List

import pandas as pd
import torch
from matplotlib import pyplot as plt

from .Kernal_MPE import KM2_estimate

BATCH_SIZE = 8000

import numpy as np
from sklearn.utils import resample


def compute_prior(server_client, Clients, is_train=True):
    priors = []
    train_nums = []
    if is_train:
        for batch_id, (inputs, labels, _) in enumerate(server_client.train_loader):
            prior = get_prior(Clients, server_client, batch_id, is_train)
            priors.append(prior)
            print("prior: " + str(prior))
            train_nums.append(inputs.shape[0])
    else:
        for batch_id, (inputs, labels, _) in enumerate(server_client.test_loader):
            prior = get_prior(Clients, server_client, batch_id, is_train)
            priors.append(prior)
            print("prior: " + str(prior))
            train_nums.append(inputs.shape[0])
    prior = sum([a * b for a, b in zip(priors, train_nums)]) / sum(train_nums)
    prior = round(prior, 4)
    return prior


def resample_data(xy_data):
    # 分别提取正样本和负样本
    pos_data = xy_data[xy_data['ISPOTIENTIAL'] == 1]
    neg_data = xy_data[xy_data['ISPOTIENTIAL'] == -1]

    # 判断是过采样还是欠采样
    if len(pos_data) < len(neg_data):
        # 过采样正样本
        pos_data_resampled = resample(pos_data, replace=True, n_samples=len(neg_data) - len(pos_data), random_state=123)
        xy_data_resampled = pd.concat([neg_data, pos_data, pos_data_resampled])
    else:
        # 过采样负样本
        neg_data_resampled = resample(neg_data, replace=True, n_samples=len(pos_data) - len(neg_data), random_state=123)
        xy_data_resampled = pd.concat([neg_data, pos_data, neg_data_resampled])

    return xy_data_resampled


def get_parameters(net) -> List[np.ndarray]:
    return [val.cpu().numpy() for _, val in net.state_dict().items()]


def set_parameters(net, parameters: List[np.ndarray]):
    params_dict = zip(net.state_dict().keys(), parameters)
    state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
    net.load_state_dict(state_dict, strict=True)


from itertools import islice


def get_batch_by_id(data_loader, batch_id):
    return next(islice(data_loader, batch_id, batch_id + 1), None)


def get_prior(clients, server, batch_id, is_train=True):
    dot_prod_matrix = None
    norms_squared = None
    # 计算prior
    for client in clients:
        dot_prod_matrix_med = client.compute_dot_prod_matrix_med(batch_id, is_train)
        if dot_prod_matrix is None:
            dot_prod_matrix = np.zeros_like(dot_prod_matrix_med)
        dot_prod_matrix += dot_prod_matrix_med

        norms_squared_med = client.compute_norms_squared_med(batch_id, is_train)
        if norms_squared is None:
            norms_squared = np.zeros_like(norms_squared_med)
        norms_squared += norms_squared_med

    dot_prod_matrix += server.compute_dot_prod_matrix_med(batch_id, is_train)

    norms_squared += server.compute_norms_squared_med(batch_id, is_train)

    N, M = server.get_N_M(batch_id, is_train)

    if N != 0 and M != 0:

        prior_ = KM2_estimate(dot_prod_matrix, norms_squared, N, M)
    else:
        prior_ = 0.1

    return prior_


def get_train_with_positive_half(negative_data, positive_data):
    chunks = []

    num_chunks = int(np.ceil(len(negative_data) + len(positive_data)) / BATCH_SIZE)

    negative_idx = list(negative_data.index)
    positive_idx = list(positive_data.index)

    np.random.seed(42)
    np.random.shuffle(negative_idx)
    np.random.seed(42)
    np.random.shuffle(positive_idx)

    for _ in range(num_chunks):
        # Check and replenish positive_idx and negative_idx if empty
        if not positive_idx:
            positive_idx = list(positive_data.index)
            np.random.shuffle(positive_idx)
        if not negative_idx:
            negative_idx = list(negative_data.index)
            np.random.shuffle(negative_idx)
        # Always extract at least one positive and one negative
        chunk_positives = [positive_idx.pop(0)]
        chunk_negatives = [negative_idx.pop(0)]

        num_remaining = BATCH_SIZE - 2

        # Randomly determine the number of additional positive samples for this chunk
        num_additional_positives = np.random.randint(num_remaining * .48, num_remaining * .6 + 1)
        num_additional_negatives = num_remaining - num_additional_positives

        # If positive_idx or negative_idx is not enough, replenish and shuffle
        while len(positive_idx) < num_additional_positives:
            additional_positives = list(positive_data.index)
            np.random.shuffle(additional_positives)
            positive_idx.extend(additional_positives)

        while len(negative_idx) < num_additional_negatives:
            additional_negatives = list(negative_data.index)
            np.random.shuffle(additional_negatives)
            negative_idx.extend(additional_negatives)

        # Extract indices for this chunk
        chunk_positives.extend(positive_idx[:num_additional_positives])
        chunk_negatives.extend(negative_idx[:num_additional_negatives])

        # Remove the used indices
        positive_idx = positive_idx[num_additional_positives:]
        negative_idx = negative_idx[num_additional_negatives:]

        # Form the chunk and shuffle
        chunk = pd.concat([negative_data.loc[chunk_negatives], positive_data.loc[chunk_positives]]).sample(
            frac=1).reset_index(drop=True)
        chunks.append(chunk)

    # Combine all chunks
    train_data = pd.concat(chunks).reset_index(drop=True)
    return train_data


def get_train_with_positive(negative_data, positive_data):
    chunks = []

    num_chunks = int(np.ceil(len(negative_data) + len(positive_data)) / BATCH_SIZE)

    negative_idx = list(negative_data.index)
    positive_idx = list(positive_data.index)

    np.random.seed(42)
    np.random.shuffle(negative_idx)
    np.random.seed(42)
    np.random.shuffle(positive_idx)

    for _ in range(num_chunks):
        # Check and replenish positive_idx and negative_idx if empty
        if not positive_idx:
            positive_idx = list(positive_data.index)
            np.random.shuffle(positive_idx)
        if not negative_idx:
            negative_idx = list(negative_data.index)
            np.random.shuffle(negative_idx)
        # Always extract at least one positive and one negative
        chunk_positives = [positive_idx.pop(0)]
        chunk_negatives = [negative_idx.pop(0)]

        num_remaining = BATCH_SIZE - 2

        # Randomly determine the number of additional positive samples for this chunk
        num_additional_positives = np.random.randint(0, num_remaining / 2 + 1)
        num_additional_negatives = num_remaining - num_additional_positives

        # If positive_idx or negative_idx is not enough, replenish and shuffle
        while len(positive_idx) < num_additional_positives:
            additional_positives = list(positive_data.index)
            np.random.shuffle(additional_positives)
            positive_idx.extend(additional_positives)

        while len(negative_idx) < num_additional_negatives:
            additional_negatives = list(negative_data.index)
            np.random.shuffle(additional_negatives)
            negative_idx.extend(additional_negatives)

        # Extract indices for this chunk
        chunk_positives.extend(positive_idx[:num_additional_positives])
        chunk_negatives.extend(negative_idx[:num_additional_negatives])

        # Remove the used indices
        positive_idx = positive_idx[num_additional_positives:]
        negative_idx = negative_idx[num_additional_negatives:]

        # Form the chunk and shuffle
        chunk = pd.concat([negative_data.loc[chunk_negatives], positive_data.loc[chunk_positives]]).sample(
            frac=1).reset_index(drop=True)
        chunks.append(chunk)

    # Combine all chunks
    train_data = pd.concat(chunks).reset_index(drop=True)
    return train_data


def image_concat(data, data2, target):
    image1 = data.permute(0, 2, 3, 1).numpy()
    image2 = data2.permute(0, 2, 3, 1).numpy()
    images = np.concatenate((image1, image2), axis=2)
    # Create a figure and a grid of subplots
    fig, axs = plt.subplots(4, 8, figsize=(12, 6))
    # Loop over the images and plot them
    for i, ax in enumerate(axs.flat):
        ax.imshow(images[i])
        ax.set_title(str(target[1].item()))
        ax.axis("off")
    # Show the plot
    fig.tight_layout()
    plt.show()


class EarlyStopping:
    def __init__(self, patience=10, delta=0, verbose=False):
        self.patience = patience
        self.counter = 0
        self.best_score = None
        self.delta = delta
        self.verbose = verbose
        self.early_stop = False

    def __call__(self, val_loss):
        score = -val_loss

        if self.best_score is None:
            self.best_score = score
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.counter = 0

        return self.early_stop
