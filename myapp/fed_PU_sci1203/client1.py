import dask.array as da
import numpy as np
import torch.optim as optim
from torch.utils.data import DataLoader

from .utils import get_parameters, set_parameters, get_batch_by_id, BATCH_SIZE


class Client:
    def __init__(self, model, train_set, val_set, test_set, device):
        if model is not None:
            self.model = model.to(device)
            self.optimizer = optim.Adam(params=self.model.parameters(), lr=0.002, weight_decay=0.005)
        self.train_set = train_set
        self.val_set = val_set
        self.test_set = test_set
        self.device = device

        self.train_loader = None
        self.val_loader = None
        self.test_loader = None

    def set_train_set(self, train_set):
        self.train_set = train_set
    def set_model(self, model, lr, weight_decay):
        self.model = model.to(self.device)

        # self.optimizer = optim.SGD(self.model.parameters(), lr=lr, momentum=0.9)
        self.optimizer = optim.Adam(params=self.model.parameters(), lr=lr, weight_decay=weight_decay)

    def get_parameters(self):
        return get_parameters(self.model)

    def set_parameters(self, parameters):
        set_parameters(self.model, parameters)

    def get_data_ids(self, is_train="train"):
        dataset_mapping = {
            "train": self.train_set,
            "val": self.val_set,
            "test": self.test_set
        }

        ids = [image_id for _, image_id in dataset_mapping.get(is_train, [])]

        return ids

    def set_dataloader(self, ids, is_train="train"):
        ids_set = set(ids)  # Convert to set for faster membership checking

        if is_train == "train":
            dataset = self.train_set
            target_loader = 'train_loader'
        elif is_train == "val":
            dataset = self.val_set
            target_loader = 'val_loader'
        elif is_train == "test":
            dataset = self.test_set
            target_loader = 'test_loader'
        else:
            raise ValueError("Invalid value for is_train")

        # 先获取满足条件的 (image, image_id) 对
        filtered_data = [(image, image_id) for image, image_id in dataset if image_id in ids_set]
        # 根据 image_id 排序
        sorted_data = sorted(filtered_data, key=lambda x: x[1])
        # 从排序后的数据中提取 images
        data = [image for image, image_id in sorted_data]

        # Set the DataLoader if data is not empty
        if len(data) > 0:
            setattr(self, target_loader, DataLoader(data, batch_size=BATCH_SIZE, shuffle=False))

    def compute_dot_prod_matrix_med(self, batch_id, is_train=True):
        if is_train:
        # Convert lists to NumPy arrays
            values_array = get_batch_by_id(self.train_loader, batch_id).cpu().numpy()
        else:
            values_array = get_batch_by_id(self.test_loader, batch_id).cpu().numpy()
        # Create dask arrays (you can specify chunks)

        dask = da.from_array(values_array, chunks=(BATCH_SIZE, 21))

        med = (da.dot(dask, dask.T)).compute()
        return med

    def compute_norms_squared_med(self, batch_id, is_train=True):
        if is_train:
            values_array = get_batch_by_id(self.train_loader, batch_id).cpu().numpy()
        else:
            values_array = get_batch_by_id(self.test_loader, batch_id).cpu().numpy()

        med = sum(np.multiply(values_array, values_array).T)

        return med
