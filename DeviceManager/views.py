
import json
import logging
import platform

from django.http import HttpResponseRedirect,HttpResponse
from DeviceManager.models import DeviceInfo, OperateRecord
from DataManager.models import UserInfo
from DeviceManager.utils.common import get_ajax_msg, device_info_logic, set_filter_session
from DeviceManager.utils.pagination import get_pager_info
from DeviceManager.utils.operation import del_device_data, del_device_lender, update_device_lender
from django.shortcuts import render_to_response

logger = logging.getLogger('DeviceMananger')

# Create your views here.
separator = '\\' if platform.system() == 'Windows' else '/'

def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return HttpResponseRedirect('/qacenter/data/login/')
        return func(request, *args, **kwargs)

    return wrapper

@login_check
def device_list(request, id):
    """
    设备列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    account = request.session["now_account"]
    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        if 'mode' in project_info.keys():
            if project_info.get('mode') == 'del':
                id = project_info.get('id')
                id_list = [int(x) for x in id.split(',')]
                msg = del_device_data(id_list, account)
            elif project_info.get('mode') == 'clear':
                id = project_info.get('id')
                msg = del_device_lender(id, account)
            elif project_info.get('mode') == 'lend':
                id = project_info.get('id')
                lender = project_info.get('lender')
                msg = update_device_lender(id, lender, account)
        # else:
        #     id = project_info.get('id')
        #     lender = project_info.get('lender')
        #     msg = update_device_lender(id, lender)
        return HttpResponse(get_ajax_msg(msg, 'ok'))
    else:
        filter_query = set_filter_session(request)
        dev_list = get_pager_info(
            DeviceInfo, filter_query, '/device/dc/device_list/', id)
        belonger = UserInfo.objects.filter(type=1)
        manage_info = {
            'account': account,
            'belonger': belonger,
            'role': request.session["role"],
            'device': dev_list[1],
            'page_list': dev_list[0],
            'sum': dev_list[2],
            'info': filter_query
        }
        return render_to_response('device/device_list.html', manage_info)


@login_check
def add_device(request):
    """
    新增设备
    :param request:
    :return:
    """
    account = request.session["now_account"]
    if request.is_ajax():
        device_info = json.loads(request.body.decode('utf-8'))
        msg = device_info_logic(True, account, **device_info)
        return HttpResponse(get_ajax_msg(msg, '/device/dc/device_list/1/'))
    elif request.method == 'GET':
        belonger = UserInfo.objects.filter(type=1)
        manage_info = {
            'account': account,
            'role': request.session["role"],
            'belonger': belonger
        }
        return render_to_response('device/add_device.html', manage_info)


@login_check
def edit_device(request, id):
    """
    编辑设备
    :param request:
    :param id: 设备id
    :return:
    """
    account = request.session["now_account"]
    if request.is_ajax():
        device_info = json.loads(request.body.decode('utf-8'))
        msg = device_info_logic(False, account, **device_info)
        return HttpResponse(get_ajax_msg(msg, '成功'))
    elif request.method == 'GET':
        deviceInfo = DeviceInfo.objects.get(id=id)
        belonger = UserInfo.objects.filter(type=1)
        manage_info = {
            'account': account,
            'role': request.session["role"],
            'deviceInfo': deviceInfo,
            'belonger': belonger
        }
        return render_to_response('device/edit_device.html', manage_info)


@login_check
def operate_record(request, id):
    """
    操作记录列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    account = request.session["now_account"]
    if request.is_ajax():
        return HttpResponse('ok')
    else:
        filter_query = set_filter_session(request)
        dev_list = get_pager_info(
            OperateRecord, filter_query, '/device/dc/operate_record/', id)
        manage_info = {
            'account': account,
            'role': request.session["role"],
            'device': dev_list[1],
            'page_list': dev_list[0],
            'sum': dev_list[2],
            'info': filter_query
        }
        return render_to_response('device/operate_record.html', manage_info)