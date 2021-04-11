import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.dirname(__file__)
# funzz字典
path = 'static/fuzz_dict/fuzz_domain.txt'
fuzz_domian_path = os.path.join(base_dir, path)

def get_db_url(dbinfo):
    engine =  dbinfo.get('ENGINE') or 'sqlite'
    driver = dbinfo.get('DRIVER') or 'sqlite'
    user = dbinfo.get('USER') or ''
    password = dbinfo.get('PASSWORD') or ''
    host = dbinfo.get('HOST') or ''
    post = dbinfo.get('POST') or ''
    dbname = dbinfo.get('NAME') or ''

    # url  数据库+驱动://用户名:密码@主机:端口/具体哪一个库
    return '{}+{}://{}:{}@{}:{}/{}'.format(engine,driver,user,password,host,post,dbname)

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(Config):

    DEBUG = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "webpenfw",
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(dbinfo)

class TestConfig(Config):

    TESTING = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "testFlask",
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(dbinfo)


class StagingConfig(Config):


    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "testFlask",
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(dbinfo)

class ProductConfig(Config):


    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "testFlask",
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(dbinfo)

envs = {
    'develop':DevelopConfig,  #开发环境
    'testing':TestConfig,    #测试环境
    'staging':StagingConfig,  #演示环境
    'product':ProductConfig,   #生成环境
    'default':DevelopConfig,   #默认环境为开发环境
}