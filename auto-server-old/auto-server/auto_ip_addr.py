# -*- coding: gb2312 -*-

import monitors
import time
import queue
import socket
import global_params

class IpMonitor(monitors.Monitor):
    def __init__(self, message_event: queue.Queue) -> None:
        '''
        /***************************************************************************************************/
        *   __init__: 初始化IpMonitor结构体
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # TODO: 获取以前的ip地址
        # self.ipv6用于存储系统ipv6地址信息
        self.ipv6 = []
        self.message_event = message_event
        # 调用父类，创建一个名为IpMonitor的线程，用于执行本类的monitor方法
        # 该线程将在本类继承自父类的start()函数被调用时被真正创建
        super().__init__("IpMonitor")
        pass # function: __init__
    
    def monitor(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor: 重写父类的monitor方法
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # 调用本类的monitor_ip方法
        self.monitor_ip()
        pass # function monitor
    
    # 获取ipv4地址，由于编写代码时计算机仅有局域网ipv4地址，无公网ipv4地址，因此该地址为局域网ipv4地址
    def get_ipv4_address(self):
        hostname = socket.gethostname()    
        ipv4_address = socket.gethostbyname(hostname)
        return ipv4_address
        pass # function: get_ipv4_address
    
    # 获取公网ipv6地址，windows11版本会有临时ipv6地址和ipv6地址，这个函数全都包含，排除以fe80开头的本地ipv6地址
    # 经测试，临时ipv6地址和ipv6地址都可以从外网访问
    def get_public_ipv6_address(self):
        ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        public_ipv6_addresses = [addr[4][0] for addr in ip_addresses if not addr[4][0].startswith("fe80")]
        return public_ipv6_addresses
        pass # function: get_public_ipv6_address
    
    # 获取ipv6地址
    def get_ipv6_address(self):
        ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        ipv6_addresses = [addr[4][0] for addr in ip_addresses]
        return ipv6_addresses
        pass # function: get_ipv6_address
    
    def check_ipv6_changed(self) -> bool:
        '''
        /***************************************************************************************************/
        *   check_ipv6_changed: 检查ipv6地址是否发生改变，windows11存在临时ipv6和正常ipv6地址，两个都可以被外网访问
        *   任何一个发生改变都视为ipv6地址发生变化
        *
        *   输入: 无
        *
        *   输出: bool
        *       如果ipv6地址信息发生改变，返回True，否则返回False
        /***************************************************************************************************/
        '''
        ipv6 = self.get_public_ipv6_address()
        if set(ipv6) != set(self.ipv6): # ipv6地址发生改变
            print("warning: ipv6 addr has changed!")
            print("old ip:", self.ipv6)
            print("new ip:", ipv6)
            self.ipv6 = ipv6 # 修改monitor中的ipv6地址，便于之后将其发送给operator
            return True
        else:
            print("debug: ipv6 addr keep the same.")
            return False
            pass # end if wechat_exe
        pass # function get_state
    
    def monitor_ip(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor_ip: 监控ipv6地址是否发生改变，如果发生变化，则会通知WeChat进程发送消息
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # 开始运行
        while True:
            # 检查Ipv6地址信息是否发生改变
            state_chaged = self.check_ipv6_changed()
            if state_chaged: # ipv6地址发生改变，调用self.operate()执行相应的动作
                self.operate()
                # self.state_changed.put(True) # 情况发生变化(ip地址发生改变)，通知operator执行操作
            else:
                # self.state_changed.put(False) # 一切正常(ip地址没有发生改变)，不需要put，不需要通知operator去执行操作
                pass # end if wechat_exe
            time.sleep(global_params.global_parameters.check_interval) # 每check_interval秒检查一次ip地址是否发生改变
            pass # end while True
        pass # function: monitor_ip
    
    def operate(self) -> None:
        '''
        /***************************************************************************************************/
        *   operate: 通知WeChat进程发送消息
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # TODO: ip地址发生变化时，通知wechat，发送信息
        print("TODO: ip地址发生变化时，通知wechat，发送信息")
        for ipv6 in self.ipv6:
            self.message_event.put(ipv6)
            pass # for ipvt in self.ipv6
        pass # function operate
    pass # class: IpMonitor



# class IpOperator(operators.Operator):
#     def operate(self, monitor: monitors.IpMonitor) -> None:
#         print("ip addr changed!", monitor.ipv6)
#         pass # function: operate
#     pass # class IpOperator