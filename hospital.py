from params import *
from bed import *
from point import *
from common import *

class Hospital(metaclass=Singleton):
    def __init__(self):
        self.x = 1150   # 医院矩形区域左上角横坐标
        self.y = 80     # 医院矩形区域左上角横坐标
        self.width = 0  # 医院矩形区域的宽度
        self.height = 600  # 医院的高度
        self.free_bed_count = Params.hospital_bed_count
        self.need_bed_count = 0

        self.point = Point(self.x,self.y)  # 第一个床位所在的坐标

        self.beds = []  # 存储所有的床位
        self.bed_row = 100   # 床位的行数
        self.bed_size = 6    # 床位的尺寸
        self.compute()
    def compute(self,bed_count_increment = None):
        # 根据床位数调整医院矩形的大小
        if Params.hospital_bed_count == 0:
            self.width = 0
            self.height = 0
        else:
            column = Params.hospital_bed_count // self.bed_row
            if Params.hospital_bed_count % self.bed_row > 0:
                column += 1
            self.width = column * self.bed_size
            value = self.bed_row * self.bed_size
            # 添加所有的床位
            if bed_count_increment == None:
                for i in range(0,column):
                    for j in range(0,value,self.bed_size):
                        bed = Bed(self.point.x + i * self.bed_size,self.point.y + j)
                        self.beds.append(bed)
                        if len(self.beds) >= Params.hospital_bed_count:
                            break
                    if len(self.beds) >= Params.hospital_bed_count:
                        break
            else:
                index = 0
                old_len = len(self.beds)
                for i in range(0,column):
                    for j in range(0,value,self.bed_size):
                        if index >= old_len:
                            bed = Bed(self.point.x + i * self.bed_size,self.point.y + j)
                            self.beds.append(bed)
                        if len(self.beds) >= Params.hospital_bed_count:
                            break
                        index += 1
                    if len(self.beds) >= Params.hospital_bed_count:
                        break


    # 使用床位
    def pick_bed(self):
        for bed in self.beds:
            if bed.is_empty:
                bed.is_empty = False
                self.free_bed_count -= 1
                return bed

    # 由于痊愈或死亡而空出床位
    def empty_bed(self,bed):
        if bed != None:
            bed.is_empty = True
            self.free_bed_count += 1
        return bed

