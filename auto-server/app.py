# -*- coding: gb2312 -*-

import auto_ip_addr
import auto_WeChat
import queue

class App(object):
    pass

def main():
    message_event = queue.Queue()
    ipv6_monitor = auto_ip_addr.IpMonitor(message_event=message_event)
    ipv6_monitor.start()
    
    wechat_monitor = auto_WeChat.WeChatMonitor(message_event)
    wechat_monitor.start()
    # 等待monitor线程结束
    ipv6_monitor.monitor_thread.join()
    wechat_monitor.monitor_thread.join()
    wechat_monitor.operator_thread.join()
    pass # function: main


# import ctypes
# import sys

# def run_as_admin():
#     if ctypes.windll.shell32.IsUserAnAdmin():
#         print("Already running with admin privileges")
#         return

#     # 提升权限
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# run_as_admin()