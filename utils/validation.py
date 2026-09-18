import os
import cv2

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")
MIN_WIDTH = 100
MIN_HEIGHT = 100


def is_valid_extension(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in VALID_EXTENSIONS


def file_exists(file_path):
    return os.path.isfile(file_path)


def load_and_validate_image(file_path):
    if not file_exists(file_path):
        return None, "File does not exist"

    if not is_valid_extension(file_path):
        return None, "Unsupported file type"

    image = cv2.imread(file_path)

    if image is None:
        return None, "Could not read image, file may be corrupted"

    height, width = image.shape[:2]
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return None, "Image resolution too small"

    return image, "OK"
