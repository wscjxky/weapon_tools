import glob
import os
import re


def delete_file(dirname):
    xmls = glob.glob(dirname + '/label/*.xml')
    imgs = glob.glob(dirname + '/*.jpeg')
    imgs.extend(glob.glob(dirname + '/*.png'))
    imgs.extend(glob.glob(dirname + '/*.jpg'))
    for i in imgs:
        flag = True
        for xml in xmls:
            file_name = re.search("label\\\(.+)\.xml", xml)
            file_name = (file_name.group(1))
            if file_name in i:
                flag = False
                break
        if flag:
            print(i)
            os.remove(i)
dirname = 'E:/标注汇总/xiaohan/xiaohan-5-16'
dirs=glob.glob(dirname+"/*")
for d in dirs:
    delete_file(d)
