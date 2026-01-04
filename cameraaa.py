import cv2
import numpy as np

def get_fake_frame(label: str):
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.putText(img, label, (70, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)
    return img
