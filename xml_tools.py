# 读取待修改文件
import glob
import os
import xml.etree.ElementTree as ET


def get_label(root):
    name = ''
    objects = root.findall("object")
    for obj in objects:
        name = obj.find("name").text
    return name


def get_filename(root):
    dirname = root.find('folder').text
    filename = root.find("filename").text
    return dirname + os.sep + filename


def get_boxs(root):
    objects = root.findall("object")
    bboxs = []
    for obj in objects:
        bndbox = obj.find("bndbox")
        xmin = bndbox.find('xmin').text
        xmax = bndbox.find('xmax').text
        ymin = bndbox.find('ymin').text
        ymax = bndbox.find('ymax').text
        bboxs.append([xmin, xmax, ymin, ymax])
    return bboxs


def set_label(filename, value):
    inputfile = ET.parse(filename)
    root = inputfile.getroot()
    objects = root.findall("object")
    for obj in objects:
        label = obj.find('name')
        label.text = value
    inputfile.write(filename)

#
# dir = "E:\标注汇总/fengyi\战斗机\label"
# files = glob.glob(dir + '/*.xml')
# for f in files:
#     inputfile = ET.parse(f)
#     root = inputfile.getroot()
#     label = get_label(root)
#     print(label)
#     set_label(f, "ZhanDouJi")
