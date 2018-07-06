DataManager
=================

Design Philosophy
-----------------

基于Django的数据工厂平台：本篇只是造数据的事务管理平台，还需要搭建一套基于spring框架，封装开发dubbo接口集合的后端平台，再通过DataManager平台调用后端平台的http接口实现造数据功能

Key Features
------------

- 项目管理：新增、编辑、删除项目、列表展示及相关操作
- 模块管理：新增、编辑、删除模块，为项目新增模块
- 添加事务模板：自定义添加事务模板，自定义入参
- 我的事务模板：铺开展示用户本人添加的事务，方便查看、编辑
- 全部事务：所有事务铺开展示，可以执行调用接口、收藏事务
- 常用事务：按调用量统计显示前10的常用事务
- 我的收藏：显示用户本人收藏的事务
- 环境管理：可添加运行环境，运行用例时可以一键切换环境
- 调用历史：查看事务被调用情况
- 调用量统计：图标展示所有事务被调用情况

本地开发环境部署
--------
1. 安装mysql数据库服务端(推荐5.7+),并设置为utf-8编码，创建相应HttpRunner数据库，设置好相应用户名、密码，启动mysql

2. 修改:qacenter/DataManager/settings.py里DATABASES字典和邮件发送账号相关配置
   ```python
        DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'qacenter',  # 新建数据库名
            'USER': 'root',  # 数据库登录名
            'PASSWORD': '123456',  # 数据库登录密码
            'HOST': '127.0.0.1',  # 数据库所在服务器ip地址
            'PORT': '3306',  # 监听端口 默认3306即可
        }
    }
    ```

3. 命令行窗口执行pip install -r requirements.txt 安装工程所依赖的库文件

4. 命令行窗口切换到DataManager目录 生成数据库迁移脚本,并生成表结构
    ```bash
        python manage.py makemigrations DataManager #生成数据迁移脚本
        python manage.py migrate  #应用到db生成数据表
    ```

5. 创建超级用户，用户后台管理数据库，并按提示输入相应用户名，密码，邮箱。 如不需用，可跳过此步骤
    ```bash
        python manage.py createsuperuser
    ```

6. 启动服务,
    ```bash
        python manage.py runserver 0.0.0.0:8000
    ```

7. 浏览器输入：http://127.0.0.1:8000/qacenter/register/  注册用户，开始尽情享用平台吧

12. 浏览器输入http://127.0.0.1:8000/admin/  输入步骤6设置的用户名、密码，登录后台运维管理系统，可后台管理数据

### 生产环境uwsgi+nginx部署参考：https://www.jianshu.com/p/d6f9138fab7b

新手入门手册
-----------
1、首先需要注册一个新用户,注册成功后会自动跳转到登录页面,正常登录即可访问页面
![注册页面](https://github.com/wangyinguang/qacenter/blob/master/images/register.png)<br>
![登录页面](https://github.com/wangyinguang/qacenter/blob/master/images/login.png)<br>
<br>
2、登陆后默认跳转到首页,左侧为菜单栏
![首页/所有事务](https://github.com/wangyinguang/qacenter/blob/master/images/all_td.png)<br>
<br>
3、首先应该先添加一个项目,事务都是以项目为维度进行管理,注意只有简描述信息可以为空
![新增项目](https://github.com/wangyinguang/qacenter/blob/master/images/add_project.png)<br>
<br>
4、列表页支持对项目进行二次编辑,单个/批量删除项目
![项目列表](https://github.com/wangyinguang/qacenter/blob/master/images/project_list.png)<br>
<br>
5、当前项目可以新增模块了，之后事务都会归属模块下，必须指定模块所属的项目,模块列表与项目列表类似，故不赘述
![新增模块](https://github.com/wangyinguang/qacenter/blob/master/images/add_module.png)<br>
<br>
6、添加事务模板，添加的事务模板需要配合后端平台http接口的地址、参数进行录入，同时参数支持文本框和下拉框两种形式，下拉框方式输入url地址，所有事务页面会根据url地址获取下拉框内容
![添加事务模板](https://github.com/wangyinguang/qacenter/blob/master/images/add_td.png)<br>
<br>
7、常用事务、我的收藏、我的事务模板、调用历史、调用量统计等模块待续


