from django.db import models

'''用户信息表操作'''

class UserInfoManager(models.Manager):
    def insert_user(self, username, email, password):
        self.create(username=username, type=type, email=email, password=password)

    def query_user(self, username, password):
        return self.filter(username__exact=username, password__exact=password).count()


'''项目信息表操作'''

class ProjectInfoManager(models.Manager):
    def insert_project(self, **kwargs):
        self.create(**kwargs)

    def update_project(self, id, **kwargs):  # 如此update_time才会自动更新！！
        obj = self.get(id=id)
        obj.project_name = kwargs.get('project_name')
        obj.responsible_name = kwargs.get('responsible_name')
        obj.test_user = kwargs.get('test_user')
        obj.simple_desc = kwargs.get('simple_desc')
        obj.save()

    def get_pro_name(self, pro_name, type=True, id=None):
        if type:
            return self.filter(project_name__exact=pro_name).count()
        else:
            if id is not None:
                return self.values('project_name').filter(id__in=id)
            return self.get(project_name__exact=pro_name)

    def get_pro_info(self, type=True):
        if type:
            return self.all().values('project_name')
        else:
            return self.all()


'''模块信息表操作'''

class ModuleInfoManager(models.Manager):
    def insert_Module(self, **kwargs):
        self.create(**kwargs)

    def update_module(self, id, **kwargs):
        obj = self.get(id=id)
        obj.module_name = kwargs.get('module_name')
        obj.test_user = kwargs.get('test_user')
        obj.dev_user = kwargs.get('dev_user')
        obj.simple_desc = kwargs.get('simple_desc')
        obj.save()

    def get_module_name(self, module_name, type=True, id=None):
        if type:
            return self.filter(module_name__exact=module_name).count()
        else:
            if id is not None:
                return self.values('module_name').filter(id__in=id)
            else:
                return self.get(id=module_name)

    def get_module_by_id(self, id):
        return self.filter(id__in=id)


'''事务信息表操作'''
class TdInfoManager(models.Manager):
    def insert_td(self, title, td_url, author, belong_project, belong_module, params, instruction):
        self.create(title=title, td_url=td_url, author=author, belong_project=belong_project, belong_module=belong_module, params=params, instruction=instruction)

    def insert_td_no_module(self, title, td_url, author, belong_project, belong_module, params, instruction):
        self.create(title=title, td_url=td_url, author=author, belong_project=belong_project, params=params, instruction=instruction)

    def update_td(self, id, **kwargs):
        obj = self.get(id=id)
        obj.title = kwargs.get('title')
        obj.td_url = kwargs.get('td_url')
        obj.author = kwargs.get('author')
        obj.belong_project = kwargs.get('belong_project')
        obj.belong_module = kwargs.get('belong_module')
        obj.params = kwargs.get('params')
        obj.instruction = kwargs.get('instruction')
        obj.save()

    def update_td_no_module(self, id, title, td_url, author, project, params, instruction):
        obj = self.get(id=id)
        obj.title = title
        obj.td_url = td_url
        obj.author = author
        obj.belong_project = project
        obj.params = params
        obj.instruction = instruction
        obj.save()

    def update_td_pv(self, id, count):
        obj = self.get(id=id)
        obj.run_count = count
        obj.save()


    def get_td_info(self, belong_project=None, belong_module=None):
        if belong_project is not None:
            return self.filter(belong_project=belong_project).count()
        elif belong_module is not None:
            return self.filter(belong_module=belong_module).count()
        else:
            return self.all()

    def get_td_by_id(self, id):
        return self.get(id=id)


'''我收藏的事务表操作'''
class FavTdManager(models.Manager):
    def insert_fav(self, user, belong_td):
        self.create(user=user, belong_td=belong_td)

    def get_fav_by_tdAndUser(self, user, belong_td):
        return self.filter(user=user, belong_td=belong_td).count()


'''调用历史表操作'''
class RecordManager(models.Manager):
    def insert_record(self, user, belong_td, request, result):
        self.create(user=user, belong_td=belong_td, request=request, result=result)
