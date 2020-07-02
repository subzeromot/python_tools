# -*- coding: utf-8 -*-
import sys
import os
from os import listdir
from os.path import isfile, isdir, join, dirname, splitext, basename
import xml.etree.ElementTree as ET
import numpy as np
from glob import glob
import cv2

scale_ratio = -1
dst_img_w = 480
dst_img_h = 270

def resize_img(path_src, path_dst):
    global scale_ratio
    images_url = glob(path_src+"/*")
    if not os.path.isdir(path_dst):
        os.mkdir(path_dst)
    for url in images_url:
        # print(url)
        oriimg = cv2.imread(url, cv2.IMREAD_COLOR)
        src_img_w, src_img_w, depth = oriimg.shape
        if scale_ratio == -1:
            scale_ratio = src_img_w/dst_img_w
        newimg = cv2.resize(oriimg,(int(dst_img_w),int(dst_img_h)))
        save_img_path = url.replace(path_src, path_dst)
        # print("------ save to: ", save_img_path)
        cv2.imwrite(save_img_path,newimg)

def resize_labels(path_src, path_dst):
    labels_url = glob(path_src+"/*")
    if not os.path.isdir(path_dst):
        os.mkdir(path_dst)
    for url in labels_url:
        save_file_label = url.replace(path_src, path_dst)
        f = open(save_file_label, "w+")
        print(save_file_label)
        with open(url) as fp:
            line = fp.readline()

            cnt = 1
            while line:
                # print("Line {}: {}".format(cnt, line.strip()))
                data = line.split(' ')
                data[4] = str(int(int(data[4])/scale_ratio))
                data[5] = str(int(int(data[5])/scale_ratio))
                data[6] = str(int(int(data[6])/scale_ratio))
                data[7] = str(int(int(data[7])/scale_ratio))
                # print(data)

                tmp = 1
                for d in data:
                    f.write(d)
                    if tmp < len(data):
                        f.write(' ')
                    tmp+=1

                line = fp.readline()
                cnt += 1
            f.close()

def main():
    resize_img("test/images", "new_test/images")
    print(scale_ratio)
    resize_labels("test/labels", "new_test/labels")


if __name__ == "__main__":
    main()

