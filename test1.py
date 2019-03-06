# from PyQt5.QtWidgets import QMainWindow,QDesktopWidget, QApplication,QPushButton
# from PyQt5.QtGui import QIcon
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.resize(400,200)
        self.status=self.statusBar()
        self.status.showMessage('这是状态栏提示',5000)
        self.setWindowTitle('PYQT example')
        self.center()

        layout=QVBoxLayout()

        self.button1=QPushButton('打开一个视频文件')
        # self.button1.setIcon(QPixmap('./neu.png'))
        self.button1.clicked.connect(lambda:self.whichbtn(self.button1))
        self.layout().addWidget(self.button1)


    def center(self):
        screen=QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)



#创建一个上述类型的对象
app=QApplication(sys.argv)
#app.setWindowIcon(QIcon('???????'))
form=MainWindow()

# btn=QPushButton(form)
# btn.setText('button')
# btn.move(100,100)

form.show()
sys.exit(app.exec())

