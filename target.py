#
class MoveTarget:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.arrived = False  # 是否达到目标点