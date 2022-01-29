import os
import datetime
import imageio
import cv2.cv2
import pycocotools
from PIL.Image import Image
from boxx import *
import cv2
import numpy as np
import os, glob
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
import CRAG_To_Json



def rgb2masks(label_name,local):
    lbl_id = os.path.split(label_name)[-1].split('.')[0]
    lbl = cv2.imread(label_name, 1)
    h, w = lbl.shape[:2]
    cell_dict = {}
    idx = 0
    white_mask = np.ones((h, w, 3), dtype=np.uint8) * 255
    for i in range(h):
        for j in range(w):
            if tuple(lbl[i][j]) in cell_dict or tuple(lbl[i][j]) == (0, 0, 0):
                continue
            cell_dict[tuple(lbl[i][j])] = idx
            mask = (lbl == lbl[i][j]).all(-1)
            # leaf = lbl * mask[..., None]      # colorful leaf with black background
            # np.repeat(mask[...,None],3,axis=2)    # 3D mask
            cell = np.where(mask[..., None], white_mask, 0)
            mask_name = local + lbl_id + '_cell_' + str(idx) + '.png'
            cv2.imwrite(mask_name, cell)
            idx += 1
trainsum = 0
testsum = 0
# rgb2masks('/home/huang/dataset/CRAG_v2/CRAG/train/Annotation/train_37.png', '/home/huang/dataset/CRAG_v2/CRAG/train/Annotation/annotations/')
label_dir = '/home/huang/dataset/CRAG_v2/CRAG/valid/Annotation'
label_list = glob.glob(os.path.join(label_dir, '*.png'))
# # # print(len(label_list))
# # print(label_list[0])
local = '/home/huang/dataset/CRAG_v2/CRAG/valid/annotations/'
for label_name in label_list:
    print(label_name)
    trainsum+=1
    rgb2masks(label_name,local)
print(trainsum)

# # # picname = '/home/huang/dataset/CRAG_v2/CRAG/valid/Annotation/test_1.png'
# # # picname = imageio.imread(picname)
# # # show(picname)
# # # print(os.path.join(label_dir, '*.png'))
# # # print(glob.glob(os.path.join(label_dir, '*.png')))
# label_dir = '/home/huang/dataset/CRAG_v2/CRAG/valid/Annotation'
# label_list = glob.glob(os.path.join(label_dir, '*.png'))
# # # print(label_list)
# # # print(len(label_list))
# local = '/home/huang/dataset/CRAG_v2/CRAG/valid/Annotation/annotations/'
# for label_name in label_list:
#     testsum+=1
#     print(label_name)
#     rgb2masks(label_name,local)
# print(trainsum,testsum)






















# label_name = '/home/huang/dataset/CRAG_v2/CRAG/train/Annotation/train_1.png'
# lbl_id = os.path.split(label_name)[-1].split('.')[0]
# lbl = cv2.imread(label_name, 1)
# show(lbl)
# print(lbl.shape)
# h, w = lbl.shape[:2]
# leaf_dict = {}
# idx = 0
# white_mask = np.ones((h, w, 3), dtype=np.uint8) * 255
# for i in range(h):
#     for j in range(w):
#         if tuple(lbl[i][j]) in leaf_dict or tuple(lbl[i][j]) == (0, 0, 0):
#             continue
#         leaf_dict[tuple(lbl[i][j])] = idx
#         mask = (lbl == lbl[i][j]).all(-1)
#         # leaf = lbl * mask[..., None]      # colorful leaf with black background
#         # np.repeat(mask[...,None],3,axis=2)    # 3D mask
#         leaf = np.where(mask[..., None], white_mask, 0)
#         mask_name = '/home/huang/dataset/CRAG_v2/CRAG/train/' + lbl_id + '_cell_' + str(idx) + '.png'
#         cv2.imwrite(mask_name, leaf)
#         idx += 1














# # filter for jpeg images
# IMAGE_DIR = '/home/huang/dataset/CRAG_v2/CRAG/train/Annotation'
# for root, _, files in os.walk(IMAGE_DIR):
#     image_files = pycocotools.filter_for_jpeg(root, files)

# # go through each image
#  for image_filename in image_files:
#     image = Image.open(image_filename)
#     image_info = pycocotools.create_image_info(
#      image_id, os.path.basename(image_filename), image.size)
#     coco_output["images"].append(image_info)
#
#     # filter for associated png annotations
#     for root, _, files in os.walk(ANNOTATION_DIR):
#         annotation_files = filter_for_annotations(root, files, image_filename)
#
#         # go through each associated annotation
#         for annotation_filename in annotation_files:
#
#             if 'square' in annotation_filename:
#                 class_id = 1
#             elif 'circle' in annotation_filename:
#                 class_id = 2
#             else:
#                 class_id = 3
#
#             category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
#             binary_mask = np.asarray(Image.open(annotation_filename)
#                 .convert('1')).astype(np.uint8)
#
#             annotation_info = pycococreatortools.create_annotation_info(
#                 segmentation_id, image_id, category_info, binary_mask,
#                 image.size, tolerance=2)
#             if annotation_info is not None:
#                 coco_output["annotations"].append(
