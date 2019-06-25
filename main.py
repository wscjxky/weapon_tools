import os
import warnings
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict

warnings.filterwarnings("error", category=UserWarning)
from PIL import Image

from compare_similar import DHash
from functions import *


class IterFile():
    def __init__(self, root):
        self.root = root
        self.imgs_count = 0
        self.xmls_count = 0
        self.label_dict = defaultdict()
        self.img_dict = defaultdict()

        self.label_list = []
        self.count_imgs()
        self.statics_classes()

    def count_imgs(self):
        count=0
        for roots, dirs, files in os.walk(self.root):
            for file in files:
                count+=1
                if count%1000==0:
                    print(count)
                if is_img(file):
                    self.imgs_count += 1
                elif is_xml(file):
                    self.xmls_count += 1
        print("图片数量：%s" % self.imgs_count)
        print("标签数量：%s" % self.xmls_count)

    def gen_label_dict(self):
        with open('labels.txt', 'r')as f_r:
            labels = f_r.readlines()
            self.label_list = [i.strip('\n') for i in labels]
            for l in self.label_list:
                self.label_dict[l.strip('\n')] = 0
                self.img_dict[l.strip('\n')] = 0


    def statics_classes(self):
        self.gen_label_dict()
        for roots, dirs, files in os.walk(self.root):
            for file in files:
                if is_xml(file):
                    self.xmls_count += 1
                    path = roots + os.sep + file
                    label = XmlTools(path).get_label()
                    if label in self.label_list:
                        self.label_dict[label] += 1
                if is_img(file):
                    self.imgs_count += 1
                    path = roots + os.sep +'../label/'+ os.path.splitext(file)[-2] + '.xml'
                    label = XmlTools(path).get_label()
                    if label in self.label_list:
                        self.img_dict[label] += 1
        for i in self.label_dict.keys():
            print(i)
        for i in self.label_dict.values():
            print(i)
        b = sum(self.label_dict.values())
        print(b)
        print('img:')
        for i in self.img_dict.values():
            print(i)
        b = sum(self.img_dict.values())
        print(b)

class XmlTools():
    def __init__(self, filename):
        self.filename = filename
        self.inputfile = ET.parse(filename)
        self.root = self.inputfile.getroot()
        self.object = self.root.find("object")

    def get_label(self):
        name = self.object.find("name").text
        return name

    def get_dirname(self):
        folder = self.root.find("folder")
        return folder.text

    def set_label(self, value):
        for obj in self.object:
            label = obj.find('name')
            label.text = value
        self.inputfile.write(self.filename)


class ProcessFolder():
    def __init__(self, root):
        self.source_root = 'E:/DODW_v1'
        self.root = root

    def copy_files_to_one_folder(self):
        # 把数据都移动到类别名文件夹中
        for roots, dirs, files in os.walk(self.root):
            for file in files:
                try:
                    if is_img(file):
                        img_path = roots + os.sep + file
                        xml_path = roots + "/../" + 'label' + os.sep + os.path.splitext(file)[-2] + '.xml'
                        xml_tool = XmlTools(xml_path)
                        label = xml_tool.get_label()
                        new_img_dir = self.source_root + '/' + label + '/img/'
                        new_label_dir = self.source_root + '/' + label + '/label/'
                        crate_dir(new_img_dir[:-5])
                        crate_dir(new_label_dir[:-7])
                        crate_dir(new_img_dir)
                        crate_dir(new_label_dir)
                        # 把img和相应的label复制到new里，
                        shutil.copy(xml_path, new_label_dir + os.path.splitext(file)[-2] + '.xml')
                        shutil.copy(img_path, new_img_dir + file)
                except Exception as e:
                    print(e)


class ImgSimilar():
    def __init__(self, root):
        self.distance_arr = []
        self.root = root
        self.new_set = []
        self.similar_count = 0

    def gen_distance_set(self):
        # TODO 改为多进程并行
        for roots, dirs, files in os.walk(self.root):
            for file in files:
                try:
                    if is_img(file):
                        # img_path=roots+os.sep+file
                        hash = os.path.splitext(file)[-2]
                        # print(hash)
                        # img = Image.open(img_path)
                        # hash = DHash.calculate_hash(img)
                        # 去重
                        if hash in self.distance_arr:
                            # print(hash)
                            self.similar_count += 1
                        else:
                            self.distance_arr.append(hash)
                except Exception as e:
                    print(e)
                    pass
                    # print(len(self.distance_arr))
                    # print(len(set(self.distance_arr)))
        print("重复图片数：%s" % self.similar_count)

    def gen_distance_files(self):
        # 生成文件名是hash长度的图片
        for roots, dirs, files in os.walk(self.root):
            for file in files:
                try:
                    if is_img(file):
                        img_path = roots + os.sep + file
                        xml_path = self.root + os.sep + 'label' + os.sep + os.path.splitext(file)[-2] + '.xml'
                        # print(hash)
                        img = Image.open(img_path)
                        hash = DHash.calculate_hash(img)
                        new_img_path = self.root + "/new/img/" + hash + os.path.splitext(file)[-1]
                        new_xml_path = self.root + "/new/label/" + hash + '.xml'
                        # 把img和相应的label复制到new里，
                        shutil.copy(xml_path, new_xml_path)
                        shutil.copy(img_path, new_img_path)
                        print(new_img_path, new_xml_path)
                        print(hash)
                except Exception as e:
                    print(e)
                    pass


source_root = 'E:/DODW_v1'
iter_file = IterFile(source_root)
# imgsim = ImgSimilar('E:\标注汇总v2')
# imgsim.gen_distance_set()
# pro_folder = ProcessFolder('E:\标注汇总v2')
# pro_folder.copy_files_to_one_folder()
