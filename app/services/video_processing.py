import cv2
import numpy as np
from typing import List

def extract_video_features(video_path: str) -> List[float]:
    cap = cv2.VideoCapture(video_path)
    frame_features = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_val = np.mean(gray)
        std_val = np.std(gray)
        frame_features.append([mean_val, std_val])

    cap.release()

    if frame_features:
        return np.mean(frame_features, axis=0).tolist()
    return [0.0, 0.0]
