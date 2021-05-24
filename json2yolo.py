import json
import cv2
import os, shutil
from pathlib import Path
from tqdm import tqdm


def xxyy2xywh(size, box):
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


def convert_json(json_file, img_file):
    contents = json.load(open(json_file, 'r'))
    out_path = '%s/%s.txt' % (new_label_dir, Path(json_file).stem)
    out_file = open(out_path, 'w')
    for item in contents['frames'][0]['objects']:
        if item['category'] in class_names:
            # print(img_file)
            # img = cv2.imread(img_file)
            # size = img.shape[1], img.shape[0]
            size = (1280, 720)
            # tf_color = item['attributes']['trafficLightColor']
            box2d = item['box2d']
            xmin, ymin, xmax, ymax = box2d['x1'], box2d['y1'], box2d['x2'], box2d['y2']
            box = [xmin, xmax, ymin, ymax]
            yolo_box = xxyy2xywh(size, box)
            cls_id = class_names.index(item['category'])
            yolo_label = str(cls_id) + ' ' + ' '.join(str(s) for s in yolo_box) + '\n'
            out_file.write(yolo_label)

    # if os.path.getsize(out_path) == 0:
    #     os.remove(out_path)
    # else:
    # shutil.copy(image_file, "%s/%s" % (new_image_dir, Path(image_file).name))


if __name__ == '__main__':
    class_names = ['traffic light']
    jsons_dir = "/media/liyq/Storage/dataset/traffic_light_dataset/tflight_detection/bdd100k_labels/json_files/train"
    new_label_dir = "/media/liyq/Storage/dataset/daytime_classify/bdd_test_final/bdd_100k_origin/train/labels"
    images_dir = "/media/liyq/Storage/dataset/daytime_classify/bdd_test_final/twilight"
    new_image_dir = "/media/liyq/Storage/dataset/daytime_classify/bdd_test_final/twilight_origin/images"

    os.makedirs(new_label_dir, exist_ok=True)
    os.makedirs(new_image_dir, exist_ok=True)

    json_files = [f for f in Path(jsons_dir).iterdir()]
    for j in tqdm(json_files):
        image_file = "%s/%s.jpg" % (images_dir, j.stem)
        convert_json(str(j), image_file)

