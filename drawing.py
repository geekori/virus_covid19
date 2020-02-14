# 绘制医院
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from const import *
from hospital import *
import personpool
from params import  *

class Drawing(QWidget):
    def __init__(self,ui):
        super(Drawing,self).__init__(ui.centralwidget)
        self.ui = ui
        width = self.parent().parent().size().width()
        height = self.parent().parent().size().height()

        self.setGeometry(QRect(10,10,width * 4/5,height - 20))
    # 每次Drawing刷新，都会调用该方法
    def paintEvent(self,event):
        qp = QPainter()
        qp.begin(self)
        self.drawing(qp)
        qp.end()

    # 用来绘制图形
    def drawing(self,qp):
        if Params.success:
            return
        qp.setPen(Qt.green)
        rect = QRect(Hospital().x,Hospital().y,Hospital().width,Hospital().height)
        # 开始绘制医院的边界
        qp.drawRect(rect)

        font = QFont('微软雅黑',20)
        font.setBold(True)
        qp.setFont(font)

        # 绘制文本
        qp.setPen(Qt.red)
        rect = QRect(Hospital().x - (80 - Hospital().width)//2, Hospital().y - 40,80,40)
        qp.drawText(rect,Qt.AlignCenter,'医院')

        # 绘制代表市民的5000个小矩形
        persons = personpool.Persons().persons
        if persons == None:
            return

        normal_person_count = 0   # 正常人的数量
        latency_person_count = 0  # 处于潜伏期感染者的数量
        confirmed_person_count = 0  # 已经确诊感染者的数量
        freeze_person_count = 0     # 被隔离者的数量
        death_person_count = 0      # 死亡者的数量

        for person in persons:
            if person.state == NORMAL:
                # 健康的人
                qp.setPen(Qt.white)
                normal_person_count += 1
            elif person.state == LATENCY:
                # 潜伏期感染者
                qp.setPen(QColor(255,238,0))
                latency_person_count += 1
            elif person.state == CONFIRMED:
                # 确诊患者
                qp.setPen(Qt.red)
                confirmed_person_count += 1
            elif person.state == FREEZE:
                # 已隔离者
                qp.setPen(QColor(72,255,252))
                freeze_person_count += 1
            elif person.state == DEATH:
                # 死亡患者
                qp.setPen(Qt.black)
                death_person_count += 1
            # 更新人员状态
            person.update()
            bed_half_size = Hospital().bed_size // 2
            # 设置人员块的尺寸
            rect= QRect(person.x - bed_half_size,person.y - bed_half_size,Hospital().bed_size // 2,Hospital().bed_size // 2)

            brush = QBrush(Qt.SolidPattern)
            brush.setColor(qp.pen().color())
            qp.setBrush(brush)
            qp.drawRect(rect)

        # 实时更新数据
        self.ui.labelPersonCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#000000;\">{Params.city_person_count}</span></p></body></html>')
        self.ui.labelNormalPersonCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#0000ff;\">{normal_person_count}</span></p></body></html>')
        self.ui.labelLatencyPersonCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#ffff0a;\">{latency_person_count}</span></p></body></html>')
        self.ui.labelConfirmedPersonCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#fc0107;\">{confirmed_person_count}</span></p></body></html>')
        self.ui.labelFreezePersonCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#20ffff;\">{freeze_person_count}</span></p></body></html>')
        self.ui.labelDeathPersonCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#000000;\">{death_person_count}</span></p></body></html>')
        self.ui.labelFreeBedCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#21ff06;\">{Hospital().free_bed_count}</span></p></body></html>')
        self.ui.labelNeedBedCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#fc02ff;\">{Hospital().need_bed_count}</span></p></body></html>')
        self.ui.labelCurrentTime.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">{Params.current_time // 10}</span></p></body></html>')
        self.ui.labelBedCount.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#0000ff;\">{Params.hospital_bed_count}</span></p></body></html>')
        self.ui.labelAverageFlowIntention.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#fc02ff;\">{Params.average_flow_intention}</span></p></body></html>')
        self.ui.labelBroadRate.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#fc0107;\">{Params.broad_rate}</span></p></body></html>')
        self.ui.labelLatency.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#ffff0a;\">{Params.virus_latency // 10}</span></p></body></html>')
        self.ui.labelReceiveTime.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#21ff06;\">{Params.hospital_receive_time}</span></p></body></html>')
        self.ui.labelSafeDistance.setText(f'<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">{Params.safe_distance}</span></p></body></html>')

        if latency_person_count == 0 and confirmed_person_count == 0:
            Params.success = True
            QMessageBox.information(self.ui.centralwidget,'消息','恭喜，疫情已经结束，可以摘口罩了！',QMessageBox.Ok)
            Params.app.quit()

