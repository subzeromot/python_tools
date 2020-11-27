import sys
import os
from os import listdir
from os.path import isfile, isdir, join, dirname, splitext, basename
import numpy as np
from glob import glob
import random
import shutil

def copy_data(src, dst, limit):

    # create folder dst
    dst_label_folder = dst + '/labels/'
    if not os.path.exists(dst_label_folder):
        os.mkdir(dst_label_folder)
    dst_img_folder = dst + '/images/'
    if not os.path.exists(dst_img_folder):
        os.mkdir(dst_img_folder)

    labels_url = glob(src + "labels" + "/*")
    random.shuffle(labels_url)
    idx = 0
    for url_label in labels_url:
        file_name = url_label.split('/')[-1].split('.txt')[0]
        url_img = src + 'images' + "/" + file_name + '.jpg'

        if not os.path.exists(url_img):
            continue

        # copy file label
        dst_label = dst_label_folder + file_name + '.txt'
        shutil.copyfile(url_label, dst_label)

        # copy file image
        dst_img = dst_img_folder + file_name + '.jpg'
        shutil.copyfile(url_img, dst_img)

        print(file_name)

        idx+=1
        if idx >= limit:
            break

def main():
    copy_data("face/data_320_320/", "/DATA4T/Dannv5/NVIDIA-train/transfer_learning_face_plate/data_train/training", 3000)
    copy_data("plate/data_320_320/", "/DATA4T/Dannv5/NVIDIA-train/transfer_learning_face_plate/data_train/training", 3000)

if __name__ == "__main__":
    main()
