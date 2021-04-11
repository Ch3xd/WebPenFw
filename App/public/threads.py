import time
import queue
import threading


#自定义多线程类封装
class MyThread:

    def __init__(self,thread=147,filePath='',waitTime=7,domain=None,func=None):
        self.multi = thread  # 线程数量
        self.queueSize = thread + 37  # 申请队列空间大小,值一般略大于multi的值
        self.filePath = filePath  # 文件路径，和脚本同一目录下可直接用文件名
        self.waitTime = waitTime  # 文件线程准备时间(s)，默认1s，若需要读取的文件大小大于10M可增加至5s以上，文件越大设置的时间理论上越长
        self.workQueue = queue.Queue(self.queueSize)
        self.domain = domain
        self.func=func

    def read_file(self):
        with open(self.filePath,'r') as fp:
            file_data = fp.readlines()
        dataList = file_data
        dataLength = len(dataList)
        flag_xy = 0
        while flag_xy != dataLength:
            while (not self.workQueue.full()) and (flag_xy != dataLength):
                self.workQueue.put(dataList[flag_xy])
                flag_xy += 1
            continue
        # print("文件内容放入队列完成")


    def multi_start_tmain(self):
        while not self.workQueue.empty():
            file_line_api = self.workQueue.get()
            self.custom_def(file_line_api)


    def custom_def(self,file_line_api):
        fileDataLine = file_line_api.strip()  # fileDataLine变量为文件的每一行内容,可直接用
        # ================= #
        # 自定义功能从下方开始
        # ================= #
        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        # print(fileDataLine)  # 测试代码：将文件中每一行的信息延时1s输出
        self.func(fileDataLine,self.domain)


    def run(self):
        # =========================================================
        threads = []
        fileThread = threading.Thread(target=self.read_file)
        fileThread.start()
        print("文件读取线程准备时间%ss" %self.waitTime)
        time.sleep(self.waitTime)
        for i in range(self.multi+1):
            thread = threading.Thread(target=self.multi_start_tmain)
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        fileThread.join()
        print("主线程结束，任务完成")


# 测试用函数
def test():
    print('hello word!')


if __name__ == '__main__':
    my = MyThread(filePath='../ip.txt',thread=17,waitTime=3,func=test)
    my.run()

