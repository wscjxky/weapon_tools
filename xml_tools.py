# 读取待修改文件
import glob
import os
import shutil
import xml.etree.ElementTree as ET


def get_label(root):
    object = root.find("object")
    name = object.find("name").text
    return name


def get_dirname(root):
    name = ''
    folder = root.find("folder")

    return folder.text


def get_filename(filename):
    inputfile = ET.parse(filename)
    root = inputfile.getroot()
    img_name = root.find("filename").text
    return img_name


def set_new_filename(filename, value):
    inputfile = ET.parse(filename)
    root = inputfile.getroot()
    name = root.find("filename")
    name.text = value
    inputfile.write(name)


def get_filename_label(root):
    img_name = root.find("filename").text
    label = get_label(root)
    return img_name, label


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


import re


def is_not_exist_mkdir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)


def imagenet_to_me():
    with open('imagenet.txt', 'r', encoding='utf8')as f:
        a = f.readlines()
        label_arr = []
        new_name_arr = []
        for i in a:
            i = i.strip('\n')
            new_name = i.split(' ')[1]
            label = i.split(' ')[0]
            label_arr.append(label)
            new_name_arr.append(new_name)

    count = 0
    dirname = "E:\标注汇总v2\songyi\斧头/"
    for roots, dirs, files in os.walk(dirname):
        try:
            for file in files:
                if file.endswith('xml'):
                    path = roots + os.sep + file
                    inputfile = ET.parse(path)
                    root = inputfile.getroot()
                    label = get_label(root)
                    if label in label_arr:
                        new_name = new_name_arr[label_arr.index(label)]
                        set_label(path, new_name)
                        new_dir = dirname + new_name
                        is_not_exist_mkdir(new_dir)
                        shutil.copy(path, new_dir)
                        img_file = get_filename(path) + '.JPEG'
                        shutil.copy(dirname + img_file, new_dir)

                        print(label)
        except Exception as e :
            print(e)
            pass
            # os.remove()
            # set_label(path, label_name)
            # set_label(path, 'WuRenJi')
    print(count)
def imagenet_to_ourlabel():
    with open('imagenet.txt', 'r', encoding='utf8')as f:
        a = f.readlines()
        label_arr = []
        new_name_arr = []
        for i in a:
            i = i.strip('\n')
            new_name = i.split(' ')[1]
            label = i.split(' ')[0]
            label_arr.append(label)
            new_name_arr.append(new_name)
    count = 0
    dirname = "E:\标注汇总v2\kaiyuan/new"
    for roots, dirs, files in os.walk(dirname):
        try:
            for file in files:
                if file.endswith('xml'):
                    path = roots + os.sep + file
                    inputfile = ET.parse(path)
                    root = inputfile.getroot()
                    label = get_label(root)
                    if label in label_arr:
                        new_name = new_name_arr[label_arr.index(label)]
                        set_label(path, new_name)
                        print(label)
        except Exception as e :
            print(e)
            pass
            # os.remove()
            # set_label(path, label_name)
            # set_label(path, 'WuRenJi')
    print(count)

if __name__ == '__main__':
    pass
    # imagenet_to_me()
# main()
