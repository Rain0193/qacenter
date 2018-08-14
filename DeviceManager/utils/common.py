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


def device_info_logic(type=True, *account, **kwargs):
    """
    设备信息逻辑处理
    :param account: 操作人
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

    return add_device_data(type, account, **kwargs)


def set_filter_session(request):
    """
    update session
    :param request:
    :return:
    """
    # 出现数据工厂DataManager登录，DeviceManager没有进入index页面，重新初始化下面session
    request.session['device_name'] = ''
    request.session['device_number'] = ''
    request.session['manufacturer'] = '请选择厂商'
    request.session['belonger'] = '请选择归属人'

    if 'device_name' in request.POST.keys():
        request.session['device_name'] = request.POST.get('device_name')
    if 'device_number' in request.POST.keys():
        request.session['device_number'] = request.POST.get('device_number')
    if 'manufacturer' in request.POST.keys():
        request.session['manufacturer'] = request.POST.get('manufacturer')
    if 'belonger' in request.POST.keys():
        request.session['belonger'] = request.POST.get('belonger')

    filter_query = {
        'device_name': request.session['device_name'],
        'device_number': request.session['device_number'],
        'manufacturer': request.session['manufacturer'],
        'belonger': request.session['belonger']
    }

    return filter_query