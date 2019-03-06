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


        self.label_showImage=QLabel(self)
        self.label_showImage.resize(500,500)
        self.label_showImage.move(100,100)

        self.button2=QPushButton('读取需要进行处理的原视频呢！')
        self.button2.clicked.connect(self.getOriginalVideo)

        self.setLayout(layout)

        self.setWindowTitle('智能监控系统')


    def QuanPing(self):
        screen=QDesktopWidget().screenGeometry()
        self.resize(screen.width(),screen.height())



    def getImage(self):
        fname,_=QFileDialog.getOpenFileName(self,'Open file','./','Image files (*.* )')
        self.label_showImage.setPixmap(QPixmap(fname))

    def getOriginalVideo(self):
        fname,_=QFileDialog.getOpenFileName(self,'Open file','./','Video files (*.* )')






app=QApplication(sys.argv)
ex=FileDialogdemo()
ex.show()
sys.exit(app.exec_())




