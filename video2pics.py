import cv2
import argparse
import os
from pathlib import Path

# video_path = "/home/liyq/下载/center_down_1.mp4"
video_path = "/data/liyq/mine_tunnel/center_down_1.mp4"
vp = Path(video_path)

out_path = str(vp.parent) + '_2pics_5fps'
os.makedirs(out_path, exist_ok=True)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--videoPath", default=video_path, help="path to input video")
ap.add_argument("-o", "--outputPath", default=out_path, help="path to output frames")

args = vars(ap.parse_args())

# 初始化,并读取第一帧
# rval表示是否成功获取帧
# frame是捕获到的图像
vc = cv2.VideoCapture(args["videoPath"])
rval, frame = vc.read()

# 获取视频fps
fps = vc.get(cv2.CAP_PROP_FPS)
# 获取视频总帧数
frame_all = vc.get(cv2.CAP_PROP_FRAME_COUNT)
print("[INFO] 视频FPS: {}".format(fps))
print("[INFO] 视频总帧数: {}".format(frame_all))
print("[INFO] 视频时长: {}s".format(frame_all/fps))

outputPath = os.path.sep.join([args["outputPath"]])
if os.path.exists(outputPath) is False:
    print("[INFO] 创建文件夹,用于保存提取的帧")
    os.mkdir(outputPath)

# 每隔多少帧保存一张图片
frame_interval = 100
# 统计当前帧
frame_count = 1
# 保存图片个数初始化（无需修改）
count = 0
# 是否进行直方图均衡
histogram = False

with open('test.txt', 'w') as f:
    while rval:
        rval, frame = vc.read()
        if frame_count % frame_interval == 0:
            numero = '0'*(5-len(str(count)))+str(count)
            filename = os.path.sep.join([outputPath, "{}_{}.jpg".format(str(vp.stem), numero)])
            f.write(filename+'\n')
            # cv2.rotate(frame, cv2.ROTATE_180)  # 画面旋转180度
            cv2.flip(frame,0) # 左右镜像翻转

            if histogram:
                (b, g, r) = cv2.split(frame)  # 通道分解
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # 自适应直方图均衡(限制对比度)
                b = clahe.apply(b)
                g = clahe.apply(g)
                r = clahe.apply(r)
                frame = cv2.merge([b, g, r])  # 通道合成

            cv2.imwrite(filename, frame)
            count += 1
            print("保存图片:{}".format(filename))
        frame_count += 1
# 关闭视频文件
vc.release()
print("[INFO] 总共保存：{}张图片".format(count))
