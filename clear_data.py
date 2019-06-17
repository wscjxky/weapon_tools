import os
import shutil
import glob
import re

from PIL import Image

from compare_similar import DHash

file_list = []


def walk_static_dir1(dirPath):
    if not os.path.isdir(dirPath):
        return
    files = os.listdir(dirPath)
    try:
        for file in files:
            filePath = os.path.join(dirPath, file)
            if os.path.isfile(filePath):
                if filePath.endswith('g'):
                    print(filePath)
                else :
                    shutil.rmtree(filePath)
            elif os.path.isdir(filePath):
                walk_static_dir1(filePath)
    except Exception as e:
        raise e

img_type = ['png', 'jpg', 'jpeg', 'JPG', 'PNG','JPEG']

def compare_distance(dirname):
    count = 0
    with open('D:\pycharmproject\weapon_tools\DODW_arguement\DODW_distance.txt', 'r')as f:
        lines = f.readlines()
        exist_arr = [i.strip('\n') for i in lines]

    for roots, dirs, files in os.walk(dirname):
        for file in files:
            path = roots + os.sep + file
            if file[-3:] in img_type or file[-4:] in img_type:
                try:
                    if count % 500 == 0:
                        print(count)
                    count += 1
                    image = Image.open(path)
                    hash = DHash.calculate_hash(image)
                    if hash in exist_arr:
                        print('del'+path)
                        os.remove(path)
                    else:
                        exist_arr.append(hash)

                except OSError as e:
                    print(e)
                    try:
                        os.remove(path)
                    except:
                        pass
                except Exception as e:
                    print(e)
            else:
                print(path)
                os.remove(path)
                    #             pass
            #             # os.remove(path)
    # exist_arr=set(exist_arr)
    # exist_arr=list(exist_arr)
    # print(exist_arr[0])
    # with open('D:\pycharmproject\weapon_tools\DODW_arguement\DODW_distance.txt','w')as f:
    #     for e in exist_arr:
    #         f.write(e+'\n')
    #
# print(gen_redis_distance('D:\pycharmproject\download_images'))
print(compare_distance('D:\pycharmproject\download_images\未分配'))