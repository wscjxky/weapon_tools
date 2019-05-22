import os
import pdb
from xml_tools import get_label, set_label
import xml.etree.ElementTree as ET
from collections import defaultdict
label_dict=defaultdict()

def walk_dirs(dirname):
    with open('labels.txt', 'r')as f_r:
        labels = f_r.readlines()
        label_list=[i.strip('\n') for i in labels ]
        for l in label_list:
            label_dict[l.strip('\n')] = 0
        count=0
        for roots, dirs, files in os.walk(dirname):
            for xml_file in files:
                try:
                    if xml_file.endswith('.xml'):
                        path=roots + os.sep + xml_file
                        inputfile = ET.parse(path)
                        root = inputfile.getroot()
                        label = get_label(root)
                        if label in label_list:
                            label_dict[label] += 1
                        else:
                            # if ('ZhanDouWuRenJi'==label):
                            #     set_label(path,'WuRenJi')
                            print(path)
                            print(label)
                            count+=1

                except Exception as e:
                    print(e)
                    print(xml_file)
                    pass
    print(count)
    print(label_dict)

# 装甲车 战斗机 拖拉机 坦克 客机 导弹
walk_dirs('E:\标注汇总v1')
