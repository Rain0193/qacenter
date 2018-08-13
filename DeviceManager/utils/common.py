# -*- coding: utf-8 -*-
import logging

from DeviceManager.utils.operation import add_device_data

logger = logging.getLogger('deviceManager')

def get_ajax_msg(msg, success):
    """
    ajax提示信息
    :param msg: str：msg
    :param success: str：
    :return:
    """
    return success if msg is 'ok' else msg


def device_info_logic(type=True, **kwargs):
    """
    设备信息逻辑处理
    :param type: boolean:True 默认新增设备
    :param kwargs: dict: 设备信息
    :return:
    """
    if kwargs.get('device_name') is '':
        return '设备名称不能为空'
    if kwargs.get('manufacturer') is '':
        return '厂商不能为空'
    if kwargs.get('model') is '':
        return '型号不能为空'
    if kwargs.get('memory_size') is '':
        return '内存大小不能为空'
    if kwargs.get('system_version') is '':
        return '系统版本不能为空'
    if kwargs.get('belonger') is '':
        return '归属人不能为空'

    return add_device_data(type, **kwargs)


def set_filter_session(request):
    """
    update session
    :param request:
    :return:
    """

    if 'device_name' in request.POST.keys():
        request.session['device_name'] = request.POST.get('device_name')
    if 'manufacturer' in request.POST.keys():
        request.session['manufacturer'] = request.POST.get('manufacturer')
    if 'belonger' in request.POST.keys():
        request.session['belonger'] = request.POST.get('belonger')

    filter_query = {
        'device_name': request.session['device_name'],
        'manufacturer': request.session['manufacturer'],
        'belonger': request.session['belonger']
    }

    return filter_query