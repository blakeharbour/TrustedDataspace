from django.db import models

# Create your models here.
import os

# os.environ['DJANGO_SETTINGS_MODULE'] = 'hotel.settings'   # myweb是改成自己的项目名称



# import torch
# import torch.nn as nn
# import torch.nn.functional as F

class SampleAlignment(models.Model):
    # Assuming you want 'id' to be a primary key
    id = models.AutoField(primary_key=True)
    SAMPLE_NUM = models.CharField(max_length=255)
    SAMPLE_NUM_SUCCESS = models.CharField(max_length=255)

    def __str__(self):
        return f"SampleAlignment - ID: {self.id}, Sample ID: {self.SAMPLE_NUM}, Alignment Result: {self.SAMPLE_NUM_SUCCESS}"


