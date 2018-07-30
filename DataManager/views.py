# -*- coding: utf-8 -*-
import json
import logging
import platform

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from urllib3.connectionpool import xrange

from DataManager.models import UserInfo, ProjectInfo, ModuleInfo, TdInfo, FavTd, Record
from DataManager.utils.common import register_info_logic, get_ajax_msg, init_filter_session, project_info_logic, set_filter_session, module_info_logic, td_info_logic, record_info_logic
from DataManager.utils.httpGet import httpGet
from DataManager.utils.operation import del_project_data, del_module_data, add_fav_data, add_td_pv, projectAndModule
from DataManager.utils.pagination import get_pager_info

logger = logging.getLogger('qacenter')

# Create your views here.
separator = '\\' if platform.system() == 'Windows' else '/'

def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return HttpResponseRedirect('/qacenter/data/login/')
        return func(request, *args, **kwargs)

    return wrapper


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')

        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            logger.info('{username} 登录成功'.format(username=username))
            request.session["login_status"] = True
            request.session["now_account"] = username
            return HttpResponseRedirect('/qacenter/data/all_td/')
        else:
            logger.info('{username} 登录失败, 请检查用户名或者密码'.format(username=username))
            request.session["login_status"] = False
            return render_to_response("data/login.html")
    elif request.method == 'GET':
        return render_to_response("data/login.html")

@login_check
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
        return HttpResponseRedirect("/qacenter/data/login")


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
        return render_to_response("data/register.html")

@login_check
def base(request):
    """
    导航
    :param request:
    :return:
    """
    projectlist = projectAndModule
    manage_info = {
        'account': request.session["now_account"],
        'projects': projectlist
    }
    init_filter_session(request)
    return render_to_response('data/base.html', manage_info)


@login_check
def all_td(request):
    """
    首页
    :param request:
    :return:
    """
    account = request.session["now_account"]
    projectlist = projectAndModule
    fav_opt = FavTd.objects
    tdinfo = TdInfo.objects.all().order_by("-run_count")
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
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        td.setdefault('params', eval(tdinfo[k].params))
        tdlist.append(td)
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
        return render_to_response('data/all_td.html', manage_info)

@login_check
def hot_td(request):
    """
    常用事务：调用量前十
    :param request:
    :return:
    """
    account = request.session["now_account"]
    projectlist = projectAndModule
    fav_opt = FavTd.objects
    tdinfo = TdInfo.objects.all().order_by('-run_count')[:10]
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
        td.setdefault('instruction', tdinfo[k].instruction)
        td.setdefault('belong_project', tdinfo[k].belong_project)
        td.setdefault('belong_module', tdinfo[k].belong_module)
        td.setdefault('params', eval(tdinfo[k].params))
        tdlist.append(td)
    if request.method == 'GET':
        manage_info = {
            'account': account,
            'tdList': tdlist,
            'projects': projectlist
        }
        init_filter_session(request)
        return render_to_response('data/hot_td.html', manage_info)

@login_check
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
    tdinfo = TdInfo.objects.filter(belong_project__id=id).order_by("-run_count")
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
        return render_to_response('data/project_td.html', manage_info)

@login_check
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
    tdinfo = TdInfo.objects.filter(belong_module__id=id).order_by("-run_count")
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
        return render_to_response('data/module_td.html', manage_info)

@login_check
def project_list(request, id):
    """
    项目列表
    :param request:
    :param id: str or int：当前页
    :return:
    """
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        id = project_info.get('id')
        id_list = [int(x) for x in id.split(',')]
        if 'mode' in project_info.keys():
            msg = del_project_data(id_list)
        else:
            msg = project_info_logic(type=False, **project_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/all_td/'))
    else:
        filter_query = set_filter_session(request)
        pro_list = get_pager_info(
            ProjectInfo, filter_query, '/qacenter/data/project_list/', id)
        manage_info = {
            'account': account,
            'project': pro_list[1],
            'page_list': pro_list[0],
            'info': filter_query,
            'sum': pro_list[2],
            'projects': projectlist
        }
        return render_to_response('data/project_list.html', manage_info)

@login_check
def add_project(request):
    """
    新增项目
    :param request:
    :return:
    """
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        msg = project_info_logic(**project_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/project_list/1/'))

    elif request.method == 'GET':
        manage_info = {
            'account': account,
            'projects': projectlist
        }
        return render_to_response('data/add_project.html', manage_info)

@login_check
def edit_project(request, id):
    """
    编辑项目
    :param request:
    :param id: 项目id
    :return:
    """
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        msg = project_info_logic(False, **project_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/edit_project/' + id + '/'))

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
        return render_to_response('data/edit_project.html', manage_info)

@login_check
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
    account = request.session["now_account"]
    if request.is_ajax():
        module_info = json.loads(request.body.decode('utf-8'))
        id = module_info.get('id')
        id_list = [int(x) for x in id.split(',')]
        if 'mode' in module_info.keys():  # del module
            msg = del_module_data(id_list)
        else:
            msg = module_info_logic(type=False, **module_info)
        return HttpResponse(get_ajax_msg(msg, 'ok'))
    else:
        projectName = request.POST.get('belong_project')
        if projectName == 'All' or projectName is None:
            projectName = ''
        filter_query = {
            'belong_project': projectName,
        }
        module_list = get_pager_info(
            ModuleInfo, filter_query, '/qacenter/data/module_list/', id)
        manage_info = {
            'account': account,
            'module': module_list[1],
            'page_list': module_list[0],
            'sum': module_list[2],
            'project': projectInfoList,
            'projects': projectlist
        }
        return render_to_response('data/module_list.html', manage_info)

@login_check
def add_module(request):
    '''
    新增模块
    :return:
    '''
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        module_info = json.loads(request.body.decode('utf-8'))
        msg = module_info_logic(**module_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/module_list/1'))
    elif request.method == 'GET':
        manage_info = {
            'account': account,
            'data': ProjectInfo.objects.all().values('project_name'),
            'projects': projectlist
        }
        return render_to_response('data/add_module.html', manage_info)

@login_check
def edit_project(request, id):
    """
    编辑项目
    :param request:
    :param id: 模块id
    :return:
    """
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        msg = project_info_logic(False, **project_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/edit_project/' + id + '/'))

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
        return render_to_response('data/edit_project.html', manage_info)

@login_check
def edit_module(request, id):
    """
    编辑模块
    :param request:
    :return:
    """
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        module_info = json.loads(request.body.decode('utf-8'))
        msg = module_info_logic(False, **module_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/edit_module/' + id + '/'))

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
        return render_to_response('data/edit_module.html', manage_info)

@login_check
def add_td(request):
    '''
    添加事务模板
    :param request:
    :return:
    '''
    projectlist = projectAndModule
    account = request.session["now_account"]
    if request.is_ajax():
        td_info = json.loads(request.body.decode('utf-8'))
        msg = td_info_logic(**td_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/add_td/'))
    elif request.method == 'GET':
        manage_info = {
            'account': account,
            'project': ProjectInfo.objects.all().values('project_name').order_by('-create_time'),
            'projects': projectlist
        }
        return render_to_response('data/add_td.html', manage_info)

@login_check
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
    if request.is_ajax():
        td_info = json.loads(request.body.decode('utf-8'))
        msg = td_info_logic(False, **td_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/edit_td/' + id + '/'))

    elif request.method == 'GET':
        manage_info = {
            'account': account,
            'tdList': td,
            'project': ProjectInfo.objects.all().values('project_name').order_by('-create_time'),
            'projects': projectlist
        }
        return render_to_response('data/edit_td.html', manage_info)

@login_check
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
    if request.method == 'GET':
        manage_info = {
            'tdList': tdlist,
            'projects': projectlist
        }
        return render_to_response('data/my_tds.html', manage_info)

@login_check
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
    if request.method == 'GET':
        manage_info = {
            'account': account,
            'tdList': tdlist,
            'projects': projectlist
        }
        return render_to_response('data/my_fav.html', manage_info)

@login_check
def record(request, id):
    '''
    调用历史
    :param request:
    :param id str or int：当前页
    :return:
    '''
    account = request.session["now_account"]
    projectlist = projectAndModule
    if request.is_ajax():
        record_info = json.loads(request.body.decode('utf-8'))
        msg = record_info_logic(**record_info)
        return HttpResponse(get_ajax_msg(msg, '/qacenter/data/record/' + id + '/'))

    if request.method == 'GET':
        filter_query = {}
        record_list = get_pager_info(
            Record, filter_query, '/qacenter/data/record/', id, 15)
        manage_info = {
            'account': account,
            'record': record_list[1],
            'page_list': record_list[0],
            'sum': record_list[2],
            'projects': projectlist
        }
        return render_to_response('data/record.html', manage_info)

@login_check
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
        return render_to_response('data/summary.html', manage_info)