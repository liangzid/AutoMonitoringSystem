import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FileDialogdemo(QWidget):
    def __init__(self,parent=None):
        super(FileDialogdemo,self).__init__(parent)


        self.QuanPing() # 设置打开时处于全屏状态



        layout=QVBoxLayout()

        self.button1=QPushButton('读取目标行人图像')
        self.button1.clicked.connect(self.getImage)
        layout.addWidget(self.button1)


        self.le=QLabel(self)
        self.le.resize(500,500)
        self.le.move(100,100)

        self.setLayout(layout)

        self.setWindowTitle('智能监控系统')


    def QuanPing(self):
        screen=QDesktopWidget().screenGeometry()
        self.resize(screen.width(),screen.height())



    def getImage(self):
        fname,_=QFileDialog.getOpenFileName(self,'Open file','./','Image files (*.* )')
        self.le.setPixmap(QPixmap(fname))

app=QApplication(sys.argv)
ex=FileDialogdemo()
ex.show()
sys.exit(app.exec_())




