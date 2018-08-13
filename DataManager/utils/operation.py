# -*- coding: utf-8 -*-
import logging

from DataManager.models import UserInfo, ProjectInfo, ModuleInfo, TdInfo, FavTd, Record
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist
from urllib3.connectionpool import xrange

logger = logging.getLogger('qacenter')

def add_register_data(**kwargs):
    """
    用户注册信息逻辑判断及落地
    :param kwargs: dict
    :return: ok or tips
    """
    user_info = UserInfo.objects
    try:
        username = kwargs.pop('username')
        email = kwargs.pop('email')
        password = kwargs.pop('password')
        type = kwargs.pop('type')

        if user_info.filter(username__exact=username).filter(status=1).count() > 0:
            logger.debug('{account} 已被其他用户注册'.format(username=username))
            return '该用户名已被注册，请更换用户名'
        if user_info.filter(email__exact=email).filter(status=1).count() > 0:
            logger.debug('{email} 昵称已被其他用户注册'.format(email=email))
            return '邮箱已被其他用户注册，请更换邮箱'
        user_info.create(username=username, password=password, email=email, type=type)
        logger.info('新增用户：{user_info}'.format(user_info=user_info))
        return 'ok'
    except DataError:
        logger.error('信息输入有误：{user_info}'.format(user_info=user_info))
        return '字段长度超长，请重新编辑'


def add_project_data(type, **kwargs):
    """
    项目信息落地
    :param type: true: 新增， false: 更新
    :param kwargs: dict
    :return: ok or tips
    """
    project_opt = ProjectInfo.objects
    project_name = kwargs.get('project_name')
    if type:
        if project_opt.get_pro_name(project_name) < 1:
            try:
                project_opt.insert_project(**kwargs)
            except DataError:
                return '项目信息过长'
            except Exception:
                logger.error('项目添加异常：{kwargs}'.format(kwargs=kwargs))
                return '添加失败，请重试'
            logger.info('项目添加成功：{kwargs}'.format(kwargs=kwargs))
        else:
            return '该项目已存在，请重新命名'
    else:
        try:
            project_opt.update_project(kwargs.pop('id'), **kwargs)
        except DataError:
            return '项目信息过长'
        except Exception:
            logger.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return '更新失败，请重试'
        logger.info('项目更新成功：{kwargs}'.format(kwargs=kwargs))
    return 'ok'

def add_module_data(type, **kwargs):
    '''
    模块信息落地
    :param type: boolean: true: 新增， false：更新
    :param kwargs: dict
    :return: ok or tips
    '''
    module_opt = ModuleInfo.objects
    belong_project = kwargs.pop('belong_project')
    module_name = kwargs.get('module_name')
    if type:
        if module_opt.filter(belong_project__project_name__exact=belong_project).filter(module_name__exact=module_name).count() < 1:
            try:
                belong_project = ProjectInfo.objects.get_pro_name(belong_project, type=False)
            except ObjectDoesNotExist:
                logging.error('项目信息读取失败：{belong_project}'.format(belong_project=belong_project))
                return '项目信息读取失败，请重试'
            kwargs['belong_project'] = belong_project
            try:
                module_opt.insert_Module(**kwargs)
            except DataError:
                return '模块信息过长'
            except Exception:
                logger.error('模块添加异常： {kwargs}'.format(kwargs=kwargs))
                return '添加失败，请重试'
            logger.info('模块添加成功：{kwargs}'.format(kwargs=kwargs))
        else:
            return '该模块已在项目中存在，请重新编辑'
    else:
        try:
            module_opt.update_module(kwargs.pop('id'), **kwargs)
        except DataError:
            return '模块信息过长'
        except Exception:
            logger.error('更新模块失败:{kwargs}'.format(kwargs=kwargs))
            return '更新失败，请重试'
        logger.info('更新模块成功：{kwargs}'.format(kwargs=kwargs))
    return 'ok'


def del_project_data(id):
    """
    根据项目索引删除项目数据，强制删除其下模块、事务
    :param id: str or int: 项目索引
    :return: ok or tips
    """
    try:
        project_name = ProjectInfo.objects.get_pro_name('', type=False, id=id)

        ModuleInfo.objects.filter(belong_project__project_name__in=project_name).delete()

        ProjectInfo.objects.filter(id__in=id).delete()

    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('{project_name} 项目已删除'.format(project_name=project_name))
    return 'ok'

def del_module_data(id):
    '''
    根据模块索引删除模块数据，强制删除其下所有事务
    :param id: str or int: 模块索引
    :return: ok or tips
    '''
    try:
        module_name = ModuleInfo.objects.get_module_name('', type=False, id=id)
        ModuleInfo.objects.filter(id__in=id).delete()
    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('{module_name} 模块已删除'.format(module_name=module_name))
    return 'ok'

def del_td_data(id):
    '''
    根据事务索引删除事务数据
    :param id: str or int: 事务索引
    :return: ok or tips
    '''
    try:
        TdInfo.objects.filter(id__in=id).delete()
    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('事务已删除'.format(id=id))
    return 'ok'

def add_td_data(type, **kwargs):
    '''
    事务模板信息落地
    :param type: boolean: true: 新增， false：更新
    :param kwargs: dict
    :return: ok or tips
    '''
    td_opt = TdInfo.objects
    project = kwargs.get('project')
    module = kwargs.get('module')
    title = kwargs.get('title')
    td_url = kwargs.get('td_url')
    author = kwargs.get('author')
    params = kwargs.get('params')
    instruction = kwargs.get('instruction')
    if type:
        try:
            belong_project = ProjectInfo.objects.get_pro_name(project, type=False)
        except ObjectDoesNotExist:
            logging.error('项目信息读取失败：{belong_project}'.format(belong_project=belong_project))
            return '项目信息读取失败，请重试'
        if module != '0':
            try:
                belong_module = ModuleInfo.objects.get_module_name(module, type=False)
            except ObjectDoesNotExist:
                logging.error('模块信息读取失败：{belong_module}'.format(belong_module=belong_module))
                return '模块信息读取失败，请重试'
            try:
                td_opt.insert_td(title=title, td_url=td_url, author=author, belong_project=belong_project, belong_module=belong_module,  params=params, instruction=instruction)
            except DataError:
                return '事务信息过长'
            except Exception:
                logger.error('事务添加异常： {kwargs}'.format(kwargs=kwargs))
                return '添加失败，请重试'
        else:
            try:
                td_opt.insert_td_no_module(title=title, td_url=td_url, author=author, belong_project=belong_project, params=params, instruction=instruction)
            except DataError:
                return '事务信息过长'
            except Exception:
                logger.error('事务添加异常： {kwargs}'.format(kwargs=kwargs))
                return '添加失败，请重试'
        logger.info('事务添加成功：{kwargs}'.format(kwargs=kwargs))
    else:
        try:
            belong_project = ProjectInfo.objects.get_pro_name(project, type=False)
        except ObjectDoesNotExist:
            logging.error('项目信息读取失败：{belong_project}'.format(belong_project=belong_project))
            return '项目信息读取失败，请重试'
        kwargs['belong_project'] = belong_project
        if module != '0':
            try:
                belong_module = ModuleInfo.objects.get_module_name(module, type=False)
            except ObjectDoesNotExist:
                logging.error('模块信息读取失败：{belong_module}'.format(belong_module=belong_module))
                return '模块信息读取失败，请重试'
            kwargs['belong_module'] = belong_module
            try:
                td_opt.update_td(kwargs.pop('id'), **kwargs)
            except DataError:
                return '事务信息过长'
            except Exception:
                logger.error('更新事务失败:{kwargs}'.format(kwargs=kwargs))
                return '更新失败，请重试'
            logger.info('更新事务成功：{kwargs}'.format(kwargs=kwargs))
        else:
            try:
                td_opt.update_td_no_module(id=id, title=title, td_url=td_url, author=author, belong_project=belong_project, params=params, instruction=instruction)
            except DataError:
                return '事务信息过长'
            except Exception:
                logger.error('事务更新异常： {kwargs}'.format(kwargs=kwargs))
                return '更新失败，请重试'
        logger.info('事务更新成功：{kwargs}'.format(kwargs=kwargs))
    return 'ok'


def add_fav_data(type, **kwargs):
    '''
    我的收藏信息落地
    :param type: boolean: true: 新增， false：更新
    :param kwargs: dict
    :return: ok or tips
    '''
    favTd_opt = FavTd.objects
    id = kwargs.get('id')
    user = kwargs.get('user')
    flag = favTd_opt.get_fav_by_tdAndUser(user, id)
    if type:
        try:
            belong_td = TdInfo.objects.get_td_by_id(id)
        except ObjectDoesNotExist:
            logging.error('事务信息读取失败：{belong_project}'.format(belong_td=belong_td))
            return '事务信息读取失败，请重试'
        try:
            if flag == 0:
                favTd_opt.insert_fav(user=user, belong_td=belong_td)
            else:
                return '已经订阅'
        except DataError:
            return '收藏信息过长'
        except Exception:
            logger.error('收藏添加异常： {kwargs}'.format(kwargs=kwargs))
            return '订阅失败，请重试'
        return '订阅成功'
    else:
        try:
            favTd_opt.filter(belong_td=id).delete()
        except ObjectDoesNotExist:
            return '删除异常，请重试'
        return '取消订阅成功'


def add_td_pv(id):
    '''
    事务pv
    :param type: boolean: true: 新增， false：更新
    :param kwargs: dict
    :return: ok or tips
    '''
    td_opt = TdInfo.objects
    try:
        pv = td_opt.values('run_count').filter(id=id)
        count = pv[0]['run_count'] + 1
        td_opt.update_td_pv(id, count)
    except ObjectDoesNotExist:
        logger.error('事务pv更新异常： {kwargs}'.format(id=id))
        return '更新失败，请重试'
    return '{"entry":{"success":"事务pv更新成功"}}'

def add_record_data(**kwargs):
    '''
    调用历史
    :param kwargs: dict
    :return: ok or tips
    '''
    record_opt = Record.objects
    user = kwargs.get('user')
    tdId = kwargs.get('belong_td')
    request = kwargs.get('request')
    result = kwargs.get('result')
    try:
        belong_td = TdInfo.objects.get_td_by_id(tdId)
        record_opt.insert_record(user=user, belong_td=belong_td, request=request, result=result)
    except ObjectDoesNotExist:
        logger.error('调用历史添加异常： {kwargs}'.format(kwargs=kwargs))
        return '调用历史添加失败，请重试'
    return '调用历史添加成功'

def projectAndModule():
    '''
    查询项目和模块列表
    :param kwargs: dict
    :return: ok or tips
    '''
    projectInfo = ProjectInfo.objects.all()
    projectlist = []
    for k in xrange(len(projectInfo)):
        pro = {}
        moduleInfo = ModuleInfo.objects.filter(belong_project__id=projectInfo[k].id)
        pro.setdefault("id", projectInfo[k].id)
        pro.setdefault("project_name", projectInfo[k].project_name)
        pro.setdefault("moduleList", moduleInfo)
        projectlist.append(pro)
    return projectlist