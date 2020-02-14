from common import *
from params import *
from city import *
from person import *
import numpy as np  # pip install numpy
# 人员池
class Persons(metaclass=Singleton):
    def __init__(self):
        self.persons = []                   # 保存所有的人员
        self.latency_persons = []           # 保存处于潜伏期的人员

        city = City(Params.city_center_x,Params.city_center_y)

        for value in range(0, Params.city_person_count):
            x = Params.person_position_scale * next_gaussian() + city.center_x
            y = Params.person_position_scale * next_gaussian() + city.center_y
            if x > Params.city_width:
                x = Params.city_width
            if y > Params.city_height:
                y = Params.city_height
            self.persons.append(Person(city,x,y))
    # 获取特定人群的数量
    def get_person_size(self,state):
        if state == -1:
            return len(self.persons)
        count = 0
        for person in self.persons:
            if person.state == state:
                count += 1
        return count

