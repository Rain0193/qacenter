from django.utils.safestring import mark_safe

from DataManager.models import ModuleInfo, ProjectInfo, TdInfo


class PageInfo(object):
    """
    分页类
    """

    def __init__(self, current, total_item, per_items=5):
        self.__current = current
        self.__per_items = per_items
        self.__total_item = total_item

    @property
    def start(self):
        return (self.__current - 1) * self.__per_items

    @property
    def end(self):
        return self.__current * self.__per_items

    @property
    def total_page(self):
        result = divmod(self.__total_item, self.__per_items)
        if result[1] == 0:
            return result[0]
        else:
            return result[0] + 1


def customer_pager(base_url, current_page, total_page):
    """
    返回可分页的html
    :param base_url: a标签href值
    :param current_page: 当前页
    :param total_page: 总共页
    :return: html
    """
    per_pager = 11
    middle_pager = 5
    start_pager = 1
    if total_page <= per_pager:
        begin = 0
        end = total_page
    else:
        if current_page > middle_pager:
            begin = current_page - middle_pager
            end = current_page + middle_pager
            if end > total_page:
                end = total_page
        else:
            begin = 0
            end = per_pager
    pager_list = []

    if current_page <= start_pager:
        first = "<li><a href=''>首页</a></li>"
    else:
        first = "<li><a href='%s%d'>首页</a></li>" % (base_url, start_pager)
    pager_list.append(first)

    if current_page <= start_pager:
        prev = "<li><a href=''><<</a></li>"
    else:
        prev = "<li><a href='%s%d/'><<</a></li>" % (base_url, current_page - start_pager)
    pager_list.append(prev)

    for i in range(begin + start_pager, end + start_pager):
        if i == current_page:
            temp = "<li><a href='%s%d/' class='selected'>%d</a></li>" % (base_url, i, i)
        else:
            temp = "<li><a href='%s%d/'>%d</a></li>" % (base_url, i, i)
        pager_list.append(temp)
    if current_page >= total_page:
        next = "<li><a href=''>>></a></li>"
    else:
        next = "<li><a href='%s%d/'>>></a></li>" % (base_url, current_page + start_pager)
    pager_list.append(next)
    if current_page >= total_page:
        last = "<li><a href='''>尾页</a></li>"
    else:
        last = "<li><a href='%s%d/' >尾页</a></li>" % (base_url, total_page)
    pager_list.append(last)
    result = ''.join(pager_list)
    return mark_safe(result)  # 把字符串转成html语言


def get_pager_info(Model, filter_query, url, id, per_items=12):
    """
    筛选列表信息
    :param Model: Models实体类
    :param filter_query: dict: 筛选条件
    :param url:
    :param id:
    :param per_items: int: m默认展示12行
    :return:
    """
    id = int(id)
    if filter_query:
        belong_project = filter_query.get('belong_project')
        belong_module = filter_query.get('belong_module')
        name = filter_query.get('name')
        user = filter_query.get('user')

    obj = Model.objects

    if url == '/qacenter/data/project_list/':
        obj = obj.filter(project_name__contains=name) if name is not '' else obj.filter(responsible_name__contains=user)


    elif url == '/qacenter/data/module_list/':
        if belong_project is not '':
            obj = obj.filter(belong_project__project_name__exact=belong_project)
        else:
            obj = obj.all()
            # obj = obj.filter(module_name__contains=name) if name is not '' else obj.filter(test_user__contains=user)

    elif url == '/qacenter/data/record/':
        obj = obj.all()

    elif url != '/qacenter/data/env_list/':
        obj = obj.filter(type__exact=1) if url == '/qacenter/data/test_list/' else obj.filter(type__exact=2)

        if belong_project and belong_module is not '':
            obj = obj.filter(belong_project__contains=belong_project).filter(
                belong_module__module_name__contains=belong_module)

        else:
            if belong_project is not '':
                obj = obj.filter(belong_project__contains=belong_project)
            elif belong_module is not '':
                obj = obj.filter(belong_module__module_name__contains=belong_module)
            else:
                obj = obj.filter(name__contains=name) if name is not '' else obj.filter(author__contains=user)

    obj = obj.order_by('-update_time')

    total = obj.count()
    page_info = PageInfo(id, total, per_items=per_items)
    info = obj[page_info.start:page_info.end]

    sum = {}
    page_list = ''
    if total != 0:
        if url == '/qacenter/data/project_list/':
            for model in info:
                project_id = model.id
                td_count = str(TdInfo.objects.filter(belong_project__id=project_id).count())
                sum.setdefault(model.id, td_count)

        elif url == '/qacenter/data/module_list/':
            for model in info:
                module_id = model.id
                td_count = str(TdInfo.objects.filter(belong_module__id=module_id).count())
                sum.setdefault(model.id, td_count)

        page_list = customer_pager(url, id, page_info.total_page)

    return page_list, info, sum
