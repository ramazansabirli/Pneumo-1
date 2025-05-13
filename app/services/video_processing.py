import cv2
import numpy as np
from typing import List


def extract_video_features(video_path: str) -> List[float]:
    """
    Toraks BT videoları üzerinden klinik-özgül görüntü işleme:
    - Ortalama parlaklık ve kontrast
    - Pnömotoraks yüzdesi (siyah alan segmentasyonu)
    - Mediastinal shift tespiti (orta hattın kayması)
    - Costophrenic açı sönümü (alt akciğer bölgesi analizi)
    - Akciğer kenar netliği (kenar tespiti)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Video açılamadı: {video_path}")

    brightness, contrast, pt_percent, shift_values = [], [], [], []
    blunt_scores, edge_sharpness = [], []

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (256, 256))

        brightness.append(np.mean(resized))
        contrast.append(np.std(resized))

        # --- Pnömotoraks segmentasyonu (siyah alan yüzdesi) ---
        thresh = cv2.threshold(resized, 30, 255, cv2.THRESH_BINARY_INV)[1]
        black_ratio = np.sum(thresh == 255) / (256 * 256)
        pt_percent.append(black_ratio * 100)

        # --- Mediastinal shift (orta yoğunluk dağılımı) ---
        mid_col = np.sum(resized[:, 120:136])  # orta bölge yoğunluğu
        left_col = np.sum(resized[:, :120])
        right_col = np.sum(resized[:, 136:])
        shift_score = (right_col - left_col) / (right_col + left_col + 1e-5)
        shift_values.append(shift_score)

        # --- Costophrenic açı sönümü (alt alan kontrastı) ---
        lower_area = resized[192:, :]
        blunt_score = np.std(lower_area)
        blunt_scores.append(blunt_score)

        # --- Kenar netliği (akciğer sınırı gradient gücü) ---
        edges = cv2.Canny(resized, 50, 150)
        edge_sharpness.append(np.mean(edges))

    cap.release()

    # Ortalama tüm karelerden
    if frame_count == 0:
        return [0.0] * 6

    return [
        np.mean(brightness),
        np.mean(contrast),
        np.mean(pt_percent),
        np.mean(shift_values),
        np.mean(blunt_scores),
        np.mean(edge_sharpness)
    ]
