from PIL import ImageFile


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
from redis import StrictRedis, ConnectionPool

pool = ConnectionPool(host='123.56.19.49', password='wscjxky123', port=6379, db=15, decode_responses=True)
redis = StrictRedis(connection_pool=pool)
ImageFile.LOAD_TRUNCATED_IMAGES = True


def gen_files_distance(dirname, filename):
    with open(filename, 'w', encoding='utf8') as f_w:
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
                    # os.remove(path)
                    pass


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
                        redis.sadd("source",hash)
                        # redis.set(key_head + path, hash)
                    except OSError as e:
                        print(e)
                        pass
                        # os.remove(path)


def cal_files_distance(source_filename, target_filename):
    count = 0
    with open(source_filename, 'r', encoding='utf8')as fs_r:
        with open(target_filename, 'r', encoding='utf8')as ft_r:
            ls_r = fs_r.readlines()
            lt_r = ft_r.readlines()
            for s in ls_r:
                for t in lt_r:
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
                        except Exception as e:
                            print(e)
                            pass

    print(count)


def cal_redis_distance(source_filename, target_filename):
    count = 0
    keys_source = redis.keys(source_filename + "*")
    keys_target = redis.keys(target_filename + "*")
    print('add')
    s_hash_arr = redis.mget(keys_source)
    t_hash_arr = redis.mget(keys_target)
    print(s_hash_arr[0])

    for t_index, t_hash in enumerate(t_hash_arr):
        if count % 1000 == 0:
            print(count)
        count += 1
        try:
            find_result = s_hash_arr.index(t_hash)
        except:
            continue
        if find_result:
            try:
                source_filename = (keys_source[find_result])[len('Target_Dhash:'):]
                target_filename = (keys_target[t_index])[len('Target_Dhash:'):]
                # os.remove(target_filename)
                print(source_filename)
                print(target_filename)
                if target_filename[:-4] in img_type:
                    print(target_filename)
                    # 删除相应的xml
                    os.remove(target_filename[:-4]+'xml')

            except Exception as e:
                print(e)
                pass


def compare_self_distance(filename):
    count = 0
    with open(filename, 'r', encoding='utf8')as fs_r:
        ls_r = fs_r.readlines()
        for index, s in enumerate(ls_r):
            for t in ls_r[index + 1:]:
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
                    except Exception as e:
                        print(e)
                        pass


source_txt = 'all_already_data.txt'
target_txt = 'no_already_data.txt'
target_txt='a.txt'
gen_redis_distance('E:\标注汇总v1')
# gen_redis_distance('E:\未标注','Target_Dhash:')
# cal_redis_distance('Source_Dhash:', 'Source_Dhash:')

# source_txt='already_files_dis.txt'
# cal_files_distance(source_txt,target_txt)
# gen_files_distance('D:\pycharmproject\download_images_new',target_txt)
# compare_self_distance(target_txt)
cal_files_distance(source_txt,target_txt)

