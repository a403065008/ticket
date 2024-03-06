from ultralytics import YOLO
import multiprocessing
import cv2


def main():
    # model = YOLO("yolov8n.yaml")  # build a new model from scratch
    model = YOLO("yolov8m.pt")
    # results= model.predict(source="0",show=True)
    # results = model.predict("test/images/LINE_ALBUM_-_230705_87_jpg.rf.628aaf938d7ba9af6014eb2baa7e82ee.jpg")[0]  # predict on an image

    results = model(
        "train/images/LINE_ALBUM_-_230705_120_jpg.rf.fe66735fa23e3e598f98e3bdd30cd988.jpg"
    )  # predict on an image
    res_plotted = results[0].plot()
    # 可视化并显示辨识结果
    cv2.imshow("Results", res_plotted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
