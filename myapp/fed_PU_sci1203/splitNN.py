from typing import List

import numpy as np
import torch.nn as nn
import torch.nn.functional as F


def get_parameters(net) -> List[np.ndarray]:
    return [val.cpu().numpy() for _, val in net.state_dict().items()]


class SyNet_client(nn.Module):
    def __init__(self):
        super(SyNet_client, self).__init__()
        self.l1 = nn.Linear(392, 128, bias=False)
        self.b1 = nn.BatchNorm1d(128)
        self.l2 = nn.Linear(128, 128, bias=False)
        self.b2 = nn.BatchNorm1d(128)
        self.l3 = nn.Linear(128, 128, bias=False)
        self.b3 = nn.BatchNorm1d(128)
        self.l4 = nn.Linear(128, 128, bias=False)
        self.b4 = nn.BatchNorm1d(128)

    def forward(self, x):
        h = self.l1(x)
        h = self.b1(h)
        h = F.relu(h)
        h = self.l2(h)
        h = self.b2(h)
        h = F.relu(h)
        h = self.l3(h)
        h = self.b3(h)
        h = F.relu(h)
        h = self.l4(h)
        h = self.b4(h)
        h = F.relu(h)

        return h


class SyNet_client_coleft(nn.Module):
    def __init__(self):
        super(SyNet_client_coleft, self).__init__()

        self.l1 = nn.Linear(20, 28, bias=False)
        self.b1 = nn.BatchNorm1d(28)
        self.l2 = nn.Linear(28, 28, bias=False)
        self.b2 = nn.BatchNorm1d(28)
        self.l3 = nn.Linear(28, 28, bias=False)
        self.b3 = nn.BatchNorm1d(28)

    def forward(self, x):
        h = F.relu(self.b1(self.l1(x)))
        h = F.relu(self.b2(self.l2(h)))
        h = F.relu(self.b3(self.l3(h)))
        return h


class SyNet_client_coright(nn.Module):
    def __init__(self):
        super(SyNet_client_coright, self).__init__()
        self.l1 = nn.Linear(5, 4, bias=False)
        self.b1 = nn.BatchNorm1d(4)
        self.l2 = nn.Linear(4, 4, bias=False)
        self.b2 = nn.BatchNorm1d(4)
        self.l3 = nn.Linear(4, 4, bias=False)
        self.b3 = nn.BatchNorm1d(4)

    def forward(self, x):
        h = self.l1(x)
        h = self.b1(h)
        h = F.relu(h)
        h = self.l2(h)
        h = self.b2(h)
        h = F.relu(h)
        h = self.l3(h)
        h = self.b3(h)
        h = F.relu(h)
        return h


class SyNet_server_co(nn.Module):
    def __init__(self):
        super(SyNet_server_co, self).__init__()

        self.l1 = nn.Linear(32, 32, bias=False)
        self.b1 = nn.BatchNorm1d(32)
        self.l2 = nn.Linear(32, 32, bias=False)
        self.b2 = nn.BatchNorm1d(32)
        self.l3 = nn.Linear(32, 32, bias=False)
        self.b3 = nn.BatchNorm1d(32)
        self.l4 = nn.Linear(32, 1, bias=False)

    def forward(self, x):
        h = self.l1(x)
        h = self.b1(h)
        h = F.relu(h)
        h = self.l2(h)
        h = self.b2(h)
        h = F.relu(h)
        h = self.l3(h)
        h = self.b3(h)
        h = F.relu(h)
        h = self.l4(h)
        return h


class SyNet_server(nn.Module):
    def __init__(self):
        super(SyNet_server, self).__init__()
        self.l5 = nn.Linear(256, 256, bias=False)
        self.b5 = nn.BatchNorm1d(256)
        self.l6 = nn.Linear(256, 256, bias=False)
        self.b6 = nn.BatchNorm1d(256)
        self.l7 = nn.Linear(256, 1, bias=False)

    def forward(self, x):
        h = self.l5(x)
        h = self.b5(h)
        h = F.relu(h)
        h = self.l6(h)
        h = self.b6(h)
        h = F.relu(h)
        h = self.l7(h)
        return h


def intersection_find(id_tensors, server_set):
    id_list = list(id_tensors)
    dl2 = [data for data, labels, ids in server_set if ids in id_list]
    labels = [labels for data, labels, ids in server_set if ids in id_list]
    return dl2, labels
