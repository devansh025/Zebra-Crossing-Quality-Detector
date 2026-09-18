import numpy as np
from core import quality_analysis


def test_calculate_visibility_blank():
    blank = np.zeros((100, 100), dtype=np.uint8)
    visibility = quality_analysis.calculate_visibility(blank)
    assert visibility == 0.0


def test_calculate_visibility_full():
    full = np.full((100, 100), 255, dtype=np.uint8)
    visibility = quality_analysis.calculate_visibility(full)
    assert visibility == 1.0


def test_calculate_continuity_empty():
    continuity = quality_analysis.calculate_continuity([])
    assert continuity == 0.0


def test_calculate_continuity_good_stripes():
    stripe_boxes = [(0, 0, 10, 10, 100), (0, 0, 10, 10, 100)]
    continuity = quality_analysis.calculate_continuity(stripe_boxes)
    assert continuity == 1.0


def test_calculate_count_ratio_capped():
    ratio = quality_analysis.calculate_count_ratio(10)
    assert ratio == 1.0


def test_calculate_quality_score_range():
    score = quality_analysis.calculate_quality_score(1.0, 1.0, 1.0, 1.0)
    assert score == 100

    score_zero = quality_analysis.calculate_quality_score(0.0, 0.0, 0.0, 0.0)
    assert score_zero == 0


def test_classify_condition_not_detected():
    condition = quality_analysis.classify_condition(False, 0)
    assert condition == "NOT DETECTED"


def test_classify_condition_clear():
    condition = quality_analysis.classify_condition(True, 80)
    assert condition == "CLEAR"


def test_classify_condition_faded():
    condition = quality_analysis.classify_condition(True, 60)
    assert condition == "FADED"


def test_classify_condition_damaged():
    condition = quality_analysis.classify_condition(True, 20)
    assert condition == "DAMAGED / PARTIALLY MISSING"
