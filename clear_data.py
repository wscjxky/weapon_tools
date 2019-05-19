import os
import shutil
import glob
import re

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


fs = walk_static_dir1('D:\pycharmproject\weapon\环球军事网')
