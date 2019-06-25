import os


def is_xml(file_name):
    img_type = ['.xml']
    if os.path.splitext(file_name)[-1] in img_type:
        return True
    return False


def is_img(file_name):
    img_type = ['.JPEG', '.png', '.jpg', '.jpeg', '.JPG', '.PNG']
    if os.path.splitext(file_name)[-1] in img_type:
        return True
    return False


def crate_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
