import os
import datetime

from pycococreatortools import pycococreatortools
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






INFO = {
    "description": "Example Dataset",
    "url": "https://github.com/waspinator/pycococreator",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "waspinator",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'cell',
        'supercategory': 'cell',
    },
]

def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg', '*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    return files


def filter_for_annotations(root, files, image_filename):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]
    return files


def translate(ROOT_DIR,IMAGE_DIR,ANNOTATION_DIR):
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    i =0
    image_id = 1
    segmentation_id = 1

    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        #所有图片
        image_files = filter_for_jpeg(root, files)
        # tree-image_files
        finish = []
        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)
            i+=1
#             image_filename_json = image_filename.split('cell')

#             image_filename_json = image_filename_json[0][:-1]+'.png'
#             print(image_filename_json)
            #创建image_info,这个其实就是每张图放进去而不是每个实例
#             if image_filename_json not in finish:
            image_info = pycococreatortools.create_image_info(
                    image_id, os.path.basename(image_filename), image.size)
            coco_output["images"].append(image_info)
#             finish.append(image_filename_json)
            

            #这方面应该先
            # filter for associated png annotations
            for root, _, files in os.walk(ANNOTATION_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    
                    annotation_filename_json = annotation_filename.split('cell')

                    annotation_filename_json = annotation_filename_json[0][:-1]+'.png'

                    print("image_filename:",image_filename,"\nannotation_filename:",annotation_filename,"\n",
                          "annotation_filename_json:",annotation_filename_json,"\n")
                    
                    image_filename_compare = image_filename.split('/')[-1]
                    annotation_filename_json_compare = annotation_filename_json.split('/')[-1]
                    
                    if annotation_filename_json_compare == image_filename_compare:
                        print("!!!!!")
                        class_id = [x['id'] for x in CATEGORIES if x['name'] in annotation_filename][0]

                        tree-class_id

                        category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                        binary_mask = np.asarray(Image.open(annotation_filename)
                                                 .convert('1')).astype(np.uint8)

                        annotation_info = pycococreatortools.create_annotation_info(
                                segmentation_id, image_id, category_info, binary_mask,
                                image.size, tolerance=2)

                        if annotation_info is not None :
                            coco_output["annotations"].append(annotation_info)

                        segmentation_id = segmentation_id + 1
            image_id = image_id + 1



    # with open('{}/instances_train2017.json'.format(ANNOTATION_DIR), 'w') as output_json_file:
    #     json.dump(coco_output, output_json_file)
    with open('{}/instances_val2017.json'.format(ANNOTATION_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)
    print(i)



def main():

    # ROOT_DIR = '/home/huang/dataset/CRAG_v2/CRAG/train'
    # IMAGE_DIR = os.path.join(ROOT_DIR, "Images")
    # ANNOTATION_DIR = os.path.join(ROOT_DIR, "annotations")


    # translate(ROOT_DIR,IMAGE_DIR,ANNOTATION_DIR)

    ROOT_DIR = '/home/huang/dataset/CRAG_v2/CRAG/valid'
    IMAGE_DIR = os.path.join(ROOT_DIR, "Images")
    ANNOTATION_DIR = os.path.join(ROOT_DIR, "annotations")

    # print(IMAGE_DIR,ANNOTATION_DIR,'????')
    translate(ROOT_DIR,IMAGE_DIR,ANNOTATION_DIR)


#     ROOT_DIR = '/home/huang/dataset/CRAG_v2/test_json/annotation'
#     IMAGE_DIR = os.path.join(ROOT_DIR, "Image")
#     ANNOTATION_DIR = os.path.join(ROOT_DIR, "annotations")

    translate(ROOT_DIR,IMAGE_DIR,ANNOTATION_DIR)



if __name__ == "__main__":
    main()
