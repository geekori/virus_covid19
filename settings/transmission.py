from PyQt5.QtWidgets import *
from socket import *

class Transmission:
    def __init__(self,ui):
        self.ui = ui
        self.host = 'localhost'
        self.port = 5678
        self.addr = (self.host,self.port)

    def send_command(self,command,value=None):
        tcp_client_socket = socket(AF_INET,SOCK_STREAM)
        tcp_client_socket.connect(self.addr)

        if value == None:
            value = 0

        data = command + ':' + str(value)
        tcp_client_socket.send(('%s\r\n' % data).encode(encoding='utf-8'))
        data = tcp_client_socket.recv(1024)
        result = data.decode('utf-8').strip()
        tcp_client_socket.close()
        return result
    def setup(self):
        self.ui.horizontalSliderBedCount.valueChanged.connect(self.bed_count_value_change)
        self.ui.pushButtonUpdateBedCount.clicked.connect(self.update_bed_count)

        self.ui.horizontalSliderFlowIntention.valueChanged.connect(self.flow_intention_value_change)
        self.ui.pushButtonFlowIntention.clicked.connect(self.update_flow_intention)

        self.ui.horizontalSliderBroadRate.valueChanged.connect(self.broad_rate_value_change)
        self.ui.pushButtonBroadRate.clicked.connect(self.update_broad_rate)

        self.ui.horizontalSliderLatency.valueChanged.connect(self.latency_value_change)
        self.ui.pushButtonLatency.clicked.connect(self.update_latency)

        self.ui.pushButtonClose.clicked.connect(self.close_virus_simulation)

    def bed_count_value_change(self):
        self.ui.labelBedIncrement.setText(
            f'<html><head/><body><p><span style=\" font-size:24pt; color:#0000ff;\">{self.ui.horizontalSliderBedCount.value()}</span></p></body></html>')

    def update_bed_count(self):
        print(self.ui.horizontalSliderBedCount.value())
        result = self.send_command('add_bed_count', self.ui.horizontalSliderBedCount.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, '消息', f'成功添加了{self.ui.horizontalSliderBedCount.value()}张床位',
                                    QMessageBox.Ok)

    def flow_intention_value_change(self):
        self.ui.labelFlowIntention.setText(
            f'<html><head/><body><p><span style=\" font-size:24pt; color:#fc02ff;\">{self.ui.horizontalSliderFlowIntention.value() / 100}</span></p></body></html>')

    def update_flow_intention(self):
        result = self.send_command('set_flow_intention', self.ui.horizontalSliderFlowIntention.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, '消息',
                                    f'成功设置流动意向为{self.ui.horizontalSliderFlowIntention.value() / 100}', QMessageBox.Ok)

    def broad_rate_value_change(self):
        self.ui.labelBroadRate.setText(
            f'<html><head/><body><p><span style=\" font-size:24pt; color:#fc0107;\">{self.ui.horizontalSliderBroadRate.value() / 100}</span></p></body></html>')

    def update_broad_rate(self):
        result = self.send_command('set_broad_rate', self.ui.horizontalSliderBroadRate.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, '消息',
                                    f'成功设置传播率为{self.ui.horizontalSliderBroadRate.value() / 100}', QMessageBox.Ok)

    def latency_value_change(self):
        self.ui.labelLatency.setText(
            f'<html><head/><body><p><span style=\" font-size:24pt; color:#ffff0a;\">{self.ui.horizontalSliderLatency.value()}</span></p></body></html>')

    def update_latency(self):
        result = self.send_command('set_latency', self.ui.horizontalSliderLatency.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, '消息', f'成功设置传播率为{self.ui.horizontalSliderLatency.value()}',
                                    QMessageBox.Ok)

    def close_virus_simulation(self):
        reply = QMessageBox.information(self.ui.centralwidget, "请问", "是否真的要关闭病毒扩散仿真器？",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = self.send_command('close')
            if result == 'ok':
                QMessageBox.information(self.ui.centralwidget, '消息', '已经成功关闭病毒扩散仿真器', QMessageBox.Ok)