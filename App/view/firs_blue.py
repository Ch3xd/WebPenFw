from App.ext import db
from App.model import User
from App.public.fofa_public import getip_list
from App.public.file_oper import *
from App.public.global_var import *
from flask import Blueprint, render_template, request, send_from_directory

blue = Blueprint('blue',__name__)

# 添加数据
def db_add(obj):
    db.session.add(obj)
    db.session.commit()
# 删除数据
def db_delete(obj):
    db.session.delete(obj)
    db.session.commit()
# 更新数据
def db_updata():
    db.session.commit()

# 根url
@blue.route('/')
def hello_world():
    return render_template('index.html')


# FOFA
@blue.route('/fofa',methods=['GET','POST'])
def fofa_search():
    search_url = ''
    url_list = []
    workey = ''
    nologin = False
    set_cookie = ''
    set_cookie_status = 2
    is_keep = '0'
    # 接收POST提交的参数
    if request.method == 'POST':
        workey = request.form.get('fofa',type=str,default=None)
        is_keep = request.form.get('is_keep',type=str,default=None)
        set_cookie = request.form.get('cookies', type=str, default=None)
        print('is_keep:{}'.format(is_keep))
        # 去掉两边的空格
        if type(set_cookie) == str:
            set_cookie = set_cookie.strip()
        # print(set_cookie)
    # 从数据库获取cookie
    user = User.query.get(1)
    user_cookie = user.cookie
    # print(user_cookie)
    # 判断用户是否输入搜索语法
    if workey:
        res = getip_list(query_str=workey,Cookie=user_cookie)
        # 判断返回结果是否有内容
        if res:
            url_list = res.get('url_lists')
            nologin = res.get('nologin')
    # 判断是否已经获取url列表
    if not getip_list:
        ress = getip_list(workey)
        search_url = ress.get('search_url')
    # 设置FOFA—-Cookie
    if set_cookie:
        try:
            user = User.query.get(1)
            user.cookie = set_cookie
            db_updata()
            set_cookie_status = True
        except Exception as e:
            print(e)
            print('设置cookie失败~')
            set_cookie_status = False
    else:
        print('用户没有提交cookie数据')

    #保存搜索结果
    if is_keep:
        if int(is_keep) == 1:
            if url_list:
                file_status = write_file(file_name=FOFA_FILE_NAME,context=url_list)
    #保存文件路径
    res_path = os.path.join(Dome_path,'App/search_result')
    file_name_list = os.listdir(res_path)
    print(file_name_list)

    #返回的data数据
    print('nologin: {}'.format(nologin))
    context = {
        'workey':workey,
        'url_list':url_list,
        'search_url':search_url,
        'nologin':nologin,
        'cookie_status':{'cookie':user_cookie,'status':set_cookie_status},
        'file_name_list':file_name_list,
    }
    return render_template('fofa.html',**context)


#下载搜索结果
@blue.route('/down_file')
def down_file():
    filename = ''
    directory = ''
    if request.method == 'GET':
        file_path = os.path.join(Dome_path,'App/search_result')
        filename = request.args.get('file_name')
        print(filename)
        print(directory)

    return send_from_directory(file_path, filename, as_attachment=True)


# 处理ajax异步请求
@blue.route('/settings',methods=['POST'])
def settings():
    set_cookie = ''
    set_cookie_status = False
    if request.method == 'POST':
        set_cookie = request.form.get('cookies', type=str, default=None)
        # print(set_cookie)
        # 设置FOFA—-Cookie
    try:
        user = User.query.get(1)
        user.cookie = set_cookie
        db_updata()
        set_cookie_status = True
    except Exception as e:
        print(e)
        print('设置cookie失败~')