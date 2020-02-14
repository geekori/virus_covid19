from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
from common import *
from params import *
from hospital import *
from PyQt5.QtCore import *
import sys

class MyRequestHandler(SRH):
    def handle(self):
        # 读取客户端的请求
        data = str(self.rfile.readline(),'utf-8')
        # command:value
        index = data.find(':')
        # 获取客户端发送的命令
        command = data[:index]
        # 获取与命令相关的值
        value = data[index + 1:]
        value = int(value)

        if command == 'add_bed_count':
            Params.hospital_bed_count += value
            Hospital().free_bed_count = Hospital().free_bed_count + value
            Hospital().compute(value)
        elif command == 'set_flow_intention':
            Params.average_flow_intention = value / 100
        elif command == 'set_broad_rate':
            Params.broad_rate = value / 100

        elif command == 'set_latency':
            Params.virus_latency = value * 10
        elif command == 'close':
            Params.app.quit()

        self.wfile.write(b'ok\r\n')

class Receiver(QThread):
    tcp_server = None
    def __init__(self):
        super(Receiver,self).__init__()
        self.host = ''
        self.port = 5678
        self.addr = (self.host,self.port)

        Receiver.tcp_server = TCP(self.addr,MyRequestHandler)

    def run(self):
        Receiver.tcp_server.serve_forever()

