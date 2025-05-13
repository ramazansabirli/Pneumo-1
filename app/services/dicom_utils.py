import pydicom
import numpy as np
import cv2

def dicom_to_image_array(dicom_path):
    dcm = pydicom.dcmread(dicom_path)
    img = dcm.pixel_array
    img = cv2.normalize(img.astype(np.float32), None, 0, 255, cv2.NORM_MINMAX)
    img = img.astype(np.uint8)
    return img
