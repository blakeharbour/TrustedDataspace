import numpy as np
import torch


class PUEvaluator:

    def __init__(self, prior, model1, model2, top_model, client_dataloader, server_dataloader, criterion, device):
        self.prior = prior
        self.model1 = model1
        self.model2 = model2
        self.top_model = top_model

        self.client_dataloader = client_dataloader
        self.server_dataloader = server_dataloader
        self.criterion = criterion
        self.device = device

    def evaluate(self):
        presicion = []
        recall = []
        error_rate = []
        loss_ = []
        with torch.no_grad():
            self.model1.eval()
            self.model2.eval()
            self.top_model.eval()
            for data1, (data2, target, _) in zip(self.client_dataloader, self.server_dataloader):


                data1 = data1.reshape(data1.shape[0], -1).to(self.device).float()
                output1 = self.model1(data1)


                data2 = data2.reshape(data2.shape[0], -1).to(self.device).float()
                t = target.detach().cpu().numpy()
                size = len(t)

                output2 = self.model2(data2)

                output = torch.cat((output1, output2), 1)

                final_output = self.top_model(output)

                h = np.reshape(final_output.detach().cpu().numpy(), size)
                h = self.predict_with_density_threshold(h, t, self.prior)

                target = target.to(self.device).view(-1, 1).float()
                loss = self.criterion(final_output, target)
                # evalution
                result = self.zero_one_loss(h, t)
                loss_.append(loss.item())
                presicion.append(result[0])
                recall.append(result[1])
                error_rate.append(result[2])
            return sum(presicion) / len(presicion), sum(recall) / len(recall), sum(error_rate) / len(error_rate), sum(
                loss_) / len(loss_)

    def error(self, is_logistic=False):
        presicion = []
        recall = []
        error_rate = []
        loss_ = []
        with torch.no_grad():
            self.model1.eval()
            self.model2.eval()
            self.top_model.eval()
            for data1, (data2, target, _) in zip(self.client_dataloader, self.server_dataloader):

                data1 = data1.reshape(data1.shape[0], -1).to(self.device).float()
                output1 = self.model1(data1)

                data2 = data2.reshape(data2.shape[0], -1).to(self.device).float()
                t = target.detach().cpu().numpy()
                size = len(t)

                output2 = self.model2(data2)

                output = torch.cat((output1, output2), 1)

                final_output = self.top_model(output)

                if is_logistic:
                    h = np.reshape(torch.sigmoid(
                        final_output).detach().cpu().numpy(), size)
                    h = np.where(h > 0.5, 1, -1).astype(np.int32)
                else:
                    h = np.reshape(torch.sign(
                        final_output).detach().cpu().numpy(), size)

                target = target.to(self.device).view(-1, 1).float()
                loss = self.criterion(final_output, target)
                loss_.append(loss.item())
                # evalution
                result = self.zero_one_loss(h, t)

                presicion.append(result[0])
                recall.append(result[1])
                error_rate.append(result[2])

            return sum(presicion) / len(presicion), sum(recall) / len(recall), sum(error_rate) / len(error_rate), sum(
                loss_) / len(loss_)

    def predict_with_density_threshold(self, f_x, target, prior):
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

    def zero_one_loss(self, h, t):
        positive = 1
        negative = -1

        n_p = (t == positive).sum()
        n_n = (t == negative).sum()
        size = n_p + n_n

        t_p = ((h == positive) * (t == positive)).sum()
        t_n = ((h == negative) * (t == negative)).sum()
        f_p = n_n - t_n
        f_n = n_p - t_p

        # print("size:{0},t_p:{1},t_n:{2},f_p:{3},f_n:{4}".format(
        #     size, t_p, t_n, f_p, f_n))

        presicion = (0.0 if t_p == 0 else t_p / (t_p + f_p))
        recall = (0.0 if t_p == 0 else t_p / (t_p + f_n))

        return presicion, recall, 1 - (t_p + t_n) / size


class MultiPUEvaluator:

    def __init__(self, prior, model1, model2, top_model, client_dataloader, server_dataloader, device):
        self.prior = prior
        self.model1 = model1
        self.model2 = model2
        self.top_model = top_model

        self.client_dataloader = client_dataloader
        self.server_dataloader = server_dataloader

        self.device = device

    def compute_summary(self, summary):
        prior = self.prior
        computed_summary = {}
        for k, values in summary.items():
            t_p, t_u, f_p, f_u = values
            n_p = t_p + f_u
            n_u = t_u + f_p
            error_p = 1 - t_p / n_p
            error_u = 1 - t_u / n_u
            computed_summary[k] = 2 * prior * error_p + error_u - prior
        return computed_summary

    def evaluate(self):
        summary = {name: np.zeros(4) for name in ['fed_pu']}
        with torch.no_grad():
            self.model1.eval()
            self.model2.eval()
            self.top_model.eval()
            for batch_idx, data in enumerate(self.client_dataloader):

                data1 = data.reshape(data.shape[0], -1).to(self.device).float()
                output1 = self.model1(data1)

                data2 = None
                target = None
                for batch_id, (inputs, labels) in enumerate(self.server_dataloader):
                    if batch_id == batch_idx:
                        data2 = inputs
                        target = labels
                        break
                assert data2 is not None

                assert target is not None

                data2 = data2.reshape(data2.shape[0], -1).to(self.device).float()
                target = target.to(self.device)

                output2 = self.model2(data2)

                output = torch.cat((output1, output2), 1)

                final_output = self.top_model(output)

                summary['fed_pu'] += self.compute_prediction_summary(final_output, target)
            computed_summary = self.compute_summary(summary)
            return {k: v.mean() for k, v in computed_summary.items()}

    def compute_prediction_summary(self, outputs, targets):
        outputs = torch.sign(outputs).view(-1).cpu().numpy()
        targets = targets.cpu().numpy()
        n_p = (targets == 1).sum()
        n_n = (targets == -1).sum()
        t_p = ((outputs == 1) & (targets == 1)).sum()
        t_n = ((outputs == -1) & (targets == -1)).sum()
        f_p = n_n - t_n
        f_n = n_p - t_p
        return np.array([t_p, t_n, f_p, f_n])
