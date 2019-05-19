class DHash(object):
    @staticmethod
    def calculate_hash(image):
        """
        计算图片的dHash值
        :param image: PIL.Image
        :return: dHash值,string类型
        """
        difference = DHash.__difference(image)
        # 转化为16进制(每个差值为一个bit,每8bit转为一个16进制)
        decimal_value = 0
        hash_string = ""
        for index, value in enumerate(difference):
            if value:  # value为0, 不用计算, 程序优化
                decimal_value += value * (2 ** (index % 8))
            if index % 8 == 7:  # 每8位的结束
                hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f
                decimal_value = 0
        return hash_string

    @staticmethod
    def hamming_distance(first, second):
        """
        计算两张图片的汉明距离(基于dHash算法)
        :param first: Image或者dHash值(str)
        :param second: Image或者dHash值(str)
        :return: hamming distance. 值越大,说明两张图片差别越大,反之,则说明越相似
        """
        # A. dHash值计算汉明距离
        if isinstance(first, str):
            return DHash.__hamming_distance_with_hash(first, second)

        # B. image计算汉明距离
        hamming_distance = 0
        image1_difference = DHash.__difference(first)
        image2_difference = DHash.__difference(second)
        for index, img1_pix in enumerate(image1_difference):
            img2_pix = image2_difference[index]
            if img1_pix != img2_pix:
                hamming_distance += 1
        return hamming_distance

    @staticmethod
    def __difference(image):
        """
        *Private method*
        计算image的像素差值
        :param image: PIL.Image
        :return: 差值数组。0、1组成
        """
        resize_width = 9
        resize_height = 8
        # 1. resize to (9,8)
        smaller_image = image.resize((resize_width, resize_height))
        # 2. 灰度化 Grayscale
        grayscale_image = smaller_image.convert("L")
        # 3. 比较相邻像素
        pixels = list(grayscale_image.getdata())
        difference = []
        for row in range(resize_height):
            row_start_index = row * resize_width
            for col in range(resize_width - 1):
                left_pixel_index = row_start_index + col
                difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
        return difference

    @staticmethod
    def __hamming_distance_with_hash(dhash1, dhash2):
        """
        *Private method*
        根据dHash值计算hamming distance
        :param dhash1: str
        :param dhash2: str
        :return: 汉明距离(int)
        """
        difference = (int(dhash1, 16)) ^ (int(dhash2, 16))
        return bin(difference).count("1")


import PIL.Image as Image
import os
import glob

dis_txt = 'daer_data.txt'


def gen_files_distance(dirname):
    with open(dis_txt, 'w') as f_w:
        for roots, dirs, files in os.walk(dirname):
            for file in files:
                path = roots + os.sep + file
                try:
                    if path.endswith('.jpeg') or path.endswith('.png') or path.endswith('.jpg'):
                        image = Image.open(path)
                        hash = DHash.calculate_hash(image)
                        f_w.write("%s,%s\n" % (path, hash))
                except Exception as e:
                    print(e)
                    os.remove(path)
                    pass


def cal_files_distance(source_filename,target_filename):
    count = 0
    with open(source_filename, 'r')as fs_r:
        with open(target_filename, 'r')as ft_r:
            ls_r = fs_r.readlines()
            lt_r=ft_r.readlines()
            for s in ls_r:
                for t in lt_r:
                    filename_s=s.split(',')[0]
                    filename_s_hash=s.split(',')[1]
                    filename_t=t.split(',')[0]
                    filename_t_hash=t.split(',')[1]
                    # try:
                    #     distance = DHash.hamming_distance(filename_s_hash, filename_t_hash)
                    # except:
                    #     pass
                    # if distance == 0:
                    if filename_s_hash==filename_t_hash:
                        try:
                            print(filename_s)
                            print(filename_t)
                            os.remove(filename_t)
                        except:
                            print(filename_t+'e')
                            pass

    print(count)

def compare_self_distance(filename):
    count = 0
    with open(filename, 'r')as fs_r:
            ls_r = fs_r.readlines()
            for index,s in enumerate(ls_r):
                for t in ls_r[index+1:]:
                    filename_s = s.split(',')[0]
                    filename_s_hash = s.split(',')[1]
                    filename_t = t.split(',')[0]
                    filename_t_hash = t.split(',')[1]
                    # try:
                    #     distance = DHash.hamming_distance(filename_s_hash, filename_t_hash)
                    # except:
                    #     pass
                    # if distance == 0:
                    if filename_s_hash == filename_t_hash:
                        try:
                            print(filename_s)
                            print(filename_t)
                            os.remove(filename_t)
                        except:
                            print(filename_t + 'e')
                            pass


gen_files_distance('E:\daer_data')
# source_txt='already_files_dis.txt'
# target_txt='daer_data.txt'
# cal_files_distance(source_txt,target_txt)
# compare_self_distance(target_txt)
