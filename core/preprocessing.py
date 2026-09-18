import cv2
import numpy as np


def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(gray_image):
    return cv2.GaussianBlur(gray_image, (5, 5), 0)


def enhance_contrast(gray_image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray_image)


def get_roi(image, top_ratio=0.45, bottom_ratio=1.0):
    height, width = image.shape[:2]
    top = int(height * top_ratio)
    bottom = int(height * bottom_ratio)
    roi = image[top:bottom, 0:width]
    return roi, top, bottom


def apply_threshold(gray_image):
    _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def apply_morphology(binary_image):
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
    return opened


def preprocess_image(image):
    gray = convert_to_grayscale(image)
    denoised = remove_noise(gray)
    enhanced = enhance_contrast(denoised)
    roi, top, bottom = get_roi(enhanced)
    thresh = apply_threshold(roi)
    cleaned = apply_morphology(thresh)
    return {
        "gray": gray,
        "denoised": denoised,
        "enhanced": enhanced,
        "roi": roi,
        "roi_top": top,
        "roi_bottom": bottom,
        "thresh": thresh,
        "cleaned": cleaned,
    }
