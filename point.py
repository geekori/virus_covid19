class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def move_to(self,x,y):
        self.x += x
        self.y += y