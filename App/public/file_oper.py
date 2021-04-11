import os

# 封装文件读取函数
from App.public.global_var import Dome_path


def read_file(file_path):
    # print('读取文件:{}'.format(file_path))
    line_list = []
    with open(file_path,'r+') as f:
        line_list = f.readlines()

    return line_list

# 封装文件写入函数
def write_file(file_name,context):
    if type(context) == list:
        file_path = '{}/App/search_result/{}'.format(Dome_path,file_name)
        print(file_path)
        # if not os.path.isfile(file_path):
        #     os.f
        try:
            with open(file_path,'w+') as f:
                for item in context:
                    f.write(item+'\n')
        except Exception as e:
            print(e)
            return False
        return True
    else:
        print('context的数据类型必须是list.')
        return False


if __name__ == '__main__':
    read_file('d:/as/as')