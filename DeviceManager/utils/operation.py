# -*- coding: utf-8 -*-
import logging

from DeviceManager.models import DeviceInfo
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('deviceManager')


def add_device_data(type, **kwargs):
    """
    设备信息落地
    :param type: true: 新增， false: 更新
    :param kwargs: dict
    :return: ok or tips
    """
    device_opt = DeviceInfo.objects
    device_number = kwargs.get('device_number')
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
        else:
            return '该设备编号已存在，请重新命名'
    else:
        try:
            device_opt.update_device(kwargs.pop('id'), **kwargs)
        except DataError:
            return '设备信息过长'
        except Exception:
            logger.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return '更新失败，请重试'
        logger.info('设备更新成功：{kwargs}'.format(kwargs=kwargs))
    return 'ok'


def del_device_data(id):
    """
    根据设备索引删除设备数据
    :param id: str or int: 设备索引
    :return: ok or tips
    """
    try:

        DeviceInfo.objects.filter(id__in=id).delete()

    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('{id} 设备已删除'.format(id=id))
    return 'ok'

def del_device_lender(id):
    """
    根据设备索引清空设备出借人
    :param id: str or int: 设备索引
    :return: ok or tips
    """
    try:

        DeviceInfo.objects.clear_lender(id)

    except ObjectDoesNotExist:
        return '清空出借人异常，请重试'
    logger.info('{id} 设备出借人已清空'.format(id=id))
    return '归还成功'

def update_device_lender(id, lender):
    """
    根据设备索引更新设备出借人
    :param id: str or int: 设备索引
    :return: ok or tips
    """
    try:
        device_lender = DeviceInfo.objects.values('lender').filter(id=id)
        if device_lender[0].get('lender') != '':
            return '该设备已借出，请先操作归还，再出借'
        DeviceInfo.objects.update_lender(id, lender)

    except ObjectDoesNotExist:
        return '更新设备出借人异常，请重试'
    logger.info('{id} 设备出借成功'.format(id=id))
    return '借出成功'