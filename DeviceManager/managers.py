from django.db import models

'''设备信息表操作'''

class DeviceInfoManager(models.Manager):
    def insert_device(self, **kwargs):
        self.create(**kwargs)

    def update_device(self, id, **kwargs):  # 如此update_time才会自动更新！！
        obj = self.get(id=id)
        obj.device_name = kwargs.get('device_name')
        obj.manufacturer = kwargs.get('manufacturer')
        obj.model = kwargs.get('model')
        obj.memory_size = kwargs.get('memory_size')
        obj.system_version = kwargs.get('system_version')
        obj.belonger = kwargs.get('belonger')
        obj.simple_desc = kwargs.get('simple_desc')
        obj.save()

    def clear_lender(self, id):
        obj = self.get(id=id)
        obj.lender = ''
        obj.save()

    def get_dev_name(self, dev_name, type=True, id=None):
        if type:
            return self.filter(device_name__exact=dev_name).count()
        else:
            if id is not None:
                return self.values('device_name').filter(id__in=id)
            return self.get(device_name__exact=dev_name)