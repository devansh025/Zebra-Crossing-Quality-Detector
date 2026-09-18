import numpy as np
from core import crossing_detection


def make_stripe_mask():
    mask = np.zeros((200, 300), dtype=np.uint8)
    for i in range(0, 200, 40):
        mask[i:i + 20, 20:280] = 255
    return mask


def test_find_stripe_contours_detects_stripes():
    mask = make_stripe_mask()
    stripes = crossing_detection.find_stripe_contours(mask)
    assert len(stripes) > 0


def test_find_stripe_contours_on_blank():
    blank = np.zeros((200, 300), dtype=np.uint8)
    stripes = crossing_detection.find_stripe_contours(blank)
    assert len(stripes) == 0


def test_is_crossing_detected_true():
    stripe_boxes = [(0, 0, 50, 10, 500), (0, 40, 50, 10, 500)]
    assert crossing_detection.is_crossing_detected(stripe_boxes, 0) is True


def test_is_crossing_detected_false():
    assert crossing_detection.is_crossing_detected([], 0) is False


def test_count_horizontal_lines_none():
    count = crossing_detection.count_horizontal_lines(None)
    assert count == 0


def test_build_overlay_shape():
    image = np.zeros((200, 300, 3), dtype=np.uint8)
    stripe_boxes = [(10, 10, 40, 10, 400)]
    overlay = crossing_detection.build_overlay(image, stripe_boxes, roi_top=0)
    assert overlay.shape == image.shape
