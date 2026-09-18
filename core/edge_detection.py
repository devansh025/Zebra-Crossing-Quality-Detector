import cv2
import numpy as np


def detect_edges(gray_image, low_threshold=50, high_threshold=150):
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)
    return edges


def detect_hough_lines(edge_image, threshold=40, min_line_length=30, max_line_gap=10):
    lines = cv2.HoughLinesP(
        edge_image,
        1,
        np.pi / 180,
        threshold=threshold,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap,
    )
    return lines


def edge_density(edge_image):
    total_pixels = edge_image.shape[0] * edge_image.shape[1]
    if total_pixels == 0:
        return 0.0
    edge_pixels = np.count_nonzero(edge_image)
    return edge_pixels / total_pixels
