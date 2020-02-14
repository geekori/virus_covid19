from common import *

class City(metaclass=Singleton):
    def __init__(self,center_x,center_y):
        self.center_x = center_x
        self.center_y = center_y