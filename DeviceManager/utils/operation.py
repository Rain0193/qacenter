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
    device_name = kwargs.get('device_name')
    if type:
        if device_opt.get_dev_name(device_name) < 1:
            try:
                device_opt.insert_device(**kwargs)
            except DataError:
                return '设备信息过长'
            except Exception:
                logger.error('设备添加异常：{kwargs}'.format(kwargs=kwargs))
                return '添加失败，请重试'
            logger.info('设备添加成功：{kwargs}'.format(kwargs=kwargs))
        else:
            return '该设备已存在，请重新命名'
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