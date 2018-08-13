
import json
import logging
import platform

from django.http import HttpResponseRedirect,HttpResponse
from DeviceManager.models import DeviceInfo
from DataManager.models import UserInfo
from DeviceManager.utils.common import get_ajax_msg, device_info_logic, set_filter_session
from DeviceManager.utils.pagination import get_pager_info
from DeviceManager.utils.operation import del_device_data
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
        id = project_info.get('id')
        id_list = [int(x) for x in id.split(',')]
        if 'mode' in project_info.keys():
            msg = del_device_data(id_list)
        # else:
        #     msg = project_info_logic(type=False, **project_info)
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
        msg = device_info_logic(**device_info)
        return HttpResponse(get_ajax_msg(msg, '/device/dc/device_list/1/'))
    elif request.method == 'GET':
        belonger = UserInfo.objects.filter(type=1)
        manage_info = {
            'account': account,
            'role': request.session["role"],
            'belonger': belonger
        }
        return render_to_response('device/add_device.html', manage_info)

