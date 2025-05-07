from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings
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

# 数据确权dadadaadaadad

# 数据资产类型枚举
DATA_ASSET_TYPES = [
    ('铁路准入到货信息', '铁路准入到货信息'),
    ('预配舱单', '预配舱单'),
    ('理货报告编制要求', '理货报告编制要求'),
    # 可以添加更多数据类型
]

# 申请状态枚举
REQUEST_STATUS = [
    ('pending', '待审核'),
    ('approved', '已批准'),
    ('rejected', '已拒绝'),
]

# 操作类型枚举
OPERATION_TYPES = [
    ('request', '申请数据'),
    ('approve', '批准申请'),
    ('reject', '拒绝申请'),
    ('view', '查看数据'),
]

# 角色枚举
ROLE_TYPES = [
    ('customs', '海关'),
    ('port', '港口'),
    ('railway', '铁路'),
    ('foreign', '外方'),
]

class DataAsset1(models.Model):
    """数据资产模型，用于关联已有的数据资产"""
    name = models.CharField('资产名称', max_length=100)
    asset_type = models.CharField('资产类型', max_length=50, choices=DATA_ASSET_TYPES)
    owner = models.CharField('所有方', max_length=20, choices=ROLE_TYPES)
    description = models.TextField('描述', blank=True, null=True)
    file_path = models.CharField('文件路径', max_length=255)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_owner_display()})"

    class Meta:
        verbose_name = '数据资产'
        verbose_name_plural = '数据资产'

class DataRequest(models.Model):
    """数据请求模型，记录数据申请信息"""
    asset = models.ForeignKey(DataAsset1, on_delete=models.CASCADE, verbose_name='申请资产')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='data_requests', verbose_name='申请人')
    request_reason = models.TextField('申请原因')
    request_purpose = models.TextField('用途说明')
    status = models.CharField('申请状态', max_length=20, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField('申请时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    remark = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return f"{self.requester.username} 申请 {self.asset.name}"

    class Meta:
        verbose_name = '数据申请'
        verbose_name_plural = '数据申请'

class DataAuthorization(models.Model):
    """数据授权模型，记录授权信息"""
    request = models.OneToOneField(DataRequest, on_delete=models.CASCADE, verbose_name='关联申请')
    authorizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='授权人')
    authorized_at = models.DateTimeField('授权时间', default=timezone.now)
    is_active = models.BooleanField('是否有效', default=True)
    remark = models.TextField('授权备注', blank=True, null=True)

    def __str__(self):
        return f"{self.request.asset.name} 授权给 {self.request.requester.username}"

    class Meta:
        verbose_name = '数据授权'
        verbose_name_plural = '数据授权'

class OperationLog(models.Model):
    """操作日志模型，记录所有数据确权相关操作"""
    operation_type = models.CharField('操作类型', max_length=20, choices=OPERATION_TYPES)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='操作人')
    operation_time = models.DateTimeField('操作时间', auto_now_add=True)
    operation_detail = models.TextField('操作详情')
    related_request = models.ForeignKey(DataRequest, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联申请')

    def __str__(self):
        return f"{self.operator.username} {self.get_operation_type_display()} at {self.operation_time}"

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'

