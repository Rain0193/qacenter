# -*- coding: utf-8 -*-
import logging

from DataManager.models import UserInfo, ProjectInfo, ModuleInfo, TdInfo
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist


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
        account = kwargs.pop('account')
        password = kwargs.pop('password')

        if user_info.filter(account_number__exact=account).filter(status=1).count() > 0:
            logger.debug('{account} 已被其他用户注册'.format(account=account))
            return '该用户名已被注册，请更换用户名'
        if user_info.filter(email__exact=email).filter(status=1).count() > 0:
            logger.debug('{email} 昵称已被其他用户注册'.format(email=email))
            return '邮箱已被其他用户注册，请更换邮箱'
        user_info.create(username=username,account_number=account, password=password, email=email)
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
        if project_name != project_opt.get_pro_info('', type=False, id=kwargs.get('index')) and project_opt.get_pro_info(project_name) > 0:
            return '该项目已存在，请重新命名'
        try:
            project_opt.update_project(kwargs.pop('index'), **kwargs)
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
            module_opt.update_module(kwargs.pop('index'), **kwargs)
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

        ModuleInfo.objects.filter(belong_project__project_name=project_name).delete()

        ProjectInfo.objects.get(id=id).delete()

    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('{project_name} 项目已删除'.format(project_name=project_name))
    return 'ok'

def del_module_data(id):
    '''
    根据模块索引删除模块数据，强制删除其下所有事务
    :param id: str or int: 项目索引
    :return: ok or tips
    '''
    try:
        module_name = ModuleInfo.objects.get_module_name('', type=False, id=id)
        ModuleInfo.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return '删除异常，请重试'
    logger.info('{module_name} 模块已删除'.format(module_name=module_name))
    return 'ok'

def add_td_data(type, **kwargs):
    '''
    事务模板信息落地
    :param type: boolean: true: 新增， false：更新
    :param kwargs: dict
    :return: ok or tips
    '''
    td_opt = TdInfo.objects
    belong_project = kwargs.pop('project')
    module = kwargs.pop('module')
    title = kwargs.pop('title')
    td_url = kwargs.pop('td_url')
    author = kwargs.pop('author')
    params = kwargs.pop('params')
    instruction = kwargs.pop('instruction')
    if type:
        try:
            belong_project = ProjectInfo.objects.get_pro_name(belong_project, type=False)
        except ObjectDoesNotExist:
            logging.error('项目信息读取失败：{belong_project}'.format(belong_project=belong_project))
            return '项目信息读取失败，请重试'
        try:
            belong_module = ModuleInfo.objects.get_module_name(module, type=False)
        except ObjectDoesNotExist:
            logging.error('模块信息读取失败：{belong_module}'.format(belong_module=belong_module))
            return '模块信息读取失败，请重试'
        # kwargs['belong_project'] = belong_project
        # kwargs['belong_module'] = belong_module
        try:
            # td_opt.insert_Td(**kwargs)
            td_opt.insert_Td(title=title, td_url=td_url, author=author, belong_project=belong_project, belong_module=belong_module,  params=params, instruction=instruction)
        except DataError:
            return '事务信息过长'
        except Exception:
            logger.error('事务添加异常： {kwargs}'.format(kwargs=kwargs))
            return '添加失败，请重试'
        logger.info('事务添加成功：{kwargs}'.format(kwargs=kwargs))
    else:
        try:
            td_opt.update_td(kwargs.pop('index'), **kwargs)
        except DataError:
            return '事务信息过长'
        except Exception:
            logger.error('更新事务失败:{kwargs}'.format(kwargs=kwargs))
            return '更新失败，请重试'
        logger.info('更新事务成功：{kwargs}'.format(kwargs=kwargs))
    return 'ok'
