from django.db import models

from DataManager.managers import UserInfoManager, ProjectInfoManager, ModuleInfoManager, TdInfoManager
from django.db.models.fields.related import ManyToManyField
# Create your models here.

class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        abstract = True
        verbose_name = '公共字段表'
        db_table = 'BaseTable'


class UserInfo(BaseTable):
    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'

    username = models.CharField('姓名',max_length=10)
    type = models.IntegerField('角色',default=1)
    account_number = models.CharField('账号',max_length=20)
    email = models.EmailField('邮箱')
    password = models.CharField('密码', max_length=20)
    status = models.IntegerField('有效/无效',default=1)
    objects = UserInfoManager()


class ProjectInfo(BaseTable):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'ProjectInfo'

    project_name = models.CharField('项目名称', max_length=50)
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

class TdInfo(BaseTable):
    class Meta:
        verbose_name = '事务信息'
        db_table = 'TdInfo'

    title = models.CharField('事务名称', max_length=50)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    belong_module = models.ForeignKey(ModuleInfo, on_delete=models.CASCADE)
    td_url = models.CharField('事务地址', max_length=200)
    author = models.CharField('编写人员', max_length=20)
    run_count = models.IntegerField('调用次数', default=0)
    params = models.TextField('入参列表')
    instruction = models.TextField('帮助说明')
    objects = TdInfoManager()
