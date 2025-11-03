from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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
        #下一行改了
        return f"{self.account} ({self.com})"

        # 添加调试属性
@property
def debug_info(self):
    return {
        'id': self.id,
        'account': self.account,
        'com': self.com,
        'comid': self.comid,
        'is_active': self.is_active,
        'is_staff': self.is_staff,
        'is_superuser': self.is_superuser,
        }


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
from django.db import models
from django.utils import timezone
import uuid

# 数据来源选择
DATA_SOURCE_CHOICES = [
    ('customs', '海关'),
    ('port', '港口'),
    ('railway', '铁路'),
    ('kazakhstan', '哈方'),
]




class DataRightApplication(models.Model):
    """数据权利申请模型"""
    # 略
    # 申请基本信息
    application_id = models.CharField(max_length=50, unique=True, verbose_name="申请编号")
    applicant = models.CharField(max_length=50, choices=DATA_SOURCE_CHOICES, verbose_name="申请方")
    target_data_holder = models.CharField(max_length=50, choices=DATA_SOURCE_CHOICES, verbose_name="目标数据持有方")

    # 目标数据信息
    target_data_name = models.CharField(max_length=255, verbose_name="目标数据名称")
    # 将project_name改回target_business_stage，但去掉choices限制，改为自由输入项目名称
    target_business_stage = models.CharField(max_length=255, verbose_name="项目名称")

    # 申请权利类型（多选）
    resource_holding_right = models.BooleanField(default=False, verbose_name="申请资源持有权")
    processing_use_right = models.BooleanField(default=False, verbose_name="申请加工使用权")
    reauthorization_right = models.BooleanField(default=False, verbose_name="申请转授权权")
    redistribution_right = models.BooleanField(default=False, verbose_name="申请再分发权")
    view_right = models.BooleanField(default=False, verbose_name="申请查看权")

    # 申请理由和用途
    application_reason = models.TextField(verbose_name="申请理由")
    intended_use = models.TextField(verbose_name="预期用途说明")

    # 申请时间相关
    intended_duration_start = models.DateField(verbose_name="预期使用开始时间")
    intended_duration_end = models.DateField(null=True, blank=True, verbose_name="预期使用结束时间")
    is_permanent = models.BooleanField(default=False, verbose_name="是否永久使用")

    # 联系信息
    contact_person = models.CharField(max_length=100, verbose_name="申请联系人")
    contact_phone = models.CharField(max_length=20, verbose_name="联系电话")
    contact_email = models.EmailField(verbose_name="联系邮箱")

    # 申请状态
    APPLICATION_STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已同意'),
        ('rejected', '已拒绝'),
        ('withdrawn', '已撤回'),
    ]
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending',
                              verbose_name="申请状态")

    # 审核信息
    reviewer = models.CharField(max_length=50, null=True, blank=True, verbose_name="审核人")
    review_time = models.DateTimeField(null=True, blank=True, verbose_name="审核时间")
    review_comments = models.TextField(null=True, blank=True, verbose_name="审核意见")

    # 记录时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'data_right_application'
        verbose_name = '数据权利申请'
        verbose_name_plural = '数据权利申请'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application_id} - {self.target_data_name}"

    def save(self, *args, **kwargs):
        # 自动生成申请编号
        if not self.application_id:
            from datetime import datetime
            import uuid
            date_str = datetime.now().strftime('%Y%m%d')
            random_str = str(uuid.uuid4())[:8].upper()
            self.application_id = f"DRA{date_str}{random_str}"
        super().save(*args, **kwargs)

    def get_applied_rights_display(self):
        """获取申请权利的显示文本"""
        rights = []
        if self.resource_holding_right:
            rights.append('资源持有权')
        if self.processing_use_right:
            rights.append('加工使用权')
        if self.reauthorization_right:
            rights.append('转授权权')
        if self.redistribution_right:
            rights.append('再分发权')
        if self.view_right:
            rights.append('查看权')
        return '、'.join(rights) if rights else '无'


class DataRightRecord(models.Model):
    """数据确权记录模型"""

    # 确权基本信息
    record_id = models.CharField(max_length=50, unique=True, verbose_name="确权记录编号")
    original_application = models.ForeignKey(DataRightApplication, on_delete=models.CASCADE, verbose_name="原始申请")

    # 数据信息
    data_name = models.CharField(max_length=255, verbose_name="数据名称")
    data_holder = models.CharField(max_length=50, choices=DATA_SOURCE_CHOICES, verbose_name="数据持有方")
    right_recipient = models.CharField(max_length=50, choices=DATA_SOURCE_CHOICES, verbose_name="权利获得方")
    # 将project_name改回business_stage，但去掉choices限制，改为自由输入项目名称
    business_stage = models.CharField(max_length=255, verbose_name="项目名称")

    # 已获得权利
    granted_resource_holding_right = models.BooleanField(default=False, verbose_name="已获得资源持有权")
    granted_processing_use_right = models.BooleanField(default=False, verbose_name="已获得加工使用权")
    granted_reauthorization_right = models.BooleanField(default=False, verbose_name="已获得转授权权")
    granted_redistribution_right = models.BooleanField(default=False, verbose_name="已获得再分发权")
    granted_view_right = models.BooleanField(default=False, verbose_name="已获得查看权")

    # 使用期限
    usage_start_date = models.DateField(verbose_name="使用开始时间")
    usage_end_date = models.DateField(null=True, blank=True, verbose_name="使用结束时间")
    is_permanent_usage = models.BooleanField(default=False, verbose_name="是否永久使用")

    # 确权状态
    RECORD_STATUS_CHOICES = [
        ('active', '生效中'),
        ('expired', '已过期'),
        ('revoked', '已撤销'),
        ('rejected', '已拒绝'),
    ]
    status = models.CharField(max_length=20, choices=RECORD_STATUS_CHOICES, default='active', verbose_name="确权状态")

    # 审核人信息
    approver = models.CharField(max_length=50, verbose_name="审核人")
    approval_time = models.DateTimeField(verbose_name="审核通过时间")
    approval_comments = models.TextField(verbose_name="审核意见")

    # 记录时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="确权时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'data_right_record'
        verbose_name = '数据确权记录'
        verbose_name_plural = '数据确权记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.record_id} - {self.data_name}"

    def save(self, *args, **kwargs):
        # 自动生成确权记录编号
        if not self.record_id:
            from datetime import datetime
            import uuid
            date_str = datetime.now().strftime('%Y%m%d')
            random_str = str(uuid.uuid4())[:8].upper()
            self.record_id = f"DCR{date_str}{random_str}"
        super().save(*args, **kwargs)

    def get_granted_rights_display(self):
        """获取已获得权利的显示文本"""
        rights = []
        if self.granted_resource_holding_right:
            rights.append('资源持有权')
        if self.granted_processing_use_right:
            rights.append('加工使用权')
        if self.granted_reauthorization_right:
            rights.append('转授权权')
        if self.granted_redistribution_right:
            rights.append('再分发权')
        if self.granted_view_right:
            rights.append('查看权')
        return '、'.join(rights) if rights else '无'

    def get_usage_period_display(self):
        """获取使用期限的显示文本"""
        if self.is_permanent_usage:
            return "永久使用"
        elif self.usage_end_date:
            return f"{self.usage_start_date} 至 {self.usage_end_date}"
        else:
            return f"自 {self.usage_start_date} 起"

    def is_expired(self):
        """判断是否已过期"""
        if self.is_permanent_usage:
            return False
        if self.usage_end_date:
            from datetime import date
            return date.today() > self.usage_end_date
        return False

class DataRightApplicationHistory(models.Model):
    """数据权利申请历史记录模型"""

    application = models.ForeignKey(DataRightApplication, on_delete=models.CASCADE, verbose_name="申请")
    action_type = models.CharField(max_length=50, verbose_name="操作类型")  # submit, review, approve, reject
    action_user = models.CharField(max_length=50, verbose_name="操作人")
    action_time = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")
    action_comments = models.TextField(null=True, blank=True, verbose_name="操作说明")

    class Meta:
        db_table = 'data_right_application_history'
        verbose_name = '申请历史记录'
        verbose_name_plural = '申请历史记录'
        ordering = ['-action_time']

    def __str__(self):
        return f"{self.application.application_id} - {self.action_type}"
##数据确权AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
###
# myapp/models.py
from django.db import models

class SandboxIPLog(models.Model):
    # 已有字段
    address   = models.CharField(max_length=255)
    ip        = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=False)  # 或根据实际情况设 auto_now_add=True

    # 新增这一行，映射你表里的 jieguo 列
    jieguo    = models.CharField(max_length=255)          # max_length 根据表结构调整

    class Meta:
        db_table = 'sandboxiplog'
        managed  = False   # 如果你不希望 Django 管理迁移，就保持 False
class AssetDimension(models.Model):
    DIMENSION_CHOICES = [
        ('security', '安全维度'),
        ('time', '时间维度'),
        ('space', '空间维度'),
        ('business', '业务维度'),
    ]

    SECURITY_SUB_CHOICES = [
        ('national_secret', '国家秘密'),
        ('confidential', '机密'),
        ('internal', '内部'),
        ('public', '公开'),
    ]

    TIME_SUB_CHOICES = [
        ('realtime', '实时级'),
        ('minutes', '*分钟'),
        ('hours', '*小时'),
        ('weeks', '*周'),
        ('months', '*月'),
        ('quarters', '*季度'),
        ('years', '*年'),
    ]

    SPACE_SUB_CHOICES = [
        ('all_railway', '全路'),
        ('railway_bureau', '路局内'),
        ('station', '站'),
        ('section', '段'),
        ('interval', '区间'),
    ]

    BUSINESS_SUB_CHOICES = [
        ('summary', '汇总'),
        ('detail', '不汇总'),
    ]

    asset = models.ForeignKey(DataAsset, on_delete=models.CASCADE, verbose_name="数据资产")
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE, verbose_name="授权用户")
    target_company = models.CharField(max_length=255, verbose_name="目标机构")
    field_name = models.CharField(max_length=100, verbose_name="字段名")
    time_dimension = models.CharField(max_length=20, choices=TIME_SUB_CHOICES, blank=True, null=True,
                                      verbose_name="时间子维度")
    space_dimension = models.CharField(max_length=20, choices=SPACE_SUB_CHOICES, blank=True, null=True,
                                       verbose_name="空间子维度")
    security_dimension = models.CharField(max_length=20, choices=SECURITY_SUB_CHOICES, blank=True, null=True,
                                          verbose_name="安全子维度")
    business_dimension = models.CharField(max_length=20, choices=BUSINESS_SUB_CHOICES, blank=True, null=True,
                                          verbose_name="业务子维度")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "数据资产维度表"
        verbose_name_plural = "数据资产维度表"
        unique_together = ['asset', 'user', 'field_name', 'target_company']


# 维度明细表
class AssetDimensionDetail(models.Model):
    SUB_DIMENSION_CHOICES = [
        ('time', '时间维度'),
        ('space', '空间维度'),
    ]

    asset = models.ForeignKey(DataAsset, on_delete=models.CASCADE, verbose_name="数据资产")
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE, verbose_name="授权用户")
    target_company = models.CharField(max_length=255, verbose_name="目标机构")
    field_name = models.CharField(max_length=100, verbose_name="字段名")
    sub_dimension = models.CharField(max_length=20, choices=SUB_DIMENSION_CHOICES, verbose_name="子维度类型")
    sub_dimension_detail = models.CharField(max_length=200, verbose_name="子维度明细")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "数据资产维度明细表"
        verbose_name_plural = "数据资产维度明细表"