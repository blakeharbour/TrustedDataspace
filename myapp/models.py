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
        user = self.model(account=account,**extra_fields)
        user.set_password(password)  # 加密密码
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
