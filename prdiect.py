from ultralytics import YOLO
import multiprocessing
import cv2
import numpy as np


def main():
    # model = YOLO("yolov8n.yaml")  # build a new model from scratch
    model = YOLO("yolov8n.pt")
    model = YOLO("best.pt")  # load a custom model
    results = model.predict(source="datasets/test/images/163.png", show=True)
    # results = model.predict("test/images/LINE_ALBUM_-_230705_87_jpg.rf.628aaf938d7ba9af6014eb2baa7e82ee.jpg")[0]  # predict on an image
    # 假设你的输出结果存储在变量 result 中

    names = model.names
    list = []
    for i in results[0].numpy():
        list.append([i.boxes[0].boxes[0][0], i.boxes[0].boxes[0][5]])

    # 按照每个子列表的第一个元素进行排序
    sorted_list = sorted(list, key=lambda x: x[0])
    sorted_second_elements = [item[1] for item in sorted_list]
    # 打印排序后的列表

    for i in sorted_second_elements:
        print(names[int(i)], end="")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
