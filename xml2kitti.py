from magic.data import ImgDataset, ConcatDataset
import xml.etree.ElementTree as ET
import os


def get_img_id(path):
    ids = []
    files = os.listdir(path)
    for file in files:
        if file[-4:] == '.xml':
            id = file[:-4]
            ids.append(id)
    return sorted(ids)


def get_label(img_id, annotations_dir, labels_dir):
    in_file = open(os.path.join(annotations_dir, '%s.xml' % (img_id)))
    out_file = open(os.path.join(labels_dir, '%s.txt' % (img_id)), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        cls_name = obj.find('name').text.strip().lower()
        xml_box = obj.find('bndbox')
        xmin = xml_box.find('xmin').text
        ymin = xml_box.find('ymin').text
        xmax = xml_box.find('xmax').text
        ymax = xml_box.find('ymax').text

        # 类别 截断 遮挡 观察角度 xmin ymin xma ymax 高 宽 长 cx cy cz yaw
        out_file.write(cls_name + '\t' + '0\t'*3 +
                       xmin + '\t' + ymin + '\t' + xmax + '\t' + ymax + '\t' +
                       '0\t'*7 + '\n')


if __name__ == '__main__':
    anno_path = '/home/liam/Desktop/yolov3_project/data_added_1103/data_1103/xml'
    label_path = '/home/liam/Desktop/yolov3_project/kitti_format/data_1103/label'
    ids = get_img_id(anno_path)
    for id in ids:
        get_label(id, anno_path, label_path)


