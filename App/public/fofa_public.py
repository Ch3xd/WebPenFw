from lxml import etree
import base64
import requests
from urllib.parse import quote, unquote
'''
    FOFA搜索公共调用函数py文件
    #FOFA搜索功能脚本
    1、解决了中文搜索语法乱码问题
    
    2、封装了三个公共函数
    - myrquery 请求模块
    - getip_list 获取ip/域名列表
    - yu_encodes 对特殊/中文字符进行url编码
    - is_contains_chinese 检测是否有中文字符
'''


###########################################封装请求函数##########################################
def myrquery(url,headers=''):
    if headers == '':
        headers = {
            "User-Agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.88Safari / 537.36",
        }
    try:
        reslt = requests.get(url=url, headers=headers,timeout=30)
        # print(reslt.url)
    except Exception as e:
        return False
    return reslt.text



###########################################xpath正则匹配获取IP列表##########################################
def getip_list(query_str,page=5,Cookie=''):
    if not query_str:
        return False
    try:
        page = int(page)
    except Exception as e:
        return False
    page = int(page)
    headers = {
        "User-Agent":"Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.88Safari / 537.36",
        "Cookie":Cookie,
    }
    qbase64s = unquote(query_str)
    if is_contains_chinese(qbase64s):
        qbase64 = base64.b64encode(qbase64s.encode('utf8'))
    else:
        qbase64 = base64.b64encode(qbase64s.encode('gbk'))
    qbase64 = str(qbase64)[2:-1]
    # 初始化变量
    search_url = ''
    ip_lists = []
    url_lists = []
    # 开始循环
    for pg in range(1,page+1):
        # 对+、=特殊字符进行编码，防止网页乱码报错
        if  '+' in qbase64:
            qbase64 = qbase64.replace('+',quote('+'))
        elif '=' in qbase64:
            qbase64 = qbase64.replace('=',quote('='))
        #平均正常的url请求
        search_url = "https://fofa.so/result?page={}&q={}&qbase64={}".format(pg,query_str,qbase64)
        # print(search_url)
        html = myrquery(search_url,headers)
        if html == False:
            print('抱歉?? 你没有联网~_~')
            return False
        if '游客' in html:
            print('该换cookie了~_~')
            pg -= 1
            search_url = "https://fofa.so/result?page={}&q={}&qbase64={}".format(pg, query_str, qbase64)
            # 返回url列表
            return {'url_lists':url_lists,'search_url':search_url,'nologin':True}
        tree = etree.HTML(html)
        ip_list_con = tree.xpath("//div[@class='re-domain']//text()")
        for ip in ip_list_con:
            ip = ip.replace('\n', '').strip()
            if ip == '':
                continue
            if 'http' not in ip:
                url = 'http://' + ip
            else:
                url = ip
            url_lists.append(url)
    # 返回url列表
    return {'url_lists':url_lists,'search_url':search_url}


#############################对输入的搜索语法中的&&进行编码,如果含有中文字符直接全部字符编码##########################
def yu_encodes(query_str):
    if is_contains_chinese(query_str):
        return quote(query_str)
    else:
        # 对&&进行编码
        if '&&' in query_str:
            yu = quote('&&')
            query_str = query_str.replace('&&', yu)
    return query_str



#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


#exp、fofa搜索语法输入函数封装
def you_input():
    pass
