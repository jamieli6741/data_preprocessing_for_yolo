import os
import xml.etree.ElementTree as ET
from tqdm import tqdm


def load_classes(path):
    fp = open(path, 'r')
    names = fp.read().split('\n')[:-1]
    return names


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x*dw, y*dh, w*dw, h*dh)


def convert_annotation(image_id, annotations_dir, labels_dir, classes):
    in_file = open(os.path.join(annotations_dir, '%s.xml' % (image_id)))
    out_file = open(os.path.join(labels_dir, '%s.txt' % (image_id)), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    count = 0

    for obj in root.iter('object'):
        cls_id = obj.find('name').text
        if cls_id in classes:
            count += 1
            cls_id = classes.index(cls_id)  # convert class name from string to int
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        else:
            assert Exception("class %s in %s is not in the index, please check the class name!" % (cls_id, in_file))
    if count == 0: # if there is no object in image, delete .txt file
        os.remove(os.path.join(labels_dir, '%s.txt' % (image_id)))


def make_label(path, label_dir, classes):
    if os.path.exists(label_dir) is not True:
        os.makedirs(label_dir)
    p_list = os.listdir(path)
    for item in tqdm(p_list):
        new_p = os.path.join(path, item)
        if os.path.isdir(new_p) is True:
            make_label(new_p, label_dir, classes)
        else:
            if item[-4:] == '.xml':
                filename_stem = item[:-4]
                convert_annotation(filename_stem, path, label_dir, classes)


def xml2yolo(path, classes):
    print("start converting labels ...")
    annotation_path = path + '/annotations'
    new_label_path = path + '/labels'  # save new labels into 'labels' dir under path
    make_label(annotation_path, new_label_path, classes)


if __name__ == '__main__':
    classes = ['traffic_light']
    xml2yolo(path="/media/liyq/Storage/dataset/rubbish/zkhy_for_classify", classes=classes)
