/*动态改变模块信息*/
function show_module(module_info, id) {
    module_info = module_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < module_info.length; i++) {
        if (module_info[i] !== "") {
            var value = module_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

function show_case(case_info, id) {
    case_info = case_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < case_info.length; i++) {
        if (case_info[i] !== "") {
            var value = case_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

/*表单信息异步传输*/
function info_ajax(id, url) {
    var data = $(id).serializeJSON();
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/device/') !== -1) {
                    myAlertSuccess("成功");
                    window.location.href = data;
                } else {
                    myAlertSuccess(data);
                }
            }
            else {
                myAlertFail(data);
            }
        },
        error: function () {
            myAlertFail('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

/*表单信息异步传输*/
function id_ajax(id, url, type) {
    data = {
        'id': id,
        'type': type
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/device/') !== -1) {
                    myAlertSuccess("成功");
                    window.location.href = data;
                } else {
                    myAlertSuccess(data);
                    location.reload();
                }
            }
            else {
                myAlertFail(data);
            }
        },
        error: function () {
            myAlertFail('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

/*事务pv异步传输*/
function pv_ajax(id, url, model, type) {
    data = {
        'id': id,
        'type': type,
        'model': model
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/device/') !== -1) {
                    myAlertSuccess(data);
                } else {
                }
            }
            else {
                myAlertFail(data);
            }
        },
        error: function () {
            myAlertFail('Sorry，事务pv更新失败!');
        }
    });
}

/*调用历史异步传输*/
function record_ajax(tdId, user, request, result, url) {
    data = {
        'belong_td': tdId,
        'user': user,
        'request': request,
        'result': result
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/device/') !== -1) {
                    myAlertSuccess(data);
                } else {
                }
            }
            else {
                myAlertFail(data);
            }
        },
        error: function () {
            myAlertFail('Sorry，调用历史添加失败!');
        }
    });
}

function auto_load(id, url, target, flag) {
    var data = $(id).serializeJSON();
    if (id === '#infoForm') {
        data = {
            "name": data,
            "flag": flag
        }
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (type === 'module') {
                show_module(data, target)
            } else {
                show_case(data, target)
            }
        }
        ,
        error: function () {
            myAlertFail('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function del_data_ajax(id, url) {
    var data = {
        "id": id,
        'mode': 'del'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                myAlertSuccess(data);
            }
            else {
                myAlertSuccess("删除成功");
                window.location.reload();
            }
        },
        error: function () {
            myAlertFail('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function clear_lender_ajax(id, mode, url) {
    var data = {
        "id": id,
        'mode': mode
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('成功') !== -1) {
                myAlertSuccess(data);
            }
            else {
                myAlertFail(data);
                window.location.reload();
            }
        },
        error: function () {
            myAlertFail('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function add_lender_ajax(id, lender, mode, url) {
    var data = {
        "id": id,
        "lender":lender,
        'mode': mode
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('成功') !== -1) {
                myAlertLendSuccess(data);
            }
            else {
                myAlertLendFail(data);
            }
        },
        error: function () {
            myAlertFail('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

/*提示 弹出*/
function myAlertSuccess(data) {
    dialog.init({
        dialogId: 'myAlert',
        msg: data,
        type: 2
    });
    var t=setTimeout(next,2000);
    function next()
    {
        dialog.hide();
        window.location.reload();
    }
}

/*提示 弹出*/
function myAlertFail(data) {
    dialog.init({
        dialogId: 'myAlert',
        msg: data,
        type: 4
    });
    var t=setTimeout(next,2000);
    function next()
    {
        dialog.hide();
        window.location.reload();
    }
}

/*提示 弹出*/
function myAlertLendSuccess(data) {
    dialog.init({
        dialogId: 'myAlert',
        msg: data,
        type: 7
    });
    var t=setTimeout(next,2000);
    function next()
    {
        dialog.hide();
        window.location.reload();
    }
}
/*提示 弹出*/
function myAlertLendFail(data) {
    dialog.init({
        dialogId: 'myAlert',
        msg: data,
        type: 6
    });
    var t=setTimeout(next,2000);
    function next()
    {
        dialog.hide();
        window.location.reload();
    }
}


function module_by_project_post(url, id) {
    var params = []
    params['belong_project'] = id;
    var temp = document.createElement("form");
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in params) {
        var opt = document.createElement("input");
        opt.name = x;
        opt.value = params[x];
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}

function getOptions(url, tdIndex, paramIndex) {
    var host = window.location.host;
    var env = $('#tdPanel' + tdIndex).find('input[name="env"]').val();
    if (env == 1) { //开启本地调试
        url = url.replace(host, "localhost:8080");
    }
    $.ajax({
        url: url,
        type: "POST",
        header: 'Access-Control-Allow-Methods:*',
        success: function(res) {
        var options = '';
        var select = $('#tdForm' + tdIndex).find('select[name="param' + paramIndex + '"]');
        content = JSON.stringify(res.entry);
        if (res.responseCode == 1) {
            var obj = eval('(' + content + ')');
            $.each(obj, function(name, value) {
                options += '<option value="' + name + '">' + value + '</option>';
            })
            select.html(options);
        } else {
            options = '<option value="">' + res.message + '</option>';
            select.html(options);
        }
    },
        error: function(res) {
            console.log(res);
        }
    });
}
