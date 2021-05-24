"""
check labeled bounding-box in yolo format: class x_center y_center w h
"""
import cv2, os
import numpy as np
import torch
from pathlib import Path
from tqdm import tqdm


def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    if len(x.shape) > 1:
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    else:
        y[0] = x[0] - x[2] / 2  # top left x
        y[1] = x[1] - x[3] / 2  # top left y
        y[2] = x[0] + x[2] / 2  # bottom right x
        y[3] = x[1] + x[3] / 2  # bottom right y    return y
    return y


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.0007 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    # color = color or [random.randint(0, 255) for _ in range(3)]
    color = [0,255,255]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        tf = 1
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def main():
    save_image = True
    show_image = True
    dataset_path = Path("/media/liyq/Storage/dataset/traffic_light_dataset/tflight_detection/detect/detect_day")
    images_dir = dataset_path / 'images'
    labels_dir = dataset_path / 'labels'
    
    classes = ['traffic_light']

    images = [image for image in images_dir.iterdir()]
    for image in tqdm(images):
        print(image)
        img = cv2.imread(str(image))
        height, width = img.shape[:2]
        label = '%s/%s.txt' % (labels_dir, image.stem)
        data = np.loadtxt(label)
        if len(data.shape) > 1:
            cls, xywhs = data[:,0], data[:,1:]
            xs = xywh2xyxy(xywhs) * [width, height, width, height]
            for x, cl in zip(xs, cls):
                lbl = classes[int(cl)]
                plot_one_box(x, img, label=None)
        else:
            cl, xywh = data[0], data[1:]
            x = xywh2xyxy(xywh) * [width, height, width, height]
            lbl = classes[int(cl)]
            plot_one_box(x, img, label=None)

        if show_image:
            cv2.imshow('image', img)
            k = cv2.waitKey(0)  # waitkey代表读取键盘的输入，括号里的数字代表等待多长时间，单位ms。 0代表一直等待
            if k == 27:  # 键盘上Esc键的键值
                cv2.destroyAllWindows()
                exit()

        if save_image:
            dst_dir = Path("%s_label_check" % dataset_path)
            os.makedirs(dst_dir, exist_ok=True)
            dst_img = dst_dir/image.name
            cv2.imwrite(str(dst_img), img)


if __name__ == '__main__':
    main()