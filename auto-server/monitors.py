# -*- coding: gb2312 -*-

import wmi
import threading

# monitor 抽象类
class Monitor(object):
    def __init__(self, monitor_name: str) -> None:
        '''
        /***************************************************************************************************/
        *   Monitor: 初始化Monitor类
        *       创建Monitor监控线程
        *
        *   输入: 
        *       monitor_name: 创建的监控线程名称
        *
        *   输出:
        *       无
        /***************************************************************************************************/
        '''
        # 创建线程
        self.monitor_thread = threading.Thread(target=self.monitor, name=monitor_name, daemon=True)
        pass # function __init__
    
    def start(self) -> None:
        '''
        /***************************************************************************************************/
        *   启动Monitor初始化时创建的线程
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        self.monitor_thread.start()
        pass # function start
    
    def monitor(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor: 父类Monitor定义了一个monitor接口，该接口被monitor_thread使用，需子类自行实现
        /***************************************************************************************************/
        '''
        pass # function monitor
    
    def operate(self) -> None:
        '''
        /***************************************************************************************************/
        *   operate: 父类Monitor定义了一个operate接口，
        *   该接口被monitor方法调用，需子类自行实现monitor的调用及函数实现
        /***************************************************************************************************/
        '''
        print("not implement!")
        pass # function operate
    
    pass # class Monitor







# 使用wmi库获取所有正在运行的进程信息。
# 本程序未使用这种方式，原因是效率太低。
def check_process_running(process_name):
    c = wmi.WMI()
    for process in c.Win32_Process():
        # print(process.Name) # process.Name包含后缀名，例如输出的结果为WeChat.exe
        if process.Name == process_name:
            return True
    return False