import os
import shutil
import glob
import re

from PIL import Image

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

img_type = ['JPEG', 'png', 'jpg', 'jpeg', 'JPG', 'PNG']

def gen_redis_distance(dirname, key_head="Source_Dhash:"):
    count = 0
    for roots, dirs, files in os.walk(dirname):
        for file in files:
            path = roots + os.sep + file
            is_exist = redis.get(key_head + path)
            if is_exist is None:
                if file[-3:] in img_type or file[-4:] in img_type:
                    try:
                        if count % 1000 == 0:
                            print(count)
                        count += 1
                        image = Image.open(path)
                        hash = DHash.calculate_hash(image)
                        redis.set(key_head + path, hash)
                    except OSError as e:
                        print(e)
                        pass
                        # os.remove(path)
