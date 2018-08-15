# -*- coding: utf-8 -*-
import logging

from DeviceManager.models import DeviceInfo, OperateRecord
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('deviceManager')


def add_device_data(type, account, **kwargs):
    """
    设备信息落地
    :param type: true: 新增， false: 更新
    :param kwargs: dict
    :return: ok or tips
    """
    device_opt = DeviceInfo.objects
    operate_record_opt = OperateRecord.objects
    device_number = kwargs.get('device_number')
    device_name = kwargs.get('device_name')
    operater = account[0]
    if type:
        if device_opt.get_dev_name(device_number) < 1:
            try:
                device_opt.insert_device(**kwargs)
            except DataError:
                return '设备信息过长'
            except Exception:
                logger.error('设备添加异常：{kwargs}'.format(kwargs=kwargs))
                return '添加失败，请重试'
            logger.info('设备添加成功：{kwargs}'.format(kwargs=kwargs))
            operate_record = '[{"操作":' + '"设备添加成功"},'+ '{kwargs}'.format(kwargs=kwargs) + ']'
            operate_record_opt.insert_record(operater=operater, device_number=device_number, operate_record=operate_record, device_name=device_name)
        else:
            return '该设备编号已存在，请重新命名'
    else:
        id = kwargs.pop('id')
        device_info = device_opt.get_device_by_id(id)
        try:
            if operater == device_info.belonger:
                device_opt.update_device(id, **kwargs)
            else:
                return '更新失败，只允许设备归属人操作'
        except DataError:
            return '设备信息过长'
        except Exception:
            logger.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return '更新失败，请重试'
        logger.info('设备更新成功：{kwargs}'.format(kwargs=kwargs))
        operate_record = '[{"操作":' + '"设备更新成功"},{'
        if device_info.device_name != kwargs.get('device_name'):
            operate_record = operate_record + '"设备名称":' + '"'+ device_info.device_name + ' 修改成: ' + kwargs.get('device_name') + '"'
        if device_info.manufacturer != kwargs.get('manufacturer'):
            operate_record = operate_record + ',"品牌":' + '"'+ device_info.manufacturer + ' 修改成: ' + kwargs.get('manufacturer') + '"'
        if device_info.model != kwargs.get('model'):
            operate_record = operate_record + ',"型号":' + '"'+ device_info.model + ' 修改成: ' + kwargs.get('model') + '"'
        if device_info.memory_size != kwargs.get('memory_size'):
            operate_record = operate_record + ',"内存大小":' + '"'+ device_info.memory_size + ' 修改成: ' + kwargs.get('memory_size') + '"'
        if device_info.system_version != kwargs.get('system_version'):
            operate_record = operate_record + ',"系统版本":' + '"'+ device_info.system_version + ' 修改成: ' + kwargs.get('system_version') + '"'
        if device_info.belonger != kwargs.get('belonger'):
            operate_record = operate_record + ',"归属人":' + '"'+ device_info.belonger + ' 修改成: ' + kwargs.get('belonger') + '"'
        if device_info.simple_desc != kwargs.get('simple_desc'):
            operate_record = operate_record + ',"其他附件":' + '"'+ device_info.simple_desc + ' 修改成: ' + kwargs.get('simple_desc') + '"'
        operate_record = operate_record + '}]'
        operate_record_opt.insert_record(operater=operater, device_number=device_number, operate_record=operate_record,device_name=device_name)
    return 'ok'


def del_device_data(id, account):
    """
    根据设备索引删除设备数据
    :param id: str or int: 设备索引
    :return: ok or tips
    """
    device_opt = DeviceInfo.objects
    operate_record_opt = OperateRecord.objects
    operater = account
    try:
        belong_device = device_opt.get_device_by_ids(id)[0]
        device_number = belong_device.device_number
        device_name =  belong_device.device_name
        operate_record = '[{"操作":' + '"设备删除成功"},'
        operate_record = operate_record + '{"设备名称":' + '"' + device_name + '"'
        operate_record = operate_record + ',"设备编号":' + '"' + device_number + '"'
        operate_record = operate_record + '}]'
        operate_record_opt.insert_record(operater=operater, device_number=device_number, operate_record=operate_record,device_name=device_name)

        if operater == belong_device.belonger:
            device_opt.filter(id__in=id).delete()
        else:
            return '删除失败，只允许设备归属人操作'
    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('{id} 设备已删除'.format(id=id))
    return 'ok'

def del_device_lender(id, account):
    """
    根据设备索引清空设备出借人
    :param id: str or int: 设备索引
    :return: ok or tips
    """
    device_opt = DeviceInfo.objects
    operate_record_opt = OperateRecord.objects
    operater = account
    try:
        belong_device = device_opt.get_device_by_id(id)
        if operater == belong_device.belonger:
            device_opt.clear_lender(id)
        else:
            return '归还失败，只允许设备归属人操作'

    except ObjectDoesNotExist:
        return '清空出借人异常，请重试'
    logger.info('{id} 设备出借人已清空'.format(id=id))

    device_number = belong_device.device_number
    device_name = belong_device.device_name
    lender = belong_device.lender
    operate_record = '[{"操作":' + '"设备归还成功"},'
    operate_record = operate_record + '{"设备名称":' + '"' + device_name + '"'
    operate_record = operate_record + ',"设备编号":' + '"' + device_number + '"'
    operate_record = operate_record + ',"归还人":' + '"' + lender + '"'
    operate_record = operate_record + '}]'
    operate_record_opt.insert_record(operater=operater, device_number=device_number, operate_record=operate_record,device_name=device_name)
    return '归还成功'

def update_device_lender(id, lender, account):
    """
    根据设备索引更新设备出借人
    :param id: str or int: 设备索引
    :return: ok or tips
    """
    device_opt = DeviceInfo.objects
    operate_record_opt = OperateRecord.objects
    operater = account
    try:
        belong_device = device_opt.get_device_by_id(id)
        device_lender = belong_device.lender
        if device_lender != '':
            return '该设备已借出，请先操作归还，再出借'
        if operater == belong_device.belonger:
            device_opt.update_lender(id, lender)
        else:
            return '借出失败，只允许设备归属人操作'

    except ObjectDoesNotExist:
        return '更新设备出借人异常，请重试'
    logger.info('{id} 设备出借成功'.format(id=id))
    belong_device = device_opt.get_device_by_id(id)
    device_number = belong_device.device_number
    device_name = belong_device.device_name
    lender = belong_device.lender
    operate_record = '[{"操作":' + '"设备借出成功"},'
    operate_record = operate_record + '{"设备名称":' + '"' + device_name + '"'
    operate_record = operate_record + ',"设备编号":' + '"' + device_number + '"'
    operate_record = operate_record + ',"出借人":' + '"' + lender + '"'
    operate_record = operate_record + '}]'
    operate_record_opt.insert_record(operater=operater, device_number=device_number, operate_record=operate_record,device_name=device_name)
    return '借出成功'