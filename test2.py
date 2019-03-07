import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading


from cv2 import VideoCapture, cvtColor,COLOR_BGR2RGB,waitKey
import cv2


class FileDialogdemo(QWidget):
    def __init__(self,parent=None):
        super(FileDialogdemo,self).__init__(parent)

        self.QuanPing() # 设置打开时处于全屏状态

        layout=QVBoxLayout()

        # 设置读取行人图像的按钮
        self.button1=QPushButton('读取目标行人图像')
        self.button1.clicked.connect(self.getImage)
        layout.addWidget(self.button1)

        # 展示的图像的具体特征
        self.label_showImage=QLabel(self)
        self.label_showImage.resize(500,500)
        self.label_showImage.move(100,100)

        # 设置读取处理之前的视频的按钮
        self.button2=QPushButton('读取需要进行处理的原视频呢！')
        self.button2.clicked.connect(self.getOriginalVideo)
        layout.addWidget(self.button2)

        # 关闭按钮，用于关闭视频播放
        self.closebutton=QPushButton('关闭操作')
        self.closebutton.clicked.connect(self.closeVideo)
        layout.addWidget(self.closebutton)

        # QLabel变量设置展示的原始视频的具体特征
        self.label_showOriginalVideo=QLabel(self)
        self.label_showOriginalVideo.resize(500,500)
        self.label_showOriginalVideo.move(600,100)

        # 设置一个变量，来决定是使用相机模式还是使用别的模式.我们仅仅需要获得这个状态。
        self.checkbutton=QCheckBox('直接使用摄像头')
        self.checkbutton.setChecked(True)#默认直接使用摄像头
        self.checkbutton.stateChanged.connect(self.checkbuttonChange)
        layout.addWidget(self.checkbutton)


        self.setLayout(layout)
        self.setWindowTitle('智能监控系统')

        # 管理视频关闭的一个变量
        self.stopEvent=threading.Event()
        self.stopEvent.clear()

        #管理摄像头开闭的变量
        self.running=False

    def QuanPing(self):
        screen=QDesktopWidget().screenGeometry()
        self.resize(screen.width(),screen.height())

    def closeVideo(self):   # 管理视频有没有结束的，当按下clos按钮的时候，视频就应该结束了。
        self.stopEvent.set()

    def getImage(self):
        fname,_=QFileDialog.getOpenFileName(self,'Open file','./','Image files (*.* )')
        self.label_showImage.setPixmap(QPixmap(fname))

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

        NewThread=threading.Thread(target=self.playvideo)
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

            self.label_showOriginalVideo.setPixmap(QPixmap(QPixmap.fromImage(img)))

            #根据播放不同的东西来确定FPS值
            if self.checkbutton.checkState()==2:
                waitKey(1)
            else:
                waitKey(1)  #哎，算了

            #如果按了停止按钮则终止一切操作
            if self.stopEvent.is_set():
                print('停止按钮已按下，线程已终止。\n')
                self.stopEvent.clear()
                self.label_showOriginalVideo.clear()
                break


    def checkbuttonChange(self):
        if self.checkbutton.checkState()==True:
            self.checkbutton.setChecked(False)
        else:
            self.checkbutton.setChecked(True)







app=QApplication(sys.argv)
ex=FileDialogdemo()
ex.show()
sys.exit(app.exec_())




