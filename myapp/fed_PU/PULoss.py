import torch
import torch.nn as nn
import torch.nn.functional as F


class PULoss(nn.Module):
    """Loss function for PU learning"""

    def __init__(self, prior, loss_func=lambda x: torch.sigmoid(-x), gamma=1, beta=0, nnpu=True):
        super(PULoss, self).__init__()
        if not 0 < prior < 1:
            raise ValueError("The class prior should be in (0, 1)")
        self.prior = prior
        self.gamma = gamma
        self.beta = beta
        self.loss_func = loss_func
        self.nnpu = nnpu
        self.positive = 1
        self.unlabeled = -1

    def forward(self, x, t):
        positive = (t == self.positive)
        unlabeled = (t == self.unlabeled)
        n_positive = max(1, positive.sum())
        n_unlabeled = max(1, unlabeled.sum())
        y_positive = self.loss_func(x)
        y_unlabeled = self.loss_func(-x)

        positive_risk = (self.prior * positive.float() / n_positive * y_positive).sum()
        negative_risk = (
                (unlabeled.float() / n_unlabeled - self.prior * positive.float() / n_positive) * y_unlabeled).sum()

        objective = positive_risk + negative_risk
        if self.nnpu:
            if negative_risk.item() < -self.beta:
                objective = positive_risk - self.beta
                x_out = -self.gamma * negative_risk
            else:
                x_out = objective
        else:
            x_out = objective
        return x_out


class ImPULoss(nn.Module):
    """Loss function for PU learning"""

    def __init__(self, prior, prior_, loss_func=lambda x: torch.sigmoid(-x), gamma=1, beta=0, nnpu=True):
        super(ImPULoss, self).__init__()
        if not 0 < prior < 1:
            raise ValueError("The class prior should be in (0, 1)")
        self.prior = prior
        self.prior_ = prior_
        self.gamma = gamma
        self.beta = beta
        self.loss_func = loss_func
        self.nnpu = nnpu
        self.positive = 1
        self.unlabeled = -1

    def forward(self, x, t):
        positive = (t == self.positive)
        unlabeled = (t == self.unlabeled)
        n_positive = max(1, positive.sum())
        n_unlabeled = max(1, unlabeled.sum())
        y_positive = self.loss_func(x)
        y_unlabeled = self.loss_func(-x)

        positive_risk = (self.prior_ * positive.float() / n_positive * y_positive).sum()
        negative_risk = (
                (unlabeled.float() / n_unlabeled - self.prior * positive.float() / n_positive) * (1 - self.prior_) / (1 - self.prior) * y_unlabeled).sum()

        objective = positive_risk + negative_risk
        if self.nnpu:
            if negative_risk.item() < -self.beta:
                objective = positive_risk - self.beta
                x_out = -self.gamma * negative_risk
            else:
                x_out = objective
        else:
            x_out = objective
        return x_out


class nnPUSBloss(nn.Module):
    """Loss function for PUSB learning."""

    def __init__(self, prior, gamma=1, beta=0):
        super(nnPUSBloss, self).__init__()
        if not 0 < prior < 1:
            raise NotImplementedError("The class prior should be in (0, 1)")
        self.prior = prior
        self.gamma = gamma
        self.beta = beta
        self.positive = 1
        self.unlabeled = -1
        self.eps = 1e-7

    def forward(self, x, t):
        # clip the predict value to make the following optimization problem well-defined.
        x = torch.clamp(x, min=self.eps, max=1 - self.eps)

        positive = (t == self.positive)
        unlabeled = (t == self.unlabeled)
        n_positive = max(1, positive.sum())
        n_unlabeled = max(1, unlabeled.sum())
        y_positive = -torch.log(x)
        y_unlabeled = -torch.log(1 - x)
        positive_risk = (self.prior * positive.float() / n_positive * y_positive).sum()
        negative_risk = (
                (unlabeled.float() / n_unlabeled - self.prior * positive.float() / n_positive) * y_unlabeled).sum()

        objective = positive_risk + negative_risk

        if negative_risk.item() < -self.beta:
            objective = positive_risk - self.beta
            x_out = -self.gamma * negative_risk
        else:
            x_out = objective

        return x_out


class ImnnPUSBloss(nn.Module):
    """Loss function for PUSB learning."""

    def __init__(self, prior, prior_, gamma=1, beta=0):
        super(ImnnPUSBloss, self).__init__()
        if not 0 < prior < 1:
            raise NotImplementedError("The class prior should be in (0, 1)")
        self.prior = prior
        self.prior_ = prior_
        self.gamma = gamma
        self.beta = beta
        self.positive = 1
        self.unlabeled = -1
        self.eps = 1e-7

    def forward(self, x, t):
        # clip the predict value to make the following optimization problem well-defined.
        x = torch.clamp(x, min=self.eps, max=1 - self.eps)

        positive = (t == self.positive)
        unlabeled = (t == self.unlabeled)
        n_positive = max(1, positive.sum())
        n_unlabeled = max(1, unlabeled.sum())
        y_positive = -torch.log(x)
        y_unlabeled = -torch.log(1 - x)
        positive_risk = (self.prior * positive.float() / n_positive * y_positive).sum()
        negative_risk = (
                (unlabeled.float() / n_unlabeled - self.prior * positive.float() / n_positive) * (1 - self.prior_) / (1 - self.prior) * y_unlabeled).sum()

        objective = positive_risk + negative_risk

        if negative_risk.item() < -self.beta:
            objective = positive_risk - self.beta
            x_out = -self.gamma * negative_risk
        else:
            x_out = objective

        return x_out
