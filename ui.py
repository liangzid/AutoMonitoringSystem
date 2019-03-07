import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading
from cv2 import VideoCapture, cvtColor,COLOR_BGR2RGB,waitKey
import cv2


class FileDialogdemo(QWidget):
    def __init__(self, parent=None):
        super(FileDialogdemo, self).__init__(parent)


        self.setFixedSize(1152, 840) # 建立的是界面的大小？
        self.mainwidget = QWidget()  # 主控件
        self.mainwidget_layout = QGridLayout()
        self.mainwidget.setLayout(self.mainwidget_layout)
        self.mainwidget_layout.setSpacing(0)

        self.leftWidget = QWidget()
        self.leftWidget.setObjectName('leftWidget')
        self.leftWidget_layout = QGridLayout()
        self.leftWidget.setLayout(self.leftWidget_layout)
        self.leftWidget.setStyleSheet('''QWidget#leftWidget{
    background:#D8D8D8;
    border-left:1px solid #848484;
    border-bottom:1px solid #848484;
    border-top:1px solid #848484;
    border-left:1px solid #848484;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
} ''')

        self.rightWidget = QWidget()
        self.rightWidget.setObjectName('rightWidget')
        self.rightWidget_layout = QGridLayout()
        self.rightWidget.setLayout(self.rightWidget_layout)
        self.rightWidget.setStyleSheet('''QPushButton{border:none;color:black;} 
        QWidget#rightWidget{
    background:#2E2E2E;
    border-right:1px solid #848484;
    border-bottom:1px solid #848484;
    border-top:1px solid #848484;
    border-right:1px solid #848484;
    border-top-right-radius:10px;
    border-bottom-right-radius:10px;
}''')

        self.mainwidget_layout.addWidget(self.leftWidget, 0, 0, 12, 10)
        self.mainwidget_layout.addWidget(self.rightWidget, 0, 10, 12, 2)
        # self.setCentralWidget(self.mainwidget)

        # buttonLayout=QHBoxLayout()

        self.personImageButton = QPushButton('读取目标行人图像')
        self.personImageButton.setObjectName('rightButton')
        self.personImageButton.clicked.connect(self.getImage)
        self.personImageButton.setStyleSheet(
            '''QPushButton{background:#00B2EE;border-radius:5px;}QPushButton:hover{background:#1C86EE;}''')

        # 读取视频
        self.readButton = QPushButton('读取视频')
        self.readButton.setObjectName('rightButton')
        self.readButton.clicked.connect(self.getOriginalVideo)
        self.readButton.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        # 停止按钮
        self.stopButton = QPushButton('停止')
        self.stopButton.clicked.connect(self.closeVideo)
        self.stopButton.setObjectName('rightButton')
        self.stopButton.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:red;}''')

        # 关闭程序的按钮
        self.closeButton = QPushButton('关闭程序')
        self.closeButton.setObjectName('rightButton')
        self.closeButton.setFixedSize(200, 50)
        self.closeButton.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.closeButton.clicked.connect(self.close)

        # 显示图像的label
        self.goalPic = QLabel(self)
        self.goalPic.setStyleSheet(
            "QLabel{border: 3px solid #6495ED;border-radius:10px;color:black;font-size:20px;}")
        self.goalPic.setText('         目标行人图像')

        # 显示视频的label
        self.outputView = QLabel(self)
        self.outputView.setStyleSheet(
            "QLabel{border: 3px solid #6495ED;border-radius:10px;}")


        self.text1 = QLabel(self)

        # 设置一个变量，来决定是使用相机模式还是使用别的模式.我们仅仅需要获得这个状态。
        self.checkbutton = QCheckBox('直接使用摄像头')
        self.checkbutton.setChecked(True)  # 默认直接使用摄像头
        self.checkbutton.stateChanged.connect(self.checkbuttonChange)
        self.checkbutton.setStyleSheet(
            "QCheckBox{color:black;}")

        self.rightWidget_layout.addWidget(self.stopButton, 1, 0, 1, 3)
        self.rightWidget_layout.addWidget(self.readButton, 0, 0, 1, 3)
        self.rightWidget_layout.addWidget(self.personImageButton, 1, 0, 12, 3)
        self.rightWidget_layout.addWidget(self.closeButton, 12, 0, -1, 3)

        self.leftWidget_layout.addWidget(self.goalPic, 0, 0, 4, 3)
        self.leftWidget_layout.addWidget(self.outputView, 0, 3, 8, 9)
        self.leftWidget_layout.addWidget(self.text1, 5, 0, 1, 3)
        self.leftWidget_layout.addWidget(self.checkbutton, 4, 0, 1, 3)

        self.setLayout(self.mainwidget_layout)

        self.setWindowTitle('智能监控系统')

        self.setWindowOpacity(0.95)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        # 管理视频关闭的一个变量
        self.stopEvent = threading.Event()
        self.stopEvent.clear()

        #管理摄像头开闭的变量
        self.running=False

    # 设置界面全屏的，如果需要的话可以使用
    def QuanPing(self):
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width(), screen.height())

    def closeVideo(self):   # 管理视频有没有结束的，当按下close按钮的时候，视频就应该结束了。
        self.stopEvent.set()

    def getImage(self):
        x = self.goalPic.size()
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Image files (*.* )')
        self.goalPic.setPixmap(QPixmap(fname))
        self.goalPic.setScaledContents(1)
        self.goalPic.setFixedSize(x)

    # 读取原始图片的
    def getOriginalVideo(self):
        #这里是否需要对新的线程进行一个处理，来清空close按钮带来的影响
        # self.stopEvent.clear()
        # print(self.checkbutton.checkState())
        if (self.checkbutton.checkState()==2) & (self.running==False): # 即使用摄像头
            self.running=True
            self.cap = VideoCapture(0)
        elif self.checkbutton.checkState()==0:
            fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Video files (*.* )')
            self.cap = VideoCapture(fname)

        NewThread = threading.Thread(target=self.playvideo)
        NewThread.start()

    def playvideo(self):
        while self.running & self.cap.isOpened():
            success,frame=self.cap.read()
            if success:
                frame_new=cvtColor(frame,cv2.COLOR_BGR2RGB)
            else:
                print('读取失败了啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊\n')
                break
            img=QImage(frame_new[:],frame_new.shape[1],frame_new.shape[0],frame_new.shape[1]*3,QImage.Format_RGB888)
            self.outputView.setPixmap(QPixmap(QPixmap.fromImage(img)))

            # 根据播放不同的东西来确定FPS值
            if self.checkbutton.checkState() == 2:
                waitKey(1)
            else:
                waitKey(1)  # 哎，算了

            # 如果按了停止按钮则终止一切操作
            if self.stopEvent.is_set():
                print('停止按钮已按下，线程已终止。\n')
                self.stopEvent.clear()
                self.outputView.clear()
                break

    # 就是布尔型开关
    def checkbuttonChange(self):
        if self.checkbutton.checkState() == True:
            self.checkbutton.setChecked(False)
        else:
            self.checkbutton.setChecked(True)


app = QApplication(sys.argv)
ex = FileDialogdemo()
ex.show()
sys.exit(app.exec_())
