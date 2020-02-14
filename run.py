import simulation
from PyQt5.QtWidgets import *
import sys
from params import *
from refresh import *
from drawing import *
from personpool import  *
from receiver import *
def init_hospital():
    Hospital()
def init_refected():
    persons = Persons().persons  # 获取所有的市民
    for i in range(0, Params.original_infected_count):
        person = None
        while True:
            person = persons[random.randrange(0,len(persons))] # 随机选择一个市民
            # 如果该市民没有被感染，则选中该市民
            if not person.is_infected():
                break
        person.be_infected()   # 让该市民被感染

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Params.app = app
    mainWindow = QMainWindow()
    ui = simulation.Ui_mainWindow()
    ui.setupUi(mainWindow)
    init_hospital()
    init_refected()
    drawing = Drawing(ui)

    refresh = Refresh(drawing)
    refresh.start()

    receiver = Receiver()
    receiver.start()
    mainWindow.show()

    sys.exit(app.exec_())