import glob
import os
import re
import shutil
import xml.etree.ElementTree as ET
import threadpool
from PIL import Image

from compare_similar import DHash
from xml_tools import get_filename, get_filename_label

img_type = ['.JPEG', '.png', '.jpg', '.jpeg', '.JPG', '.PNG']

def delete_file(dirname):
    xmls = os.listdir(dirname + '/label')
    labels_name = []
    # xmls = glob.glob(dirname + '/*.xml')
    imgs = os.listdir(dirname)
    for xml in xmls:
        inputfile = ET.parse(dirname + '/label/' + xml)
        root = inputfile.getroot()
        label = get_filename(root)
        labels_name.append(label)
    for i in imgs:
        try:
            if i not in labels_name:
                os.remove(dirname + '/' + i)
                print(i)
        except Exception as e:
            print(e)
            print(i)
            pass

# dirname = 'E:/标注汇总v1/songyi/songyi-5.20-5.22/2019.5.22'
# dirs=glob.glob(dirname+"/*")
# for d in dirs:
#     delete_file(d)
def move_to_label(dirname):
    files = os.listdir(dirname)
    for file in files:
        try:
            path = dirname + '/' + file
            if os.path.splitext(path)[-1] in img_type:
                is_not_exist_mkdir(dirname + '/label')
                is_not_exist_mkdir(dirname + '/img')

                shutil.move(path, dirname + '/img')

            if file.endswith('.xml'):
                shutil.move(path, dirname + '/label')
        except:
            print(file)
            pass


def is_not_exist_mkdir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def move_to_one_dir(dirname):
    dirname1=glob.glob(dirname+"/*")
    for d1 in dirname1:
        dirname2 = glob.glob(d1+"/new" + "/*")
        for d2 in dirname2:
            try:
                print(d2)
                shutil.copytree(d2,'E:\标注汇总v2\DODW_v2/'+d2.split('\\')[-1])
            except Exception as e :
                print(e)
                pass
def contrance_img2dir(dirname):
    similar=0
    dirs = os.listdir(dirname)
    for d in dirs:
        d=''
        if os.path.isdir(dirname + d) and not d == 'new':
            imgs_path = dirname + d + "/img/"
            labels_path = dirname + d + "/label/"
            xmls_arr = os.listdir(labels_path)
            for xml_p in xmls_arr:
                if xml_p.endswith('xml'):
                    try:
                        # 便利xml，拿到文件名稱和label
                        xml_path = labels_path + xml_p
                        inputfile = ET.parse(xml_path)
                        root = inputfile.getroot()
                        img_name, label_name = get_filename_label(root)
                        if label_name == '':
                            print('label是空的')
                            return
                        img_path = imgs_path + img_name
                        # imagenet有点文件名沒有后缀
                        if not os.path.exists(img_path):
                            img_path = img_path + ".JPEG"
                            print(img_path + ",imagenet图")
                        if os.path.exists(img_path):
                            # 根據label移動到新的文件夾中-test
                            img_type = os.path.splitext(img_path)[-1]
                            img = Image.open(img_path)
                            hash = DHash.calculate_hash(img)
                            new_img_name = hash + img_type
                            new_xml_name = hash + '.xml'
                            is_not_exist_mkdir(dirname + "new/")
                            new_dirname = dirname + "new/" + label_name
                            new_imgs_path = new_dirname + "/img/"
                            new_labels_path = new_dirname + "/label/"
                            is_not_exist_mkdir(new_dirname)
                            is_not_exist_mkdir(new_imgs_path)
                            is_not_exist_mkdir(new_labels_path)
                            # 重名了，就不移動
                            if os.path.exists(img_path):
                                if os.path.exists(new_imgs_path + new_img_name):
                                    # print("重合圖source：" + new_imgs_path + new_img_name)
                                    # print("重合圖:" + img_path)
                                    similar += 1

                                else:
                                    shutil.move(xml_path, new_labels_path + new_xml_name)
                                    shutil.move(img_path, new_imgs_path + new_img_name)

                            else:
                                print("图片不存在" + img_path)
                                # else:
                                #     os.remove()
                    except Exception as e:
                        print(e)
                        continue
                        # pool = threadpool.ThreadPool(1)
                        # requests = threadpool.makeRequests(copy_img, xmls_arr)
                        # [pool.putRequest(req) for req in requests]
                        # pool.wait()

    print("重复：%s"%similar)
if __name__ == '__main__':
    # 把图片和标签分到img和laebl里
    dirname = 'E:\标注汇总v2\chenwenhan\FanChuan'
    dirs = glob.glob(dirname + "/*")
    # print(dirs)
    # for d in dirs:
    #     move_to_label(d)
    contrance_img2dir(dirname + '/')
    #
    # contrance_img2dir('E:\标注汇总v2\songyi\斧头')