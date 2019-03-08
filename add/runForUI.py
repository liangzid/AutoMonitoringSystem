'''
此文件修改自[person_search](https://github.com/ShuangLI59/person_search)
@inproceedings{xiaoli2017joint,
  title={Joint Detection and Identification Feature Learning for Person Search},
  author={Xiao, Tong and Li, Shuang and Wang, Bochao and Lin, Liang and Wang, Xiaogang},
  booktitle={CVPR},
  year={2017}
}

本文件修改的内容主要为：
将Python版本提升至3.x
封装了一个调用函数

liangzid
2019.3.8

'''

# import tools._init_paths
# import argparse
# import time
# import os
# import sys
# import os.path as osp
from glob import glob

import numpy as np
# import matplotlib as mpl
import matplotlib.pyplot as plt
import caffe
# from mpi4py import MPI

from lib.fast_rcnn.test_probe import _im_exfeat  #这是一个私有方法，这样用确实不太好。但是语法上没有问题，我还是保存吧！如若出现报错在此行可注意
from lib.fast_rcnn.test_gallery import _im_detect #理由同上
from lib.fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from lib.fast_rcnn.nms_wrapper import nms

from cv2 import imread as Cv2Imread
from io import BytesIO
import io #占用空间过大的话可以把这一行注释掉！
from numpy import asarray
from PIL.Image import open as PILImageOpen


def runForUI(imgWillBeDetected, imgOrigin, usegpu=0):

    # Setup caffe
    if usegpu >= 0:
        # caffe.mpi_init()
        caffe.set_mode_gpu()
        caffe.set_device(cfg.GPU_ID)
    else:
        # caffe.mpi_init()
        caffe.set_mode_cpu()

    # 设置应有的配置文件路径，此处仅仅是将其动态列举出来。更好的方法应该是放在一个文件里。有时间就完善
    gallery_def = 'models/psdb/resnet50/eval_gallery.prototxt'                # 所使用的gallery network的prototxt路径
    probe_def   = 'models/psdb/resnet50/eval_probe.prototxt'                  # 所使用的probe network的prototxt路径
    caffemodel  = 'output/psdb_train/resnet50/resnet50_iter_50000.caffemodel' # 训练的caffe模型的路径
    det_thresh  = 0.75                                                        # 可被监控的阈值
    cfg_file    = 'experiments/cfgs/resnet50.yml'                             # 配置文件路径
    set_cfgs    = None


    # Get query image and roi
    query_img = imgOrigin
    query_roi = [0, 0, 1292, 3008]  # [x1, y1, x2, y2]

    # Extract feature of the query person
    net = caffe.Net(probe_def, caffemodel, caffe.TEST)

    roi = np.asarray(query_roi).astype(np.float32).reshape(1, 4)

    feature = _im_exfeat(net, query_img, roi, ['feat'])
    query_feat = feature['feat'].squeeze()

    # query_feat = demo_exfeat(net, query_img, query_roi)
    del net  # Necessary to release cuDNN conv static workspace

    # Detect and extract feature of persons in each gallery image
    net = caffe.Net(gallery_def, caffemodel, caffe.TEST)

    # Necessary to warm-up the net, otherwise the first image results are wrong
    # Don't know why. Possibly a bug in caffe's memory optimization.
    # Nevertheless, the results are correct after this warm-up.
    _im_detect(net, query_img) # 这一步是由caffe的bug导致的，可能会出错。


    gallery_img=imgWillBeDetected

    boxes, scores, feat_dic = _im_detect(net, gallery_img, None, ['feat'])

    j = 1  # only consider j = 1 (foreground class)
    inds = np.where(scores[:, j] > det_thresh)[0]
    cls_scores = scores[inds, j]
    cls_boxes = boxes[inds, j * 4:(j + 1) * 4]
    boxes = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
    keep = nms(boxes, cfg.TEST.NMS)

    boxes = boxes[keep]
    features = feat_dic['feat'][inds][keep]

    if boxes.shape[0] == 0:
        return None, None

    features = features.reshape(features.shape[0], -1)

    if boxes is None:
        print(gallery_img, 'no detections')
        return Cv2Imread(gallery_img)

    # Compute pairwise cosine similarities,
    #   equals to inner-products, as features are already L2-normed
    similarities = features.dot(query_feat)

    # Visualize the results
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.imshow(plt.imread(gallery_img))
    plt.axis('off')

    for box, sim in zip(boxes, similarities):
        x1, y1, x2, y2, _ = box
        ax.add_patch(
            plt.Rectangle((x1, y1), x2 - x1, y2 - y1,
                          fill=False, edgecolor='#4CAF50', linewidth=3.5))
        ax.add_patch(
            plt.Rectangle((x1, y1), x2 - x1, y2 - y1,
                          fill=False, edgecolor='white', linewidth=1))
        ax.text(x1 + 5, y1 - 18, '{:.2f}'.format(sim),
                bbox=dict(facecolor='#4CAF50', linewidth=0),
                fontsize=20, color='white')

    plt.tight_layout()

    #将使用plt处理之后的图保存到内存中（提高处理速度，也可以保存到文档当中），并返回以供opencv-Python读取
    Buffer_=BytesIO() #申请缓存
    fig.savefig(Buffer_,format='png')
    Buffer_.seek(0)
    imgOutPut=PILImageOpen(Buffer_)
    Buffer_.close()

    del net

    return asarray(imgOutPut)
