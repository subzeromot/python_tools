# -*- coding: utf-8 -*-
import sys
import os
from os import listdir
from os.path import isfile, isdir, join, dirname, splitext, basename
import xml.etree.ElementTree as ET
import numpy as np
from glob import glob
import cv2

scale_ratio_h = -1
scale_ratio_w = -1
dst_img_w = 320
dst_img_h = 320

def resize_img(path_src, path_dst):
    global scale_ratio_h
    global scale_ratio_w

    images_url = glob(path_src+"/*")
    if not os.path.isdir(path_dst):
        os.mkdir(path_dst)
    for url in images_url:
        # print(url)
        oriimg = cv2.imread(url, cv2.IMREAD_COLOR)
        src_img_h, src_img_w, depth = oriimg.shape

        if scale_ratio_w == -1:
            scale_ratio_w = src_img_w/dst_img_w
        if scale_ratio_h == -1:
            scale_ratio_h = src_img_h/dst_img_h

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
        # print(save_file_label)
        with open(url) as fp:
            line = fp.readline()

            cnt = 1
            while line:
                # print("Line {}: {}".format(cnt, line.strip()))
                data = line.split(' ')
                data[4] = str(int(int(data[4])/scale_ratio_w))
                data[5] = str(int(int(data[5])/scale_ratio_h))
                data[6] = str(int(int(data[6])/scale_ratio_w))
                data[7] = str(int(int(data[7])/scale_ratio_h))
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

def resize_stuff_data(path, saved_path):
    src_path_img = os.path.join(path, "images")
    src_path_label = os.path.join(path, "labels")
    ratio_w = 1
    ratio_h = 1

    if not os.path.isdir(saved_path):
        print("Create path", saved_path)
        os.mkdir(saved_path)
        os.mkdir(saved_path + '/labels')
        os.mkdir(saved_path + '/images')

    label_files = glob(src_path_label + "/*")
    for lb_file in label_files:
        # get image dir
        img_file = lb_file.replace("/labels", "/images").replace(".txt", ".jpg")
        tmp_img_name = img_file.split('/')[-1]
        
        # check if image file is exist
        if not os.path.isfile(img_file):
            print("not exist: ", img_file)
            continue
        
        # get image size
        oriimg = cv2.imread(img_file, cv2.IMREAD_COLOR)
        src_img_h, src_img_w, depth = oriimg.shape

        # set ratio for current process image
        ratio_w = src_img_w/dst_img_w
        ratio_h = src_img_h/dst_img_h

        ######## resize image
        newimg = cv2.resize(oriimg,(int(dst_img_w),int(dst_img_h)))
        save_img_path = os.path.join(saved_path, "images")
        if not os.path.isdir(save_img_path):
            os.mkdir(save_img_path)
        save_img_path = os.path.join(save_img_path, tmp_img_name)
        cv2.imwrite(save_img_path,newimg)
        print(save_img_path)

        ######## resize bbox
        tmp_label_name = lb_file.split('/')[-1]
        save_file_label = os.path.join(saved_path, "labels")
        if not os.path.isdir(save_file_label):
            os.mkdir(save_file_label)
        save_file_label = os.path.join(save_file_label, tmp_label_name)

        f = open(save_file_label, "w+")
        cnt = 0
        with open(lb_file) as fp:
            line = fp.readline()
            print(line)
            while line:
                data = line.split(' ')

                tl_x = int(float(data[2])/ratio_w)
                tl_y = int(float(data[5])/ratio_h)
                br_x = int(float(data[4])/ratio_w)
                br_y = int(float(data[3])/ratio_h)

                # check size, skip too small bbox
                width = br_x - tl_x
                height = br_y - tl_y
                if width < 10 or height < 10:
                    line = fp.readline()
                    continue

                data_resize = []
                data_resize.append(data[1])
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(int(float(data[2])/ratio_w)))
                data_resize.append(str(int(float(data[3])/ratio_h)))
                data_resize.append(str(int(float(data[4])/ratio_w)))
                data_resize.append(str(int(float(data[5])/ratio_h)))
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(0))
                data_resize.append(str(0))
                print(data_resize)

                tmp = 1
                for d in data_resize:
                    f.write(d)
                    if tmp < len(data_resize):
                        f.write(' ')
                    tmp+=1
                f.write('\n')
                line = fp.readline()
                cnt += 1
        f.close()

        if cnt == 0:
            os.remove(save_file_label)

def main():
    resize_stuff_data("org_data/", "data_320_320/")


if __name__ == "__main__":
    main()

