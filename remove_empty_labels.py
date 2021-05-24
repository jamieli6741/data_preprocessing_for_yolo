#!/usr/bin/python

import os
from pathlib import Path

"""
Remove empty label files in 'labels' dir and the corresponding image files in 'images' dir.

Dataset structure is as follow:
dataset_path
        |----dataset1
                |----images
                |----labels
        |----dataset2
                |----images
                |----labels

"""

def remove_empty_files(path):
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    if dirs:
        for i in dirs:
            remove_empty_files(os.path.join(path, i))

    label_files = [os.path.join(path,i) for i in lsdir if (os.path.isfile(os.path.join(path,i)) and i.endswith('.txt'))]
    for label in label_files:
        if os.path.getsize(label) == 0:
            print("remove empty label file ", label)
            os.remove(label)
            image_tmp = str(Path(label).parent.parent)+'/images/'+ str(Path(label).stem) + '.jpg'
            image = image_tmp if os.path.isfile(image_tmp) else str(Path(label).parent.parent)+'/images/'+ str(Path(label).stem) + '.png'
            if os.path.isfile(image):
                print("remove corresponding image file ", image)
                os.remove(image)
                print('-'*100)


if __name__ == '__main__':
    dataset_path = "/media/liyq/Storage/dataset/rubbish_v3/test_split/"
    remove_empty_files(dataset_path)
