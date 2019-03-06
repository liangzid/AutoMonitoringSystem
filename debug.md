# Bug Log
## Bug of Picture can not show
the message :
```buildoutcfg
Gtk-Message: 20:23:58.583: GtkDialog mapped without a transient parent. This is discouraged.
```
## bug 2 of opencv cvtColor
```
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/home/liangzi/anaconda3/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/home/liangzi/anaconda3/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "/home/liangzi/code/mycode/AutoMonitoringSystem/test2.py", line 92, in playvideo
    frame_new=cvtColor(frame,COLOR_BGR2RGB)
cv2.error: OpenCV(4.0.0) /io/opencv/modules/imgproc/src/color.cpp:181: error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'
```


