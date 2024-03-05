# -*- coding: gb2312 -*-

import wmi
import threading


# TODO: 
# 1、抽象Monitor结构体出来
# 2、WeChatMonitor放到auto_WeChat.py中
# 3、IpMonitor放到auto_ip_addr.py中

# monitor 抽象类
class Monitor(object):
    def __init__(self, monitor_name: str) -> None:
        # 创建线程
        self.monitor_thread = threading.Thread(target=self.monitor, name=monitor_name, daemon=True)
        pass # function __init__
    
    def start(self) -> None:
        self.monitor_thread.start()
        pass # function start
    
    def monitor(self) -> None:
        pass # function monitor
    
    def operate(self) -> None:
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

