import cv2
import numpy as np

MIN_STRIPE_AREA = 150
MIN_ASPECT_RATIO = 1.5


def find_stripe_contours(cleaned_image):
    contours, _ = cv2.findContours(cleaned_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    stripe_boxes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_STRIPE_AREA:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        if h == 0:
            continue

        aspect_ratio = w / float(h)
        if aspect_ratio >= MIN_ASPECT_RATIO or (h / float(w) if w > 0 else 0) >= MIN_ASPECT_RATIO:
            stripe_boxes.append((x, y, w, h, area))

    return stripe_boxes


def count_horizontal_lines(lines):
    if lines is None:
        return 0

    horizontal_count = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 == 0:
            continue
        slope = abs((y2 - y1) / float(x2 - x1))
        if slope < 0.3:
            horizontal_count += 1

    return horizontal_count


def is_crossing_detected(stripe_boxes, hough_line_count):
    return len(stripe_boxes) >= 2 or hough_line_count >= 3


def build_overlay(original_image, stripe_boxes, roi_top):
    overlay = original_image.copy()

    for (x, y, w, h, area) in stripe_boxes:
        cv2.rectangle(
            overlay,
            (x, y + roi_top),
            (x + w, y + h + roi_top),
            (0, 255, 0),
            2,
        )

    return overlay
