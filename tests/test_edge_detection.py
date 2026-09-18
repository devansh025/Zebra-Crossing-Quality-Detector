import numpy as np
from core import edge_detection


def make_stripe_image():
    image = np.zeros((200, 200), dtype=np.uint8)
    for i in range(0, 200, 40):
        image[i:i + 20, :] = 255
    return image


def test_detect_edges_returns_binary():
    image = make_stripe_image()
    edges = edge_detection.detect_edges(image)
    assert edges.shape == image.shape
    unique_values = set(np.unique(edges))
    assert unique_values.issubset({0, 255})


def test_detect_hough_lines_on_stripes():
    image = make_stripe_image()
    edges = edge_detection.detect_edges(image)
    lines = edge_detection.detect_hough_lines(edges)
    assert lines is not None


def test_detect_hough_lines_on_blank():
    blank = np.zeros((200, 200), dtype=np.uint8)
    lines = edge_detection.detect_hough_lines(blank)
    assert lines is None


def test_edge_density_range():
    image = make_stripe_image()
    edges = edge_detection.detect_edges(image)
    density = edge_detection.edge_density(edges)
    assert 0.0 <= density <= 1.0
