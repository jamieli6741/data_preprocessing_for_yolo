# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
from tqdm import tqdm


def count_class_samples(dir, count):
    for file in tqdm(os.listdir(dir)):
        file = os.path.join(dir, file)
        with open(file) as f:
            lines = f.read().splitlines()
            for line in lines:
                label = list(map(float, line.split()))
                count['%d' % int(label[0])] += 1
    return count


if __name__ == '__main__':
    names = ['bicycle', 'bus', 'car', 'cat', 'dog', 'motorbike', 'person', 'truck', 'trash', 'trash_uncleaned']
    nb_class = len(names)

    count_train = {}
    count_valid = {}
    for i in range(nb_class):
        count_train['%d' % i] = 0
        count_valid['%d' % i] = 0

    root_path = "/home/liyq/Works/dataset/rubbish"
    # dirs = os.listdir(root_path)
    dirs = ['trash_select']
    for dir in dirs:
        train_label = root_path + '/' + dir + '/labels'
        print('counting directory %s' % train_label)
        count_train = count_class_samples(train_label, count_train)

    valid_dir = "/home/liyq/Works/dataset/yolo/valid"
    valid_label = valid_dir + '/labels'
    count_valid = count_class_samples(valid_label, count_valid)

    res_train = {}
    res_valid = {}
    for j, name in enumerate(names):
        res_train['%s' % name] = count_train['%d' % j]
        # res_valid['%s' % name] = count_valid['%d' % j]
    print("train dataset: ", res_train)
    # print("valid dataset", res_valid)

    # plot
    y_train = res_train.values()
    fig = plt.figure()
    plt.bar(names, y_train, 0.5, color="green")
    plt.xlabel("Class Name")
    plt.ylabel("Quantities")
    plt.title("Dataset Train")
    plt.savefig("train set.jpg")

    # y_test = res_valid.values()
    # fig = plt.figure()
    # plt.bar(names, y_test, 0.5, color="blue")
    # plt.xlabel("Class Name")
    # plt.ylabel("Quantities")
    # plt.title("Dataset Valid")
    # plt.savefig("valid set.jpg")
    # plt.show()


