from django.db import models

from DeviceManager.managers import DeviceInfoManager
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


class DeviceInfo(BaseTable):
    class Meta:
        verbose_name = '设备信息'
        db_table = 'Device_DeviceInfo'

    device_name = models.CharField('设备名称',max_length=20)
    manufacturer = models.CharField('厂商',max_length=20)
    model = models.CharField('型号',max_length=20)
    memory_size = models.CharField('内存大小',max_length=20)
    system_version = models.CharField('系统版本', max_length=20)
    belonger = models.CharField('归属人', max_length=20)
    lender = models.CharField('出借人', max_length=20)
    simple_desc = models.CharField('其他附件', max_length=100)
    objects = DeviceInfoManager()
