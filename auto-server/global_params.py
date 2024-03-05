# -*- coding: gb2312 -*-

class GlobalParams(object):
    def __init__(self) -> None:
        self.default_screen_scale = 1.0
        self.check_interval = 10 # 各monitor检查状态的间隔时间
        pass # function: __init__
    pass # class: GlobalParams

global_parameters = GlobalParams()


