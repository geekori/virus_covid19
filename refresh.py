from PyQt5.QtCore import *
from params import *

class Refresh(QThread):
    def __init__(self,drawing):
        super(Refresh,self).__init__()
        self.drawing = drawing

    def run(self):
        while not Params.success:
            try:
                QThread.msleep(100)
                self.drawing.update()
                Params.current_time += 1

            except:
                pass