"""
划分test、train数据集，原始文件目录结构如下
dataset_path/
|-- dataset1/
    |-- images/
    |   |-- image1.png
    |
    |-- labels/
    |   |-- label1.txt
|-- dataset2/
    |-- images/
    |   |-- image1.png
    |
    |-- labels/
    |   |-- label1.txt
"""

import os, random, shutil
from tqdm import tqdm
from pathlib import Path


def splitDataset(imgDir, lblDir,tarDir_test, tarDir_train, rate):
    tarDir_img_test = Path(tarDir_test) / image_name
    tarDir_lbl_test = Path(tarDir_test) / label_name
    tarDir_img_train = Path(tarDir_train) / image_name
    tarDir_lbl_train = Path(tarDir_train) / label_name
    paths = [tarDir_img_test, tarDir_lbl_test, tarDir_img_train, tarDir_lbl_train]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    pathDir = [p for p in imgDir.iterdir()]  # 取图片的原始路径
    filenumber = len(pathDir)
    picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
    sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片

    print("Making test dataset ...")
    for file in tqdm(sample):
        lbl_file = file.stem + label_suffix
        shutil.copy2(file, tarDir_img_test / file.name)
        shutil.copy2(lblDir / lbl_file, tarDir_lbl_test / lbl_file)

    print("Making train dataset ...")
    for file in tqdm(pathDir):
        if file not in sample:
            lbl_file = file.stem + label_suffix
            shutil.copy2(file, tarDir_img_train / file.name)
            shutil.copy2(lblDir / lbl_file, tarDir_lbl_train / lbl_file)
    return


if __name__ == '__main__':
    dataset_path = "/media/liyq/Storage/dataset/traffic_light_dataset/tflight_detection/test/test_night"
    dir_path = Path(dataset_path)
    rate = 0.1  # 自定义抽取测试图片的比例

    image_name = 'images'
    label_name = 'labels'
    label_suffix = '.txt'

    TarDir_test = str(dir_path) + '_split/test'
    TarDir_train = str(dir_path) + '_split/train'

    dirs = [d for d in dir_path.iterdir()]
    for dir in dirs:
        imageDir = dir / image_name
        labelDir = dir / label_name
        print()
        print("Start splitting dataset %s ..." % dir)
        splitDataset(imageDir, labelDir, TarDir_test, TarDir_train, rate)

















