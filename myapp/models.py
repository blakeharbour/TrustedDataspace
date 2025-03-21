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

class LoginUser(models.Model):
    account = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    com = models.CharField(max_length=255)
    comid = models.IntegerField(default=0)

    class Meta:
        db_table = 'login_user'  # 确保数据库表名是 'login_user'

    def __str__(self):
        return self.account

class DataAsset(models.Model):
    assetID = models.AutoField(primary_key=True)
    # 数据资产名称
    assetName = models.CharField(max_length=100, verbose_name="名称")
    # 数据所有者
    assetOwner = models.CharField(max_length=100, verbose_name="所有者")
    # 数据字段描述
    description = models.TextField(verbose_name="描述")
    # 数据格式
    assetFormat = models.CharField(max_length=50, verbose_name="格式")
    # 数据安全等级
    SECURITY_LEVEL_CHOICES = [
        ('L1', '高敏感密文'),
        ('L2', '高敏感'),
        ('L3', '敏感'),
        ('L4', '低敏感'),
    ]
    assetLevel = models.CharField(max_length=10, choices=SECURITY_LEVEL_CHOICES, verbose_name="安全等级")
    # 项目状态
    STATUS_CHOICES = [
        ('pending', '未开始'),
        ('started', '开始'),
        ('completed', '完成'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    # 访问路径
    assetPath = models.CharField(max_length=200, blank=True, null=True, verbose_name="访问路径")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "数据资产"
        verbose_name_plural = "数据资产"
class AssetRecord(models.Model):
    assetName = models.CharField(max_length=255, verbose_name="资产名称")
    assetOwner = models.CharField(max_length=255, verbose_name="资产所有者")
    assetField = models.CharField(max_length=255, verbose_name="资产字段")
    assetFormat = models.CharField(max_length=100, verbose_name="资产格式")
    assetLevel = models.CharField(max_length=100, verbose_name="资产级别")
    assetPath = models.CharField(max_length=255, verbose_name="资产路径")
    star_status = models.CharField(max_length=50, verbose_name="开始状态",default='默认值')
    end_status = models.CharField(max_length=50, verbose_name="结束状态",default='默认值')
    txTime = models.DateTimeField(verbose_name="交易时间")
    txID = models.CharField(max_length=255, verbose_name="交易ID")
    txHash = models.CharField(max_length=255, verbose_name="交易哈希")


    def __str__(self):
        return self.assetName  # 用于在 Django Admin 或其他地方显示记录的名称

    class Meta:
        db_table = 'myapp_assetrecord'
        verbose_name = "资产记录"  # 在 Django Admin 中显示的名称
        verbose_name_plural = "资产记录"  # 复数形式