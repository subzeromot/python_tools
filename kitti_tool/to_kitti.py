# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import isfile, isdir, join, dirname, splitext, basename
import xml.etree.ElementTree as ET
import numpy as np
from glob import glob
import cv2

class XMLReader:
    def __init__(self, path):
        self.file = file = open(path, 'r')

        self.path = path
        self.content = file.read()
        self.root = ET.fromstring(self.content)
        self.template = "{name} 0.00 0 0.0 {xmin} {ymin} {xmax} {ymax} 0.0 0.0 0.0 0.0 0.0 0.0 0.0"

    def get_filename(self):
        return splitext(basename(self.path))[0]

    def get_dir(self):
        return "./labels"

    def get_objects(self):
        objects = []

        for object in self.root.findall("object"):
            objects.append({
                "name" : object.find("name").text,
                "xmin" : object.find("bndbox").find("xmin").text,
                "ymin" : object.find("bndbox").find("ymin").text,
                "xmax" : object.find("bndbox").find("xmax").text,
                "ymax" : object.find("bndbox").find("ymax").text
            })

        return objects

    def fill_template(self, object):
        return self.template.format(**object)

    def export_kitti(self):
        objects = self.get_objects()

        #Skip empty
        if len(objects) == 0: return False

        file = open(join(self.get_dir(), self.get_filename()) + ".txt", 'w')

        for object in objects[:-1]:
            file.write(self.fill_template(object) + "\n")
        # Write last without '\n'
        file.write(self.fill_template(objects[-1]))

        file.close()

        return True
    def get_objects_ssd(self):
        lines = self.file.readlines()
        objects = []
        for line in lines:
            tmp = line.rstrip().split(' ')
            if len(tmp) == 1:
                continue
            print(tmp)
            objects.append({
                "name" : tmp[1],
                "xmin" : tmp[2],
                "ymin" : tmp[3],
                "xmax" : tmp[4],
                "ymax" : tmp[5]
            })
        return objects
    def get_objects_yolo(self):
        lut = {
		    0:"car",
		    1:"motorbike",
		    2:"bus",
		    3:"truck",
		    4:"bicycle",
		    5:"box",
		    6:"pile",
		    7:"trash"
	    }
        txtFile = self.path
        img_path = txtFile.replace('.txt','.jpg')
        imgsize = cv2.imread(img_path).shape
        data = self.file.readlines()
        objects = []
        for tmp in data:
            datum = tmp.rstrip().split(' ')
            if len(datum) == 1:
                continue
            datum = np.array(datum).astype(float).tolist()
            print(datum)
            xxBB = xyhw_to_xy(datum,imgsize)
            objects.append({
                "name" : lut[int(datum[0])],
                "xmin" : xxBB[0],
                "ymin" : xxBB[1],
                "xmax" : xxBB[2],
                "ymax" : xxBB[3]
            })
	    
        return objects

def process_file(path):
    xml_reader = XMLReader(path)

    return xml_reader.export_kitti()
    
def xyhw_to_xy(bbox, img_size):
	x_min = (bbox[1] - bbox[3]/2)*img_size[1]
	y_min = (bbox[2] - bbox[4]/2)*img_size[0]
	x_max = (bbox[1] + bbox[3]/2)*img_size[1]
	y_max = (bbox[2] + bbox[4]/2)*img_size[0]
	return [x_min, y_min, x_max, y_max]

def get_directory_xml_files(dir):
    return [join(dir, f) for f in listdir(dir) if isfile(join(dir, f)) and splitext(f)[1].lower() == ".xml"]


def check_argv(argv):
    return len(argv) > 1

import os
def main():
    yolo_txts = glob("xmls/*")

    for yolo_txt in yolo_txts:
        img_path = yolo_txt.replace(".xml",".jpg").replace("xmls/","images/")
        if os.path.isfile(img_path):
            print("Process: {}".format(yolo_txt))
            ret = process_file(yolo_txt)
            if not ret:
                os.system("rm {}".format(img_path))


if __name__ == "__main__":
    main()

