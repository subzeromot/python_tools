import sys
import os
from os import listdir
from os.path import isfile, isdir, join, dirname, splitext, basename
import numpy as np
from glob import glob
import random
import cv2

def ShuffleData(path_src_labels, path_src_imgs):
    labels_url = glob(path_src_labels + "/*")
    random.shuffle(labels_url)
    idx = 0
    for url in labels_url:
        file_name = url.split('/')[-1].split('.txt')[0]
        # change file label name
        src = url
        dst = path_src_labels + '/' + str(idx) + '.txt'
        os.rename(src, dst)

        # change file image name
        src = path_src_imgs + "/" + file_name + '.jpg'
        dst = path_src_imgs + '/' + str(idx) + '.jpg'
        os.rename(src, dst)

        idx+=1
        print(file_name)

def Verify(path_src_labels, path_src_imgs):
    print("Press ESC to exit!")
    images_url =  glob(path_src_imgs + "/*")
    for url in images_url:
        img = cv2.imread(url)

        file_name = url.split('/')[-1].split('.jpg')[0]
        label_url = path_src_labels + "/" + file_name + ".txt"
        
        with open(label_url) as fp:
            line = fp.readline()
            while line:
                data = line.split(' ')
                p1 = (int(data[4]), int(data[5]))
                p2 = (int(data[6]), int(data[7]))
                color = (255,0,0)
                cv2.rectangle(img, p1, p2, color, 2)
                line = fp.readline()
        cv2.imshow('show', img)
        if cv2.waitKey(0)==27:
            break

def main():
    ShuffleData("labels", "images")
    #Verify("labels", "images")


if __name__ == "__main__":
    main()
