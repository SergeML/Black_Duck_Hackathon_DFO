import cv2
import numpy as np
from typing import List, Tuple
from ultralytics import YOLO
from datetime import datetime


def get_frames(video_path: str, frame_rate: int) -> List[Tuple[np.ndarray, float]]:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frame_rate)

    saved_frames = []
    cnt = 0
    print(datetime.now().strftime("%H:%M:%S"), ' - start read frames')
    while cap.isOpened():

        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if cnt % interval == 0:
            timecode = cnt / fps
            saved_frames.append((frame, timecode))

        cnt += 1

    cap.release()

    return saved_frames


def inference(video_path: str, model: YOLO, callback=None):
    print(datetime.now().strftime("%H:%M:%S"), ' - start inference file:', video_path)
    timecodes_and_preds = []

    frames_and_timecodes = get_frames(video_path, 0.5)

    n = len(frames_and_timecodes)

    for i, (frame, timecode) in enumerate(frames_and_timecodes):
        pred = model(frame)[0].probs.top1
        timecodes_and_preds.append((timecode, pred))
        if callback:
            callback(i, n)

    return timecodes_and_preds