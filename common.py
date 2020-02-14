# 实现单件模式
import math
import random
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# 实现高斯随机函数，高斯分布也称为正态分布
def next_gaussian():
    v1 = 0.0
    v2 = 0.0
    s = 0.0
    while True:
        v1 = 2 * random.random() - 1
        v2 = 2 * random.random() - 1
        s = v1 * v2 + v2 * v2
        if not(s >= 1 or s == 0):
            break

    s = math.fabs(s)
    multiplier = math.sqrt(-2 * math.log(s)/2)
    return v1 * multiplier

