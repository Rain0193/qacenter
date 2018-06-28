from django.db import models

from DataManager.managers import UserInfoManager, ProjectInfoManager, ModuleInfoManager
# Create your models here.

class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        abstract = True
        verbose_name = '公共字段表'
        db_table = 'BaseTable'


class UserInfo(BaseTable):
    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'

    username = models.CharField('姓名',max_length=10)
    account_number = models.CharField('账号',max_length=20)
    email = models.EmailField('邮箱')
    password = models.CharField('密码', max_length=20)
    status = models.IntegerField('有效/无效',default=1)
    objects = UserInfoManager()


class ProjectInfo(BaseTable):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'ProjectInfo'

    project_name = models.CharField('项目名称',max_length=50)
    responsible_name = models.CharField('项目负责人', max_length=20)
    test_user = models.CharField('测试人员', max_length=100)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    objects = ProjectInfoManager()


class ModuleInfo(BaseTable):
    class Meta:
        verbose_name = '模块信息'
        db_table = 'ModuleInfo'

    module_name = models.CharField('模块名称', max_length=50)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    test_user = models.CharField('测试人员', max_length=50)
    dev_user = models.CharField('开发人员', max_length=50)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    objects = ModuleInfoManager()
