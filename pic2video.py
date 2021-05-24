import cv2, os
from tqdm import tqdm


def make_video(root_path, dir_name):
    dir_path = os.path.join(root_path, dir_name)
    files = sorted(os.listdir(dir_path))
    image_path = os.path.join(dir_path, files[0])
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    fps = 4
    print("making video %s"%dir_name)
    video = cv2.VideoWriter('%s/%s.mp4' % (root_path, dir_name), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)) #创建视频流对象-格式一
    #video = cv2.VideoWriter('ss.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width,height)) #创建视频流对象-格式二

    for i in tqdm(range(len(files))):
        # file = files[len(files)-i-1]
        file = files[i]
        file_path = os.path.join(dir_path, file)
        image = cv2.imread(file_path)
        video.write(image)


def main():
    multiple = True
    # root_path下多个文件夹批量生成视频
    if multiple:
        root_path = "/home/liyq/Desktop/putong"
        dirs = os.listdir(root_path)
        for dir in dirs:
            make_video(root_path, dir)
    else:
        root_path = "/home/liyq/Desktop/zkhy"
        dir = "03"
        make_video(root_path, dir)


if __name__ == '__main__':
    main()

"""
参数1 即将保存的文件路径
参数2 VideoWriter_fourcc为视频编解码器
    fourcc意为四字符代码（Four-Character Codes），顾名思义，该编码由四个字符组成,下面是VideoWriter_fourcc对象一些常用的参数,注意：字符顺序不能弄混
    cv2.VideoWriter_fourcc('I', '4', '2', '0'),该参数是YUV编码类型，文件名后缀为.avi 
    cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'),该参数是MPEG-1编码类型，文件名后缀为.avi 
    cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),该参数是MPEG-4编码类型，文件名后缀为.avi 
    cv2.VideoWriter_fourcc('T', 'H', 'E', 'O'),该参数是Ogg Vorbis,文件名后缀为.ogv 
    cv2.VideoWriter_fourcc('F', 'L', 'V', '1'),该参数是Flash视频，文件名后缀为.flv
    cv2.VideoWriter_fourcc('m', 'p', '4', 'v')    文件名后缀为.mp4
参数3 为帧播放速率
参数4 (width,height)为视频帧大小

"""




