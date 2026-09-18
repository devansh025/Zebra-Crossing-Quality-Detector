import os
import numpy as np
import cv2
from utils import validation


def make_temp_image(path, width=200, height=200):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.imwrite(path, image)


def test_file_does_not_exist():
    image, message = validation.load_and_validate_image("does_not_exist.jpg")
    assert image is None
    assert message == "File does not exist"


def test_invalid_extension(tmp_path):
    file_path = os.path.join(tmp_path, "notimage.txt")
    with open(file_path, "w") as f:
        f.write("hello")

    image, message = validation.load_and_validate_image(file_path)
    assert image is None
    assert message == "Unsupported file type"


def test_valid_image(tmp_path):
    file_path = os.path.join(tmp_path, "test.jpg")
    make_temp_image(file_path)

    image, message = validation.load_and_validate_image(file_path)
    assert image is not None
    assert message == "OK"


def test_small_image(tmp_path):
    file_path = os.path.join(tmp_path, "small.jpg")
    make_temp_image(file_path, width=20, height=20)

    image, message = validation.load_and_validate_image(file_path)
    assert image is None
    assert message == "Image resolution too small"
