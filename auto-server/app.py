# -*- coding: gb2312 -*-

import auto_ip_addr
import auto_WeChat

class App(object):
    pass

def main():
    wechat_monitor = auto_WeChat.WeChatMonitor()
    wechat_monitor.start()
    ipv6_monitor = auto_ip_addr.IpMonitor()
    ipv6_monitor.start()
    ipv6_monitor.monitor_thread.join()
    wechat_monitor.monitor_thread.join()
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