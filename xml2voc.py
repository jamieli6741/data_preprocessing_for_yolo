import os
import sys
import xml.etree.ElementTree as ET
import shutil
from collections import defaultdict

classes = ['ambiguous_red_stop', 'ambiguous_yellow_warning', 'ambiguous_green_go', 'arrow_red_stop',
           'arrow_yellow_warning',
           'arrow_green_go', 'arrow_red_right', 'arrow_yellow_right', 'arrow_green_right', 'arrow_red_straight',
           'arrow_yellow_ straight',
           'arrow_green_ straight', 'bike_red_stop', 'bike_yellow_warning', 'bike_green_go', 'circle_red_stop',
           'circle_yellow_warning',
           'circle_green_go', 'pedstrain_red_stop', 'pedstrain_green_go', 'number_red_stop', 'number_yellow_warning',
           'number_green_go',
           'red_slow', 'yellow_slow', 'green_slow', 'strip_red_stop', 'strip_yellow_warning', 'strip_green_go',
           'traffic_light', 'U-turn_red_stop',
           'U-turn_green_go', 'U-turn_yellow_warning']


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, annotations_dir, labels_dir, d):
    in_file = open(os.path.join(annotations_dir, '%s.xml' % (image_id)))
    out_file = open(os.path.join(labels_dir, '%s.txt' % (image_id)), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls) + 7
        d[cls_id] += 1
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def make_label(path, label_dir, image_dir, d):
    if os.path.exists(label_dir) is not True:
        os.makedirs(label_dir)
    if os.path.exists(image_dir) is not True:
        os.makedirs(image_dir)
    p_list = os.listdir(path)
    for item in p_list:
        new_p = os.path.join(path, item)
        if os.path.isdir(new_p) is True:
            make_label(new_p, label_dir, image_dir, d)
        else:
            if item[-4:] == '.xml':
                continue
            image_id = item[:-4]
            img_path = new_p
            print(img_path)
            lbl_path = os.path.join(path, image_id + '.xml')
            dest_lbl_path = os.path.join('./data_voc', image_id + '.xml')
            if os.path.exists(lbl_path) is not True:
                continue
            dest_img_path = os.path.join(image_dir, item)
            # dest_lbl_path = ''
            convert_annotation(image_id, path, label_dir, d)
            shutil.copy(img_path, dest_img_path)
            shutil.copy(lbl_path, dest_lbl_path)
    return


if __name__ == '__main__':
    d = defaultdict(int)
    cwd = os.getcwd()
    new_label_dir = './data_voc/label'
    new_image_dir = './data_voc/images'
    dir_list = os.listdir(cwd)
    path = './data_xml'

    for direc in dir_list:
        p = os.path.join(cwd, direc)
        if os.path.isdir(p) is not True:
            continue
        make_label(p, new_label_dir, new_image_dir, d)
    make_label(path, new_label_dir, new_image_dir, d)
    for key, value in d.items():
        print(key, ': ', value)
