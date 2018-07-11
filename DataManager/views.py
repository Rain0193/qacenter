# -*- coding: utf-8 -*-
import json
import logging
import platform

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from urllib3.connectionpool import xrange

from DataManager.models import UserInfo, ProjectInfo, ModuleInfo, TdInfo, FavTd, Record
from DataManager.utils.common import register_info_logic, get_ajax_msg, init_filter_session, project_info_logic, set_filter_session, module_info_logic, td_info_logic, record_info_logic
from DataManager.utils.operation import del_project_data, del_module_data, add_fav_data, add_td_pv, projectAndModule
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
    projectlist = projectAndModule
    if request.session.get('login_status'):
        manage_info = {
            'account': request.session["now_account"],
            'projects': projectlist
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
    account = request.session["now_account"]
    projectlist = projectAndModule
    fav_opt = FavTd.objects
    tdinfo = TdInfo.objects.all()
    kwargs = {}
    tdlist = []
    for k in xrange(len(tdinfo)):
        td = {}
        flag = fav_opt.get_fav_by_tdAndUser(account, tdinfo[k].id)
        if flag == 1:
            td.setdefault('isFav', 'true')
        else:
            td.setdefault('isFav', 'false')
        if k % 2 == 0:
            td.setdefault('right', 'true')
        else:
            td.setdefault('right', 'false')
        td.setdefault('id', tdinfo[k].id)
        td.setdefault('title', tdinfo[k].title)
        td.setdefault('td_url', tdinfo[k].td_url)
        td.setdefault('author', tdinfo[k].author)
        td.setdefault('params', eval(tdinfo[k].params))
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        tdlist.append(td)
    if request.session.get('login_status'):
        if request.is_ajax():
            td_info = json.loads(request.body.decode('utf-8'))
            kwargs['user'] = request.session["now_account"]
            kwargs['id'] = td_info.pop('id')
            if td_info.get('model') == 'pv':
                msg = add_td_pv(kwargs['id'])
            else:
                if td_info.pop('type'):
                    msg = add_fav_data(True, **kwargs)
                else:
                    msg = add_fav_data(False, **kwargs)
            return HttpResponse(get_ajax_msg(msg, 'ok'))
        else:
            manage_info = {
                'account': request.session["now_account"],
                'tdList': tdlist,
                'projects': projectlist
            }
            init_filter_session(request)
            return render_to_response('all_td.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def project_td(request, id):
    '''
    项目的事务
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    presentProject = ProjectInfo.objects.values('project_name').filter(id=id)
    projectlist = projectAndModule
    fav_opt = FavTd.objects
    tdinfo = TdInfo.objects.filter(belong_project__id=id)
    kwargs = {}
    tdlist = []
    for k in xrange(len(tdinfo)):
        td = {}
        flag = fav_opt.get_fav_by_tdAndUser(account, tdinfo[k].id)
        if flag == 1:
            td.setdefault('isFav', 'true')
        else:
            td.setdefault('isFav', 'false')
        if k % 2 == 0:
            td.setdefault('right', 'true')
        else:
            td.setdefault('right', 'false')
        td.setdefault('id', tdinfo[k].id)
        td.setdefault('title', tdinfo[k].title)
        td.setdefault('td_url', tdinfo[k].td_url)
        td.setdefault('author', tdinfo[k].author)
        td.setdefault('params', eval(tdinfo[k].params))
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        tdlist.append(td)
    if request.session.get('login_status'):
        if request.is_ajax():
            td_info = json.loads(request.body.decode('utf-8'))
            kwargs['user'] = request.session["now_account"]
            kwargs['id'] = td_info.pop('id')
            if td_info.get('model') == 'pv':
                msg = add_td_pv(kwargs['id'])
            else:
                if td_info.pop('type'):
                    msg = add_fav_data(True, **kwargs)
                else:
                    msg = add_fav_data(False, **kwargs)
            return HttpResponse(get_ajax_msg(msg, 'ok'))
        else:
            manage_info = {
                'account': request.session["now_account"],
                'presentProject': presentProject[0]['project_name'],
                'tdList': tdlist,
                'projects': projectlist
            }
            init_filter_session(request)
            return render_to_response('project_td.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def module_td(request, id):
    '''
    模块的事务
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    presentModule = ModuleInfo.objects.values('module_name').filter(id=id)
    projectlist = projectAndModule
    fav_opt = FavTd.objects
    tdinfo = TdInfo.objects.filter(belong_module__id=id)
    kwargs = {}
    tdlist = []
    for k in xrange(len(tdinfo)):
        td = {}
        flag = fav_opt.get_fav_by_tdAndUser(account, tdinfo[k].id)
        if flag == 1:
            td.setdefault('isFav', 'true')
        else:
            td.setdefault('isFav', 'false')
        if k % 2 == 0:
            td.setdefault('right', 'true')
        else:
            td.setdefault('right', 'false')
        td.setdefault('id', tdinfo[k].id)
        td.setdefault('title', tdinfo[k].title)
        td.setdefault('td_url', tdinfo[k].td_url)
        td.setdefault('author', tdinfo[k].author)
        td.setdefault('params', eval(tdinfo[k].params))
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        tdlist.append(td)
    if request.session.get('login_status'):
        if request.is_ajax():
            td_info = json.loads(request.body.decode('utf-8'))
            kwargs['user'] = request.session["now_account"]
            kwargs['id'] = td_info.pop('id')
            if td_info.get('model') == 'pv':
                msg = add_td_pv(kwargs['id'])
            else:
                if td_info.pop('type'):
                    msg = add_fav_data(True, **kwargs)
                else:
                    msg = add_fav_data(False, **kwargs)
            return HttpResponse(get_ajax_msg(msg, 'ok'))
        else:
            manage_info = {
                'account': request.session["now_account"],
                'presentModule': presentModule[0]['module_name'],
                'tdList': tdlist,
                'projects': projectlist
            }
            init_filter_session(request)
            return render_to_response('module_td.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def project_list(request, id):
    """
    项目列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    projectlist = projectAndModule
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            if 'mode' in project_info.keys():
                msg = del_project_data(list(eval(project_info.pop('id'))))
            else:
                msg = project_info_logic(type=False, **project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/all_td/'))
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
                'projects': projectlist
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
    projectlist = projectAndModule
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            msg = project_info_logic(**project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/project_list/1/'))

        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'projects': projectlist
            }
            return render_to_response('add_project.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def edit_project(request, id):
    """
    编辑项目
    :param request:
    :param id: 项目id
    :return:
    """
    projectlist = projectAndModule
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
                'projects': projectlist
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
    projectlist = projectAndModule
    projectInfo = ProjectInfo.objects.all()
    projectInfoList = []
    pro1 = {'project_name': 'All'}
    projectInfoList.append(pro1)
    for k in xrange(len(projectInfo)):
        pro2 = {}
        pro2.setdefault('project_name', projectInfo[k].project_name)
        projectInfoList.append(pro2)

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
                'projects': projectlist
            }
            return render_to_response('module_list.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def add_module(request):
    '''
    新增模块
    :return:
    '''
    projectlist = projectAndModule
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
                'projects': projectlist
            }
            return render_to_response('add_module.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")

def edit_project(request, id):
    """
    编辑项目
    :param request:
    :param id: 模块id
    :return:
    """
    projectlist = projectAndModule
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            project_info = json.loads(request.body.decode('utf-8'))
            msg = project_info_logic(False, **project_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/edit_project/' + id + '/'))

        elif request.method == 'GET':
            projectInfo = ProjectInfo.objects.get(id=id)
            manage_info = {
                'account': account,
                'id': projectInfo.id,
                'project_name': projectInfo.project_name,
                'responsible_name': projectInfo.responsible_name,
                'test_user': projectInfo.test_user,
                'simple_desc': projectInfo.simple_desc,
                'projects': projectlist
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
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.session.get('login_status'):
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
                'projects': projectlist
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
    projectlist = projectAndModule
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
                'projects': projectlist
            }
            return render_to_response('add_td.html', manage_info)
    else:
         return HttpResponseRedirect("/qacenter/login/")


def edit_td(request, id):
    '''
    编辑事务模板
    :param request:
    :param id: 事务id
    :return:
    '''
    projectlist = projectAndModule
    account = request.session["now_account"]
    tdinfo = TdInfo.objects.get(id=id)
    td = {}
    td.setdefault('id', tdinfo.id)
    td.setdefault('title', tdinfo.title)
    td.setdefault('td_url', tdinfo.td_url)
    td.setdefault('author', tdinfo.author)
    td.setdefault('params', eval(tdinfo.params))
    td.setdefault('instruction', tdinfo.instruction)
    td.setdefault('belong_project', tdinfo.belong_project)
    td.setdefault('belong_module', tdinfo.belong_module)
    if request.session.get('login_status'):
        if request.is_ajax():
            td_info = json.loads(request.body.decode('utf-8'))
            msg = td_info_logic(False, **td_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/edit_td/' + id + '/'))

        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'tdList': td,
                'project': ProjectInfo.objects.all().values('project_name').order_by('-create_time'),
                'projects': projectlist
            }
            return render_to_response('edit_td.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def my_tds(request):
    '''
    获取我的事务模板
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    tdinfo = TdInfo.objects.filter(author=account)
    projectlist = projectAndModule
    fav_opt = FavTd.objects
    tdlist = []
    for k in xrange(len(tdinfo)):
        td = {}
        flag = fav_opt.get_fav_by_tdAndUser(account, tdinfo[k].id)
        if flag == 1:
            td.setdefault('isFav', 'true')
        else:
            td.setdefault('isFav', 'false')
        if k % 2 == 0:
            td.setdefault('right', 'true')
        else:
            td.setdefault('right', 'false')
        td.setdefault('id', tdinfo[k].id)
        td.setdefault('title', tdinfo[k].title)
        td.setdefault('td_url', tdinfo[k].td_url)
        td.setdefault('author', tdinfo[k].author)
        td.setdefault('params', eval(tdinfo[k].params))
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        tdlist.append(td)
    if request.session.get('login_status'):
        if request.method == 'GET':
            manage_info = {
                'tdList': tdlist,
                'projects': projectlist
            }
            return render_to_response('my_tds.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def my_fav(request):
    '''
    我的收藏
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    tdInfo = TdInfo.objects
    projectlist = projectAndModule
    favlist = FavTd.objects.filter(user=account).values('belong_td')
    tdlist = []
    for k in xrange(len(favlist)):
        td = {}
        td_id = favlist[k]['belong_td']
        tdinfo = tdInfo.filter(id=td_id)
        if k % 2 == 0:
            td.setdefault('right', 'true')
        else:
            td.setdefault('right', 'false')
        td.setdefault('isFav', 'true')
        td.setdefault('id', tdinfo[0].id)
        td.setdefault('title', tdinfo[0].title)
        td.setdefault('td_url', tdinfo[0].td_url)
        td.setdefault('author', tdinfo[0].author)
        td.setdefault('params', eval(tdinfo[0].params))
        td.setdefault('instruction', tdinfo[0].instruction)
        td.setdefault('belong_project', tdinfo[0].belong_project)
        td.setdefault('belong_module', tdinfo[0].belong_module)
        tdlist.append(td)
    if request.session.get('login_status'):
        if request.method == 'GET':
            manage_info = {
                'tdList': tdlist,
                'projects': projectlist
            }
            return render_to_response('my_fav.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def record(request):
    '''
    调用历史
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    projectlist = projectAndModule
    record_opt = Record.objects.all()
    recordlist = []
    for k in xrange(len(record_opt)):
        record = {}
        record.setdefault('name', record_opt[k].belong_td.title)
        record.setdefault('user', record_opt[k].user)
        record.setdefault('create_time', record_opt[k].create_time)
        record.setdefault('request', record_opt[k].request)
        record.setdefault('result', record_opt[k].result)
        recordlist.append(record)
    if request.session.get('login_status'):
        if request.is_ajax():
            record_info = json.loads(request.body.decode('utf-8'))
            msg = record_info_logic(**record_info)
            return HttpResponse(get_ajax_msg(msg, '/qacenter/record/'))

        if request.method == 'GET':
            manage_info = {
                'account': account,
                'recordList': recordlist,
                'projects': projectlist
            }
            return render_to_response('record.html', manage_info)
    else:
        return HttpResponseRedirect("/qacenter/login/")


def summary(request):
    '''
    调用量统计
    :param request:
    :return:
    '''
    account = request.session["now_account"]
    projectlist = projectAndModule
    if request.method == 'GET':
        manage_info = {
            'account': account,
            'projects': projectlist,
            'summary': '功能开发中~~~'
        }
        return render_to_response('summary.html', manage_info)