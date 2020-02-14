import settings
import sys
from PyQt5.QtWidgets import *
from transmission import  *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = settings.Ui_MainWindow()

    ui.setupUi(mainWindow)
    transmission = Transmission(ui)
    transmission.setup()
    mainWindow.show()
    sys.exit(app.exec_())