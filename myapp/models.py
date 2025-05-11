from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class SampleAlignment(models.Model):
    # Assuming you want 'id' to be a primary key
    id = models.AutoField(primary_key=True)
    SAMPLE_NUM = models.CharField(max_length=255)
    SAMPLE_NUM_SUCCESS = models.CharField(max_length=255)

    def __str__(self):
        return f"SampleAlignment - ID: {self.id}, Sample ID: {self.SAMPLE_NUM}, Alignment Result: {self.SAMPLE_NUM_SUCCESS}"


class CustomUserManager(BaseUserManager):
    def create_user(self, account, password=None, **extra_fields):
        if not account:
            raise ValueError('必须提供账号(account)')
        print(f"[DEBUG] 原始密码: {password}")
        user = self.model(account=account,**extra_fields)
        user.set_password(password)  # 加密密码
        print(f"[DEBUG] 加密后密码: {user.password}")
        user.save()
        return user

    def create_superuser(self, account, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(account, password,**extra_fields)

class LoginUser(AbstractBaseUser, PermissionsMixin):  # 关键！继承 AbstractBaseUser
    account = models.CharField(max_length=255, unique=True, verbose_name="账号")
    password = models.CharField(max_length=255, verbose_name="密码")  # 存储加密后的密码
    com = models.CharField(max_length=255, verbose_name="所属公司")
    comid = models.IntegerField(default=0, verbose_name="公司ID")

    # Django 认证系统必要字段
    last_login = models.DateTimeField(_("last login"), default=timezone.now)
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    is_staff = models.BooleanField(default=False, verbose_name="管理后台权限")


    USERNAME_FIELD = 'account'  # 登录标识字段
    REQUIRED_FIELDS = []  # 创建超级用户时的必填字段

    objects = CustomUserManager()

    class Meta:
        db_table = 'login_user'  # 绑定到现有表
        verbose_name = '用户'
        verbose_name_plural = '用户'

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
    # STATUS_CHOICES = [
    #     ('pending', '未开始'),
    #     ('started', '开始'),
    #     ('completed', '完成'),
    # ]
    status = models.CharField(max_length=20, blank=True, null=True, verbose_name="状态")
    # # 访问路径
    assetPath = models.CharField(max_length=200, default='无', verbose_name="访问路径")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "数据资产"
        verbose_name_plural = "数据资产"
class AssetRecord(models.Model):
    assetName = models.CharField(max_length=255, verbose_name="资产名称")
    assetOwner =models.CharField(max_length=255, verbose_name="资产所有者")
    assetFormat = models.CharField(max_length=100, verbose_name="资产格式")
    assetLevel = models.CharField(max_length=100, verbose_name="资产级别")
    assetPath = models.CharField(max_length=255, verbose_name="资产路径")
    star_status = models.CharField(max_length=50, verbose_name="开始状态",default='默认值')
    end_status = models.CharField(max_length=50, verbose_name="结束状态",default='默认值')
    operation = models.CharField(max_length=50, verbose_name="操作", default='默认值')
    txTime = models.DateTimeField(verbose_name="交易时间",null=True, blank=True)
    txID = models.CharField(max_length=255, verbose_name="交易ID",null=True, blank=True)
    txHash = models.CharField(max_length=255, verbose_name="交易哈希",null=True, blank=True)


    def __str__(self):
        return self.assetName  # 用于在 Django Admin 或其他地方显示记录的名称

    class Meta:
        db_table = 'asset_record'
        verbose_name = "资产记录"  # 在 Django Admin 中显示的名称
        verbose_name_plural = "资产记录"  # 复数形式

#####数据确权AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
class DataRights(models.Model):
    # 基本信息
    data_name = models.CharField(max_length=255, verbose_name="数据名称")
    data_description = models.TextField(verbose_name="数据内容描述")

    # 业务环节分类
    BUSINESS_STAGE_CHOICES = [
        ('货物申报数据', '货物申报数据'),
        ('通关检验数据', '通关检验数据'),
        ('物流运输数据', '物流运输数据'),
        ('交接交付数据', '交接交付数据'),
    ]
    business_stage = models.CharField(max_length=50, choices=BUSINESS_STAGE_CHOICES, verbose_name="业务环节分类")

    # 数据关系类型
    RELATIONSHIP_TYPE_CHOICES = [
        ('原始数据', '原始数据'),
        ('衍生数据', '衍生数据'),
    ]
    relationship_type = models.CharField(max_length=50, choices=RELATIONSHIP_TYPE_CHOICES, verbose_name="数据关系类型")

    # 数据来源信息
    DATA_SOURCE_CHOICES = [
        ('海关', '海关'),
        ('港口', '港口'),
        ('铁路', '铁路'),
        ('哈方', '哈方'),
    ]
    data_source = models.CharField(max_length=50, choices=DATA_SOURCE_CHOICES, verbose_name="数据来源方")
    is_original_generator = models.BooleanField(default=True, verbose_name="是否为数据原始生成者")

    # 衍生数据信息（仅当relationship_type为'衍生数据'时使用）
    original_provider = models.CharField(max_length=50, choices=DATA_SOURCE_CHOICES, null=True, blank=True,
                                         verbose_name="原始数据提供方")

    PROCESSING_LEVEL_CHOICES = [
        ('轻度加工', '轻度加工（简单整理、格式转换）'),
        ('深度加工', '深度加工（算法分析、模型应用）'),
        ('创造性加工', '创造性加工（生成新指标或见解）'),
    ]
    processing_level = models.CharField(max_length=50, choices=PROCESSING_LEVEL_CHOICES, null=True, blank=True,
                                        verbose_name="加工程度")

    # 数据格式
    DATA_FORMAT_CHOICES = [
        ('CSV文件', 'CSV文件'),
        ('Excel表格', 'Excel表格'),
        ('数据库表', '数据库表'),
        ('JSON数据', 'JSON数据'),
        ('XML文档', 'XML文档'),
        ('其他', '其他'),
    ]
    data_format = models.CharField(max_length=50, choices=DATA_FORMAT_CHOICES, verbose_name="数据格式")

    # 时间覆盖范围
    time_range_start = models.DateField(verbose_name="时间范围起始")
    time_range_end = models.DateField(null=True, blank=True, verbose_name="时间范围结束")
    is_present = models.BooleanField(default=False, verbose_name="时间范围延续至今")

    # 确权结果
    resource_holding_right = models.BooleanField(default=False, verbose_name="数据资源持有权")
    processing_use_right = models.BooleanField(default=False, verbose_name="数据加工使用权")
    right_source = models.CharField(max_length=255, verbose_name="权限依据")

    # 记录创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.data_name

    class Meta:
        db_table = 'data_rights'
        verbose_name = "数据确权"
        verbose_name_plural = "数据确权"
#####数据确权AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA