/*动态改变模块信息*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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
    if (id === '#add_task') {
        var include = [];
        var i = 0;
        $("ul#pre_case li a").each(function () {
            include[i++] = [$(this).attr('id'), $(this).text()];
        });
        data['module'] = include;
    }

    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/api/') !== -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
            else {
                window.location.reload();
            }
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function auto_load(id, url, target, type) {
    var data = $(id).serializeJSON();
    if (id === '#form_message' || id ==='#belong_message' || id === '#pro_filter') {
        data = {
            "test": {
                "name": data,
                "type": type
            }
        }
    } else if (id === '#form_config') {
        data = {
            "config": {
                "name": data,
                "type": type
            }
        }
    } else {
        data = {
            "task": {
                "name": data,
                "type": type
            }
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
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function auto_load_module(id, url,types) {
    const csrftoken = getCookie('csrftoken');
    var data = $(id).serializeJSON();
    if(types == 'module'){
        data['module'] = '请选择'
        data['version'] = '请选择'
    }
    if(types =='versions'){
        data['version'] = '请选择'
    }
    console.log(data)
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': csrftoken},
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if(types =="module"){
                show_module(data)
            }else if(types=="versions"){
                show_version(data)
            }else {
                var msg = JSON.parse(data)
                myAlert(msg['msg']);
            }

        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function show_project(location,url) {
    data = {}
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data){
            var project_list = JSON.parse(data)["project_info"]
            console.log(project_list)
            var a = $(location)
            var result = []
            a.empty()
            a.prepend("<option >请选择</option>")
            for (var i = 0; i < project_list.length; i++) {
                if (project_list[i]!== "") {
                    var value = project_list[i]['project_name'];
                    var num = result.indexOf(value)
                    if (num > -1) {
                        continue
                    } else {
                        result.push(value)
                        a.prepend("<option value='" + value + "' >" + value + "</option>")
                    }
                }
            }
        }
    })
}
function show_version(data){
    var version_list = JSON.parse(data)["version_list"]
    var a = $('#version')
    var result = []
    a.empty()
    a.prepend("<option >请选择</option>")
    for (var i =0;i<version_list.length;i++) {
        if (version_list[i] !== "") {
            var value = version_list[i]['version'];
            var num = result.indexOf(value)
            if (num > -1) {
                continue
            } else {
                result.push(value)
                a.prepend("<option value='" + value + "' >" + value + "</option>")
            }
        }
    }

}

function show_module(module_info) {
    //module_info = module_info.split('replaceFlag');
    module_info = JSON.parse(module_info)['module']
    var version = $('#version')
    version.empty();
    //version.options.length=0;
    version.prepend("<option>请选择</option>")

    var a = $('#module');
    var result = []
    a.empty();
    for (var i = 0; i < module_info.length; i++) {
        if (module_info[i] !== "") {
            var value = module_info[i]['module_name'];
            var num = result.indexOf(value)
            if (num>-1){
                continue
            }else{
                result.push(value)
                a.prepend("<option value='" + value + "' >" + value + "</option>")
            }

        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

function add_module(id,url){
    const csrftoken = getCookie('csrftoken');
    var data = $(id).serializeJSON();
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': csrftoken},
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            msg = JSON.parse(data)
            myAlert(msg['msg'])
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function select_module(){
    const csrftoken = getCookie('csrftoken')
    var a = $('#project');
    var module = $('#module')
    module.empty();
    var data = a.serializeJSON()
    $.ajax({
        type: 'post',
        headers:{"X-CSRFToken":csrftoken},
        url: '/module_list/',
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            module.append("<option selected value=\"All\">All</option>")
            var module_list = JSON.parse(data)["module"]
            for(var i=0;i<module_list.length;i++){
                module.append("<option value='"+module_list[i]['module_name']+"'>"+module_list[i]['module_name']+"</option>")
            }
        }
    })

}

function search_bug(){

    const csrftoken = getCookie('csrftoken')
    var a = $('#pro_filter');
    var data = a.serializeJSON()
    var table_body = $('#table_body')
    table_body.children("tr").remove()
    console.log(data)
    var png_list;
    $.ajax({
        type: 'post',
        headers:{"X-CSRFToken":csrftoken},
        url: '/bug_list/',
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            data = JSON.parse(data)["bug_info"]
            for(var i=0;i<data.length;i++){
                table_body.prepend('<tr><td><label><input type="checkbox" name="bug_'+data[i]["id"]+'" value="'+data[i]["id"]+'"/></label></td><td id="bug_num">'+data[i]["id"]+'</td><td><a href="#" onclick="">'+data[i]["project__project_name"]+'</a></td>' +
                    '<td>'+data[i]["module__module_name"]+'</td><td>'+data[i]["version__version"]+'</td>' +
                    '<td style="width: 50%">'+data[i]["bug_title"]+'</td><td><a onclick=""> '+data[i]["plantform"]+'</a></td><td><div id='+data[i]["id"]+'><a onclick="editstate(data[i]["id"])">'+data[i]["state"]+'</a></div></td>'+
                    '<td>'+data[i]["start"]+'</td><td><a onclick=""> '+data[i]["developer__username"]+'</a></td><td><a onclick=""> '+data[i]["buger__nick_name"]+'</a></td><td id="png_url_'+data[i]["id"]+'" style="width:"'+data[i]["png_size"]+'"px"></td></tr>')
                png_list = $('#png_url_'+data[i]["id"])
                if(data[i]['png']!=null){
                    for(var png_url=0;png_url<data[i]['png'].length;png_url++){
                        png_list.append('<div id="container" class="logoImg amplifyImg" style="display: inline"><img onclick="BigBig(this.src, this.width, this.height);" data-target="#myModal" data-toggle="modal" style="width: 50px;" src="'+data[i]['png'][png_url]+'"></div>')
                    }
                }

            }
        }
    })
}


function update_data_ajax(id, url) {
    var data = $(id).serializeJSON();
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                myAlert(data);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
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
                myAlert(data);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function copy_data_ajax(id, url) {
    var data = {
        "data": $(id).serializeJSON(),
        'mode': 'copy'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                myAlert(data);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function case_ajax(type, editor) {
    var url = $("#url").serializeJSON();
    var method = $("#method").serializeJSON();
    var dataType = $("#DataType").serializeJSON();
    var caseInfo = $("#form_message").serializeJSON();
    var variables = $("#form_variables").serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data  = eval('(' + editor.session.getValue() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！');
            return
        }
    } else {
        request_data = $("#form_request_data").serializeJSON();
    }
    var headers = $("#form_request_headers").serializeJSON();
    var extract = $("#form_extract").serializeJSON();
    var validate = $("#form_validate").serializeJSON();
    var parameters = $('#form_params').serializeJSON();
    var hooks = $('#form_hooks').serializeJSON();
    var include = [];
    var i = 0;
    $("ul#pre_case li a").each(function () {
        include[i++] = [$(this).attr('id'), $(this).text()];
    });
    caseInfo['include'] = include;
    const test = {
        "test": {
            "name": caseInfo,
            "parameters": parameters,
            "variables": variables,
            "request": {
                "url": url.url,
                "method": method.method,
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "extract": extract,
            "validate": validate,
            "hooks": hooks,
        }
    };
    if (type === 'edit') {
        url = '/api/edit_case/';
    } else {
        url = '/api/add_case/';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(test),
        contentType: "application/json",
        success: function (data) {
            if (data === 'session invalid') {
                window.location.href = "/api/login/";
            } else {
                if (data.indexOf('/api/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}


function bug_ajax(){
    var projectId = "test"
}

function config_ajax(type) {
    var dataType = $("#config_data_type").serializeJSON();
    var caseInfo = $("#form_config").serializeJSON();
    var variables = $("#config_variables").serializeJSON();
    var parameters = $('#config_params').serializeJSON();
    var hooks = $('#config_hooks').serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data = eval('(' + editor.session.getValue() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！');
            return
        }
    } else {
        request_data = $("#config_request_data").serializeJSON();
    }
    var headers = $("#config_request_headers").serializeJSON();

    const config = {
        "config": {
            "name": caseInfo,
            "variables": variables,
            "parameters": parameters,
            "request": {
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "hooks": hooks,

        }
    };
    if (type === 'edit') {
        url = '/api/edit_config/';
    } else {
        url = '/api/add_config/';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(config),
        contentType: "application/json",
        success: function (data) {
            if (data === 'session invalid') {
                window.location.href = "/api/login/";
            } else {
                if (data.indexOf('/api/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

/*提示 弹出*/
function myAlert(data) {
    $('#my-alert_print').text(data);
    $('#my-alert').modal({
        relatedTarget: this
    });
}

function post(url, params) {
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

function del_row(id) {
    var attribute = id;
    var chkObj = document.getElementsByName(attribute);
    var tabObj = document.getElementById(id);
    for (var k = 0; k < chkObj.length; k++) {
        if (chkObj[k].checked) {
            tabObj.deleteRow(k + 1);
            k = -1;
        }
    }
}


function add_row(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var cell_check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var cell_key = "<input type='text' name='test[][key]'  value='' style='" + style + "' />";
    var cell_value = "<input type='text' name='test[][value]'  value='' style='" + style + "' />";
    var cell_type = "<select name='test[][type]' class='form-control' style='height: 25px; font-size: 15px; " +
        "padding-top: 0px; padding-left: 0px; border: none'> " +
        "<option>string</option><option>int</option><option>float</option><option>boolean</option></select>";
    var cell_comparator = "<select name='test[][comparator]' class='form-control' style='height: 25px; font-size: 15px; " +
        "padding-top: 0px; padding-left: 0px; border: none'> " +
        "<option>equals</option> <option>contains</option> <option>startswith</option> <option>endswith</option> <option>regex_match</option> <option>type_match</option> <option>contained_by</option> <option>less_than</option> <option>less_than_or_equals</option> <option>greater_than</option> <option>greater_than_or_equals</option> <option>not_equals</option> <option>string_equals</option> <option>length_equals</option> <option>length_greater_than</option> <option>length_greater_than_or_equals</option> <option>length_less_than</option> <option>length_less_than_or_equals</option></select>";

    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);


    newTdObj0.innerHTML = cell_check
    newTdObj1.innerHTML = cell_key;
    if (id === 'variables' || id === 'data') {
        var newTdObj3 = myNewRow.insertCell(3);
        newTdObj2.innerHTML = cell_type;
        newTdObj3.innerHTML = cell_value;
    } else if (id === 'validate') {
        var newTdObj3 = myNewRow.insertCell(3);
        newTdObj2.innerHTML = cell_comparator;
        newTdObj3.innerHTML = cell_type;
        var newTdObj4 = myNewRow.insertCell(4);
        newTdObj4.innerHTML = cell_value;
    } else {
        newTdObj2.innerHTML = cell_value;
    }
}

function add_params(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var placeholder = '单个:["value1", "value2],  多个:[["name1", "pwd1"],["name2","pwd2"]]';
    var key = "<textarea  name='test[][key]'  placeholder='单个:key, 多个:key1-key2'  style='" + style + "' />";
    var value = "<textarea  name='test[][value]'  placeholder='" + placeholder + "' style='" + style + "' />";
    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);
    newTdObj0.innerHTML = check;
    newTdObj1.innerHTML = key;
    newTdObj2.innerHTML = value;
}


function init_acs(language, theme, editor) {
    editor.setTheme("ace/theme/" + theme);
    editor.session.setMode("ace/mode/" + language);

    editor.setFontSize(17);

    editor.setReadOnly(false);

    editor.setOption("wrap", "free");

    ace.require("ace/ext/language_tools");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        autoScrollEditorIntoView: true
    });


}

function editstate(bug_id){
    var bug = $('#bug_id_'+bug_id)
    bug.children().remove()
    bug.prepend('<select name="state"  class="form-control" onchange="update_bug('+bug_id+')" id="state">\n' +
        '                                <option >请选择</option>\n' +
        '                                <option value=\'1\' >未解决</option>\n' +
        '                                <option value=\'2\' >已解决</option>\n' +
        '                                <option value=\'3\' >延期解决</option>\n' +
        '                                <option value=\'4\' >不解决</option>\n' +
        '                                <option value=\'5\' >延期</option>\n' +
        '                                <option value=\'6\' >激活</option>\n' +
        '                            </select>')

}

function update_bug(bug_id){
    const csrftoken = getCookie('csrftoken');
    var data = $('#state').serializeJSON();
    data['bug_id'] = bug_id
    console.log(data['bug_id'])
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': csrftoken},
        url: '/edit_bug/',
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            data = JSON.parse(data)['state']
            if (data !== 10000) {
                myAlert(data['msg']);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}
function BigBig(src, width, height) {
            $('#myModal').on('show.bs.modal', function () {
                var modal = $(this);
                modal.find('.modal-dialog').css({'margin-left':(document.body.clientWidth - width*1)/3 + 'px'})
                modal.find('.modal-body #image').attr("src", src)
                    .attr("width", width*10)
                    .attr("height", height*10);
            });
        }


function login(){
    var userinfo=$('#login_form').serializeJSON();
    console.log(JSON.stringify(userinfo))
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        url: '/login/',
        data: JSON.stringify(userinfo),
        contentType: "application/json",
        success: function (data) {
            data = JSON.parse(data)['status']
            if (data === 10000) {
                window.location.reload();
            }
            else {
                myAlert(data['msg']);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}
