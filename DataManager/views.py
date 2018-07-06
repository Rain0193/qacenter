# -*- coding: utf-8 -*-
import json
import logging
import platform

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from urllib3.connectionpool import xrange

from DataManager.models import UserInfo, ProjectInfo, ModuleInfo, TdInfo
from DataManager.utils.common import register_info_logic, get_ajax_msg, init_filter_session, project_info_logic, set_filter_session, module_info_logic, td_info_logic
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
            return HttpResponseRedirect('/qacenter/all_td/')
        else:
            logger.info('{account_number} 登录失败, 请检查用户名或者密码'.format(account_number=account))
            request.session["login_status"] = False
            return render_to_response("login.html")
    elif request.method == 'GET':
        return render_to_response("login.html")

def logout(request):
    """
    注销登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        logger.info('{username}退出'.format(username=request.session['now_account']))
        try:
            del request.session['now_account']
            del request.session['login_status']
            init_filter_session(request, type=False)
        except KeyError:
            logger.error('session invalid')
        return HttpResponseRedirect("/qacenter/login")


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.is_ajax():
        user_info = json.loads(request.body.decode('utf-8'))
        msg = register_info_logic(**user_info)
        return HttpResponse(get_ajax_msg(msg, '恭喜您，账号已成功注册'))
    elif request.method == 'GET':
        return render_to_response("register.html")

def base(request):
    """
    导航
    :param request:
    :return:
    """
    projectInfo = ProjectInfo.objects.all()
    print(projectInfo)
    if request.session.get('login_status'):
        manage_info = {
            'account': request.session["now_account"],
            'projects': projectInfo
        }
        init_filter_session(request)
        return render_to_response('base.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def all_td(request):
    """
    首页
    :param request:
    :return:
    """
    projectInfo = ProjectInfo.objects.all()
    print(projectInfo)
    tdinfo = TdInfo.objects.all()
    tdlist = []
    for k in xrange(len(tdinfo)):
        td= {}
        if k % 2 == 0:
            td.setdefault('right','true')
        else:
            td.setdefault('right','false')
        td.setdefault('id',tdinfo[k].id)
        td.setdefault('title', tdinfo[k].title)
        td.setdefault('td_url', tdinfo[k].td_url)
        td.setdefault('author', tdinfo[k].author)
        td.setdefault('params', eval(tdinfo[k].params))
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        tdlist.append(td)
    if request.session.get('login_status'):
        manage_info = {
            'account': request.session["now_account"],
            'tdList': tdlist,
            'projects': projectInfo
        }
        init_filter_session(request)
        return render_to_response('all_td.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def project_list(request, id):
    """
    项目列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    projectInfo = ProjectInfo.objects.all()
    print(projectInfo)
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            if 'mode' in project_info.keys():
                msg = del_project_data(list(eval(project_info.pop('id'))))
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
                'projects': projectInfo
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
    projectInfo = ProjectInfo.objects.all()
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            msg = project_info_logic(**project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/project_list/1/'))

        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'projects': projectInfo
            }
            return render_to_response('add_project.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def edit_project(request, id):
    """
    编辑项目
    :param request:
    :return:
    """
    projectsInfo = ProjectInfo.objects.all()
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            msg = project_info_logic(False, **project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/edit_project/' + id + '/'))
            # return HttpResponse(get_ajax_msg(msg, '/qacenter/project_list/1/'))

        elif request.method == 'GET':
            projectInfo = ProjectInfo.objects.get(id=id)
            manage_info = {
                'account': account,
                'id': projectInfo.id,
                'project_name': projectInfo.project_name,
                'responsible_name': projectInfo.responsible_name,
                'test_user': projectInfo.test_user,
                'simple_desc': projectInfo.simple_desc,
                'projects': projectsInfo
            }
            return render_to_response('edit_project.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def module_list(request, id):
    """
    模块列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    projectInfo = ProjectInfo.objects.all()
    projectInfoList = []
    pro1 = {'project_name': 'All'}
    projectInfoList.append(pro1)
    for k in xrange(len(projectInfo)):
        pro2 = {}
        pro2.setdefault('project_name', projectInfo[k].project_name)
        projectInfoList.append(pro2)
    print(projectInfoList)

    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            module_info = json.loads(request.body.decode('utf-8'))
            if 'mode' in module_info.keys():  # del module
                msg = del_module_data(list(eval(module_info.pop('id'))))
            else:
                msg = module_info_logic(type=False, **module_info)
            return HttpResponse(get_ajax_msg(msg, 'ok'))
        else:
            projectName = request.POST.get('belong_project')
            if projectName == 'All' or projectName is None:
                projectName = ''
            print(projectName)
            filter_query = {
                'belong_project': projectName,
            }
            module_list = get_pager_info(
                ModuleInfo, filter_query, '/qacenter/module_list/', id)
            manage_info = {
                'account': account,
                'module': module_list[1],
                'page_list': module_list[0],
                'project': projectInfoList,
                'projects': projectInfo
            }
            return render_to_response('module_list.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def add_module(request):
    '''
    新增模块
    :return:
    '''
    projectInfo = ProjectInfo.objects.all()
    print(projectInfo)
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            module_info = json.loads(request.body.decode('utf-8'))
            msg = module_info_logic(**module_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/module_list/1'))
        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'data': ProjectInfo.objects.all().values('project_name'),
                'projects': projectInfo
            }
            return render_to_response('add_module.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def edit_project(request, id):
    """
    编辑项目
    :param request:
    :return:
    """
    projectsInfo = ProjectInfo.objects.all()
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            msg = project_info_logic(False, **project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/edit_project/' + id + '/'))
            # return HttpResponse(get_ajax_msg(msg, '/qacenter/project_list/1/'))

        elif request.method == 'GET':
            projectInfo = ProjectInfo.objects.get(id=id)
            manage_info = {
                'account': account,
                'id': projectInfo.id,
                'project_name': projectInfo.project_name,
                'responsible_name': projectInfo.responsible_name,
                'test_user': projectInfo.test_user,
                'simple_desc': projectInfo.simple_desc,
                'projects': projectsInfo
            }
            return render_to_response('edit_project.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def edit_module(request, id):
    """
    编辑模块
    :param request:
    :return:
    """
    projectsInfo = ProjectInfo.objects.all()
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            module_info = json.loads(request.body.decode('utf-8'))
            msg = module_info_logic(False, **module_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/edit_module/' + id + '/'))

        elif request.method == 'GET':
            moduleInfo = ModuleInfo.objects.get(id=id)
            manage_info = {
                'account': account,
                'id': moduleInfo.id,
                'module_name': moduleInfo.module_name,
                'belong_project': moduleInfo.belong_project,
                'test_user': moduleInfo.test_user,
                'simple_desc': moduleInfo.simple_desc,
                'dev_user': moduleInfo.dev_user,
                'projects': projectsInfo
            }
            return render_to_response('edit_module.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def add_td(request):
    '''
    添加事务模板
    :param request:
    :return:
    '''
    projectInfo = ProjectInfo.objects.all()
    print(projectInfo)
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            td_info = json.loads(request.body.decode('utf-8'))
            msg = td_info_logic(**td_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/add_td/'))
        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'project': ProjectInfo.objects.all().values('project_name').order_by('-create_time'),
                'projects': projectInfo
            }
            return render_to_response('add_td.html', manage_info)
    else:
         return HttpResponseRedirect("/qacenter/login/")


def get_module_by_project(request):
    '''
    根据项目获取模块
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    info = json.loads(request.body.decode('utf-8'))
    belong_project = info.get('belong_project')
    if request.method == 'GET':
        manage_info = {
            'account': account,
            'module': ModuleInfo.objects.filter(belong_project=belong_project)
        }
        return render_to_response('add_td.html', manage_info)