from ultralytics import YOLO
import multiprocessing


def main():
    model = YOLO("yolov8n.yaml")
    model.train(
        data="data.yaml",
        mode="detect",
        epochs=5,
        imgsz=800,
        model="yolov8n.pt",
        device="0",
    )


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
