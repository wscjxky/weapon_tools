import os

from xml_tools import get_label, set_label
import xml.etree.ElementTree as ET


def walk_dirs(dirname):
    label_dict = {}
    with open('labels.txt', 'r')as f_r:
        labels = f_r.readlines()
        label_list=[i.strip('\n') for i in labels ]
        for l in label_list:
            label_dict[l.strip('\n')] = 0
        for roots, dirs, files in os.walk(dirname):
            for xml_file in files:
                if xml_file.endswith('.xml'):
                    inputfile = ET.parse(roots + '/' + xml_file)
                    root = inputfile.getroot()
                    label = get_label(root)
                    if label in label_list:
                        label_dict[label] += 1
    print(label_dict)

# 装甲车 战斗机 拖拉机 坦克 客机 导弹
walk_dirs('E:\标注汇总')
