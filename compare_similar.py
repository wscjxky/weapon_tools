import shutil

import threadpool
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
img_type = ['.JPEG', '.png', '.jpg', '.jpeg', '.JPG', '.PNG']


def gen_files_distance(dirname, filename):
    count = 0
    with open(filename, 'w', encoding='utf8') as f_w:
        for roots, dirs, files in os.walk(dirname):
            if '\\label' in roots:
                continue
            for file in files:
                path = roots + os.sep + file
                try:
                    file_type = os.path.splitext(file)[-1]
                    f_w.write("%s\n" % os.path.splitext(file)[0])
                    if file_type in img_type:
                        xmls = os.listdir(roots + "/../label")
                        # 删除没有标签的图片
                        if file[:-len(file_type)] + '.xml' not in xmls:
                            count += 1
                            print(path)
                            # os.remove(path)
                            # os.remove(file)
                            continue


                except Exception as e:
                    print(e)
                    pass
    print(count)


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
                        redis.sadd("source", hash)
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
                    os.remove(target_filename[:-4] + 'xml')

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


def gen_labels_imgs(dirname):
    xml_files = open("DODW_arguement/DODW_xmls.txt", 'w', encoding='utf8')
    img_files = open("DODW_arguement/DODW_imgs.txt", 'w', encoding='utf8')
    img_distance = open("DODW_arguement/DODW_distance.txt", 'w', encoding='utf8')

    for root, dirs, files in os.walk(dirname):
        for file in files:
            try:
                path = root + '/' + file
                path = path.replace('\\', '/')
                if os.path.splitext(path)[-1] in img_type:
                    img_files.write(path + "\n")
                    img_distance.write("%s\n" % os.path.splitext(file)[0])

                if file.endswith('.xml'):
                    xml_files.write(path + "\n")
            except:
                print(file)
                pass


def is_not_exist_mkdir(dirname):
    try:
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
    except :
        pass

def copy_img(img,xml,label):
    # is_not_exist_mkdir('E:\DODW_v2/' + label)
    # is_not_exist_mkdir('E:\DODW_v2/' + label + '/img/')
    # is_not_exist_mkdir('E:\DODW_v2/' + label + '/label/')
    shutil.copy(img, 'E:\DODW_v2/' + label + '/img/')
    # shutil.copy(xml, 'E:\DODW_v2/' + label + '/label/')
def copy_by_files():
    xml_files = open("DODW_arguement/DODW_xmls.txt", 'r', encoding='utf8')
    img_files = open("DODW_arguement/DODW_imgs.txt", 'r', encoding='utf8')
    img_distance = open("DODW_arguement/DODW_distance.txt", 'r', encoding='utf8')
    imgs = img_files.readlines()
    xmls = xml_files.readlines()
    lenth=len(xmls)
    assert lenth==len(imgs)
    params=[]
    for index, img in enumerate(imgs):
        if index%200==0:
            print(index)
        img = img.strip('\n')
        xml = xmls[index].strip('\n')
        label =img.split('/')[-3]
        if not os.path.isfile(img):
            copy_img(img,xml,label)
        # params.append(((img,xml,label), None))
    # print(params)
    # pool = threadpool.ThreadPool(500)
    # requests = threadpool.makeRequests(copy_img,params)
    # [pool.putRequest(req) for req in requests]
    # pool.wait()
    # img.split('/')[-3]
    # is_not_exist_mkdir('E:\DODW_v2/' + label)
    # is_not_exist_mkdir('E:\DODW_v2/' + label + '/img/')
    # is_not_exist_mkdir('E:\DODW_v2/' + label + '/label/')
    # shutil.copy(img, 'E:\DODW_v2/' + label + '/img/')
    # shutil.copy(xml, 'E:\DODW_v2/' + label + '/label/')


if __name__ == '__main__':
    source_txt = 'DODW_v2_DHASH.txt'
    target_txt = 'no_already_data.txt'
    target_txt = 'a.txt'

    # gen_labels_imgs('E:\标注汇总v2')
    # gen_labels_imgs('E:\标注汇总v2')
    gen_files_distance('E:\标注汇总v2', source_txt)
    # copy_by_files()
