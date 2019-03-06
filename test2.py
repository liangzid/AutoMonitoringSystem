import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FileDialogdemo(QWidget):
    def __init__(self,parent=None):
        super(FileDialogdemo,self).__init__(parent)

        self.resize(500,500)



        layout=QVBoxLayout()

        self.button1=QPushButton('读取目标行人图像')
        self.button1.clicked.connect(self.getImage)
        layout.addWidget(self.button1)

        self.le=QLabel("")

        self.setLayout(layout)

        self.setWindowTitle('智能监控系统')

    def getImage(self):
        fname,_=QFileDialog.getOpenFileName(self,'Open file','./','Image files (*.* )')
        self.le.setPixmap(QPixmap(fname))

app=QApplication(sys.argv)
ex=FileDialogdemo()
ex.show()
sys.exit(app.exec_())




