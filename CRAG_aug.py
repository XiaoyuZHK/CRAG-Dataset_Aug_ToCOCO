import random
import numpy as np
import cv2 as cv
from boxx import *
import imageio
import imgaug as ia
from imgaug import augmenters as iaa
from imgaug.augmentables.segmaps import SegmentationMapsOnImage

ia.seed(1)
#对训练集所做 : 共有173张图片,
for i in range(92,174):
    start = str(i) + '.png'
    #原图以及标注位置
    picname = '/home/huang/dataset/CRAG_v2/CRAG/train/Images/train_'
    labname = '/home/huang/dataset/CRAG_v2/CRAG/train/Annotation/train_'
    picimg = imageio.imread(picname+start)
    labimg = imageio.imread(labname+start)
    labimg = SegmentationMapsOnImage(labimg, shape = labimg.shape)
    #随机做16种操作
    for kind in range(16):
        end = str(i) + '_aug_' + str(kind) + '.png'

        seq = iaa.Sequential([
            iaa.CoarseDropout(0.001, size_percent=0.002),
            iaa.Affine(rotate=(-180,180),shear=(-20, 20)),
            # iaa.ElasticTransformation(alpha=10, sigma=1),
            iaa.Crop(percent=(0, 0.0002)),
            iaa.Sharpen((0,0.5)),
            iaa.Sometimes(
                        0.1,
                        iaa.GaussianBlur(sigma=(0, 0.05))
                    ),
        ])

        img_aug, seg_aug = seq(image = picimg, segmentation_maps = labimg)

        #写回文件夹
        cv.imwrite(picname+end,img_aug)
        cv.imwrite(labname+end,seg_aug.draw()[0])

























