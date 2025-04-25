import torch.optim as optim
from torch.utils.data import DataLoader
import dask.array as da
import numpy as np
from .utils import get_parameters, set_parameters, get_batch_by_id, BATCH_SIZE
from collections import Counter


class Server:
    def __init__(self, model, top_model, train_set, val_set, test_set, device, criterion):
        if model is not None:
            self.model = model.to(device)
            self.optimizer = optim.Adam(params=self.model.parameters(), lr=0.001, weight_decay=0.005)
        if top_model is not None:
            self.top_model = top_model.to(device)
            self.top_optimizer = optim.Adam(params=self.top_model.parameters(), lr=0.001, weight_decay=0.005)
        self.train_set = train_set
        self.val_set = val_set
        self.test_set = test_set
        self.device = device
        self.criterion = criterion

        self.train_loader = None
        self.val_loader = None
        self.test_loader = None

    def set_train_set(self, train_set):
        self.train_set = train_set

    def set_model(self, model, top_model, lr, weight_decay):
        self.model = model.to(self.device)
        self.top_model = top_model.to(self.device)

        # self.optimizer = optim.SGD(self.model.parameters(), lr=lr, momentum=0.9)
        # self.top_optimizer = optim.SGD(self.top_model.parameters(), lr=lr, momentum=0.9)
        self.optimizer = optim.Adam(params=self.model.parameters(), lr=lr, weight_decay=weight_decay)
        self.top_optimizer = optim.Adam(params=self.top_model.parameters(), lr=lr, weight_decay=weight_decay)

    def set_criterion(self, criterion):
        self.criterion = criterion

    def get_parameters(self):
        return get_parameters(self.model)

    def set_parameters(self, parameters):
        set_parameters(self.model, parameters)

    def data_intersection(self, ids, is_train="train"):

        if is_train == "train":
            data_set = self.train_set
            loader_attr = 'train_loader'
        elif is_train == "val":
            data_set = self.val_set
            loader_attr = 'val_loader'
        else:
            data_set = self.test_set
            loader_attr = 'test_loader'

        intersect_data = self._filter_and_sort_data(data_set, ids)

        if intersect_data:
            setattr(self, loader_attr, DataLoader(intersect_data, batch_size=BATCH_SIZE, shuffle=False))

        return [image_id for _, _, image_id in intersect_data]

    def _filter_and_sort_data(self, data_set, ids):
        ids_set = set(ids)
        filtered_data = [(image, label, image_id) for image, label, image_id in data_set if image_id in ids_set]
        filtered_data.sort(key=lambda x: x[2])
        return filtered_data

    def compute_dot_prod_matrix_med(self, batch_id, is_train=True):
        if is_train:
            values_array = get_batch_by_id(self.train_loader, batch_id)[0].cpu().numpy()
        else:
            values_array = get_batch_by_id(self.test_loader, batch_id)[0].cpu().numpy()
        dask = da.from_array(values_array, chunks=(BATCH_SIZE, 3))

        med = (da.dot(dask, dask.T)).compute()
        return med

    def compute_norms_squared_med(self, batch_id, is_train=True):
        if is_train:
            values_array = get_batch_by_id(self.train_loader, batch_id)[0].cpu().numpy()
        else:
            values_array = get_batch_by_id(self.test_loader, batch_id)[0].cpu().numpy()
        med = sum(np.multiply(values_array, values_array).T)

        return med

    def get_N_M(self, batch_id, is_train=True):
        # Extract labels from train_right
        if is_train:
            labels = get_batch_by_id(self.train_loader, batch_id)[1].cpu().numpy()
        else:
            labels = get_batch_by_id(self.test_loader, batch_id)[1].cpu().numpy()
        # Count the occurrences of each label
        label_counts = Counter(labels)
        N = label_counts[-1]
        M = label_counts[1]

        return N, M

    def update_parameters(self, gradients, optimizer):
        """
        Update model parameters using the provided gradients and optimizer.

        Parameters:
        - gradients (list of torch.Tensor): List of gradients corresponding to each model parameter.
        - optimizer (torch.optim.Optimizer): Optimizer used for the parameter update.
        """
        # Ensure that the number of gradients matches the number of parameters
        if len(gradients) != len(list(self.model.parameters())):
            raise ValueError("Number of gradients does not match number of parameters.")

        # Zero the gradients of the model parameters
        optimizer.zero_grad()

        # Update each parameter with its corresponding gradient
        for param, gradient in zip(self.model.parameters(), gradients):
            # Ensure that the gradient and parameter sizes match
            if param.size() != gradient.size():
                raise RuntimeError(f"Gradient size {gradient.size()} does not match parameter size {param.size()}")

            param.grad = gradient

        # Perform a parameter update step
        optimizer.step()



