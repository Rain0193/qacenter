# -*- coding: utf-8 -*-
import json
import logging
import platform

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from DataManager.models import UserInfo, ProjectInfo, ModuleInfo
from DataManager.utils.common import register_info_logic, get_ajax_msg, init_filter_session, project_info_logic, set_filter_session, module_info_logic
from DataManager.utils.operation import del_project_data, del_module_data
from DataManager.utils.pagination import get_pager_info

logger = logging.getLogger('qacenter')

# Create your views here.
separator = '\\' if platform.system() == 'Windows' else '/'

def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        if UserInfo.objects.filter(account_number__exact=account).filter(password__exact=password).count() == 1:
            logger.info('{account_number} 登录成功'.format(account_number=account))
            request.session["login_status"] = True
            request.session["now_account"] = account
            return HttpResponseRedirect('/qacenter/index/')
        else:
            logger.info('{account_number} 登录失败, 请检查用户名或者密码'.format(account_number=account))
            request.session["login_status"] = False
            return render_to_response("login.html")
    elif request.method == 'GET':
        return render_to_response("login.html")


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.is_ajax():
        user_info = json.loads(request.body.encode('utf-8'))
        msg = register_info_logic(**user_info)
        return HttpResponse(get_ajax_msg(msg, '恭喜您，账号已成功注册'))
    elif request.method == 'GET':
        return render_to_response("register.html")


def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.session.get('login_status'):
        # applicationList = get_pager_info(
        #     Application, None, '/qacenter/index')
        manage_info = {'account': request.session["now_account"],
                       # 'applicationList' : applicationList
                       }
        init_filter_session(request)
        return render_to_response('index.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def project_list(request, id):
    """
    项目列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.load(request.body.encode('utf-8'))
            if 'mode' == project_info.keys():
                msg = del_project_data(project_info.pop('id'))
            else:
                msg = project_info_logic(type=False, **project_info)
            return HttpResponse(get_ajax_msg(msg, 'ok'))
        else:
            filter_query = set_filter_session(request)
            pro_list = get_pager_info(
                ProjectInfo, filter_query, '/qacenter/project_list/', id)
            manage_info = {
                'account': account,
                'project': pro_list[1],
                'page_list': pro_list[0],
                'info': filter_query,
                'sum': pro_list[2],
            }
            return render_to_response('project_list.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def add_project(request):
    """
    新增项目
    :param request:
    :return:
    """
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            msg = project_info_logic(**project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/project_list/1/'))

        elif request.method == 'GET':
            manage_info = {
                'account': account
            }
            return render_to_response('add_project.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def module_list(request, id):
    """
    模块列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            module_info = json.loads(request.body.decode('utf-8'))
            if 'mode' in module_info.keys():  # del module
                msg = del_module_data(module_info.pop('id'))
            else:
                msg = module_info_logic(type=False, **module_info)
            return HttpResponse(get_ajax_msg(msg, 'ok'))
        else:
            filter_query = set_filter_session(request)
            module_list = get_pager_info(
                ModuleInfo, filter_query, '/qacenter/module_list/', id)
            manage_info = {
                'account': account,
                'module': module_list[1],
                'page_list': module_list[0],
                'info': filter_query,
                'sum': module_list[2],
                'project': module_list[3]
            }
            return render_to_response('module_list.html', manage_info)
    else:
        return HttpResponseRedirect("/api/login/")

def add_module(request):
    '''
    新增模块
    :return:
    '''
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            module_info = json.loads(request.body.decode('utf-8'))
            msg = module_info_logic(**module_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/module_list/1'))
        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'data': ProjectInfo.objects.all().values('project_name')
            }
            return render_to_response('add_module.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")