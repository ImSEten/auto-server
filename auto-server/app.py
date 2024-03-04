import monitor
import threading

class App(object):
    pass

def main():
    wechat_monitor = monitor.WeChatMonitor()
    wechat_thread = threading.Thread(target=wechat_watcher, args=(wechat_monitor,))
    wechat_thread.start()
    ipv6_monitor = monitor.IpMonitor()
    ipv6_thread = threading.Thread(target=ipv6_watcher, args=(ipv6_monitor,))
    ipv6_thread.start()
    pass # function: main

def wechat_watcher(wechat_monitor: monitor.WeChatMonitor):
    while True:
        wechat_is_running_queue = wechat_monitor.wechat_is_running_queue.get()
        if wechat_is_running_queue:
            continue
        else:
            # TODO: start wechat
            pass # end if wechat_is_running_queue
        print("wechat is running:", wechat_is_running_queue)
        pass # end while True
    pass # function: wechat_thread

def ipv6_watcher(ipv6_monitor: monitor.IpMonitor):
    while True:
        ipv6_changed = ipv6_monitor.ipv6_changed.get()
        if not ipv6_changed:
            continue
        else:
            # TODO: ipv6_changed, send message
            pass # end if wechat_is_running_queue
        print("ipv6 has changed:", ipv6_changed)
        pass # end while True
    pass # function: wechat_thread

