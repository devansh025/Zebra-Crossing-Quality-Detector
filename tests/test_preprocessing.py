import numpy as np
from core import preprocessing


def make_sample_image():
    return np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)


def test_convert_to_grayscale():
    image = make_sample_image()
    gray = preprocessing.convert_to_grayscale(image)
    assert len(gray.shape) == 2
    assert gray.shape[0] == image.shape[0]
    assert gray.shape[1] == image.shape[1]


def test_remove_noise():
    image = make_sample_image()
    gray = preprocessing.convert_to_grayscale(image)
    blurred = preprocessing.remove_noise(gray)
    assert blurred.shape == gray.shape


def test_enhance_contrast():
    image = make_sample_image()
    gray = preprocessing.convert_to_grayscale(image)
    enhanced = preprocessing.enhance_contrast(gray)
    assert enhanced.shape == gray.shape


def test_get_roi():
    image = make_sample_image()
    roi, top, bottom = preprocessing.get_roi(image)
    assert roi.shape[0] == bottom - top


def test_preprocess_image_returns_all_keys():
    image = make_sample_image()
    result = preprocessing.preprocess_image(image)
    expected_keys = ["gray", "denoised", "enhanced", "roi", "roi_top", "roi_bottom", "thresh", "cleaned"]
    for key in expected_keys:
        assert key in result
