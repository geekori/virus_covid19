from point import *
from const import *
import scipy as sp
from params import *
from math import *
import personpool
from target import *
from hospital import  *
import random

class Person(Point):
    def __init__(self,city,x,y):
        super(Person,self).__init__(x,y)
        self.city = city
        self.target_sigma = 50  # 方差

        self.sigma = 1   # 方差

        self.state = NORMAL # 当前状态

        # 感染时间
        self.infected_time = 0

        # 确诊时间
        self.confirmed_time = 0

        # 死亡时间
        self.dead_time = 0

        self.need_bed = False
        self.move_target = None
        self.used_bed = None

    # 是否有移动的意愿
    def want_move(self):
        return sp.random.normal(Params.average_flow_intention, self.sigma) > 0

    # 是否被感染
    def is_infected(self):
        return self.state >= LATENCY

    # 被感染
    def be_infected(self):
        self.state = LATENCY
        personpool.Persons().latency_persons.append(self)
        self.infected_time = Params.current_time

    # 计算两点之间的直线距离
    def distance(self,person):
        return sqrt(pow(self.x - person.x,2) + pow(self.y - person.y,2))
    def distance1(self,x,y):
        return sqrt(pow(self.x - x,2) + pow(self.y - y,2))
    # 住院
    def freezy(self):
        self.state = FREEZE
    # 不同状态下的单个人实例运行行为
    def action(self):
        if self.state == FREEZE or self.state == DEATH:
            # 处于隔离或死亡状态，无法行动
            return
        if not self.want_move():
            return

        # 存在流动意愿，将进行流动，流动同样遵循标准正态分布
        if self.move_target == None or self.move_target.arrived:
            target_x = sp.random.normal(self.x,self.target_sigma)
            target_y = sp.random.normal(self.y, self.target_sigma)
            self.move_target = MoveTarget(int(target_x),int(target_y))
        # 计算运行位移
        distance = self.distance1(self.move_target.x,self.move_target.y)
        # 到达目标点
        if distance < 1:
            self.move_target.arrived = True
            return

        dx = self.move_target.x - self.x
        dy = self.move_target.y - self.y

        udx = dx // distance
        if udx == 0 and dx != 0:
            if dx > 0:
                udx = 1
            else:
                udx = -1

        udy = dy // distance
        if udy == 0 and dy != 0:
            if dy > 0:
                udy = 1
            else:
                udy = -1

        # 横向运动边界
        if self.x > Params.city_width or self.x < 0:
            self.move_target = None
            if udx > 0:
                udx = -udx

        # 纵向运动边界
        if self.y > Params.city_height or self.y < 0:
            self.move_target = None
            if udy > 0:
                udy = -udy

        self.move_to(udx,udy)

    # 对各种状态的人进行不同的处理，更新发布市民健康状态
    def update(self):
        # 如果已经隔离或死亡，就不需要处理了
        if self.state == FREEZE or self.state == DEATH:
            return
        # 处理已经确诊的感染者（患者）
        if self.state == CONFIRMED and self.dead_time == 0:
            destiny = random.randrange(1,10001) # 幸运数字
            if destiny >= 1 and destiny <= int(Params.fatality_rate * 10000):
                # 幸运数字落在死亡区间
                self.dead_time = self.confirmed_time + self.dead_time
            else:
                self.dead_time = -1  # 未死亡
        # 患者已经确诊，并且感染时间大于医院响应时间，这时就可以入院
        if self.state == CONFIRMED and Params.current_time - self.confirmed_time >= Params.hospital_receive_time:
            bed = Hospital().pick_bed() # 查找空床位
            if bed == None:
                # 没有空床位，报告需求的床位数
                if not self.need_bed:
                    Hospital().need_bed_count += 1
                    self.need_bed = True
            else:
                # 安置病人
                self.used_bed = bed
                self.state = FREEZE
                self.x = bed.x + Hospital().bed_size // 2
                self.y = bed.y + Hospital().bed_size // 2
                # 如果已经入院的患者曾经申请过床位，那么不再申请新的床位
                if self.need_bed and Hospital().need_bed_count > 0:
                    Hospital().need_bed_count -= 1

                bed.is_empty = False
        # 处理病死者
        if(self.state == CONFIRMED or self.state == FREEZE) and Params.current_time >= self.dead_time and self.dead_time > 0:
            self.state = DEATH          # 患者死亡
            personpool.Persons().latency_persons.remove(self) # 已经死亡
            Hospital().empty_bed(self.used_bed)  # 腾出床位
            if Hospital().need_bed_count > 0:
                Hospital().need_bed_count -= 1
        # 增加一个正态分布用于潜伏期内随机发病时间
        latency_symptom_time = sp.random.normal(Params.virus_latency/2,25)

        # 处理发病的潜伏期感染者
        if self.state == LATENCY and Params.current_time - self.infected_time > latency_symptom_time:
            self.state = CONFIRMED     # 潜伏期发病
            self.confirmed_time == Params.current_time   # 刷新确诊时间

        # 处理未隔离者的移动问题
        self.action()

        # 处理健康人被感染的问题
        if self.state >= LATENCY:
            return

        latency_persons = personpool.Persons().latency_persons.copy()
        for person in latency_persons:
            random_value = random.random()
            if random_value < Params.broad_rate and self.distance(person) < Params.safe_distance:
                self.be_infected()
                break
