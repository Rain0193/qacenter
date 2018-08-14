from django.db import models

'''设备信息表操作'''
class DeviceInfoManager(models.Manager):
    def insert_device(self, **kwargs):
        self.create(**kwargs)

    def update_device(self, id, **kwargs):  # 如此update_time才会自动更新！！
        obj = self.get(id=id)
        obj.device_name = kwargs.get('device_name')
        obj.device_number = kwargs.get('device_number')
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

    def update_lender(self, id, lender):
        obj = self.get(id=id)
        obj.lender = lender
        obj.save()

    def get_dev_name(self, device_number, type=True, id=None):
        if type:
            return self.filter(device_number__exact=device_number).count()
        else:
            if id is not None:
                return self.values('device_name').filter(id__in=id)
            return self.get(device_name__exact=device_number)

    def get_device_by_number(self, device_number):
        return self.get(device_number=device_number)

    def get_device_by_id(self, id):
        return self.get(id=id)

    def get_device_by_ids(self, id):
        return self.filter(id__in=id)


'''设备操作记录表'''
class OperateRecordManager(models.Manager):
    def insert_record(self, operater, device_number, operate_record, device_name):
        self.create(operater=operater, device_number=device_number, operate_record=operate_record, device_name=device_name)