import linecache
import os

import chardet

filename='F:\SogouLab（互联网图片库2.0）\sogoulab\Meta_Data'
def read_in_chunks(filePath, chunk_size=1024 * 1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M
    You can set your own chunk size
    """
    file_object = open(filePath,'rb')
    while True:
        chunk_data = file_object.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data
# for chunk in read_in_chunks(filePath):
#     print(chunk)
#     break
# with open(filePath,"r") as f:
#     for fLine in f:
#         print(fLine)
#
def read_txt():
    f = open(filename,'rb')
    f_w=open('text.txt','w')
    errer_conut=0
    lines_count=0
    while True:
        lines_count+=1
        line = f.readline()
        char_type=chardet.detect(line)
        if char_type['encoding']:
            try:
                line=line.decode(char_type['encoding'])
                # if "开" in line:
                #     print(line)
                f_w.write(line)
            except:
                errer_conut+=1
                pass
            # print(errer_conut)
            print(lines_count)
        if not line:
            break

    # str = linecache.getlines(filename)
    # print(str)
    def tong1():
        with open(filename, 'r') as f:
            num = sum(1 for line in f)
            print('总行数为%s行。' % num)
    tong1()
read_txt()