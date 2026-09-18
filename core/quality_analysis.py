EXPECTED_MIN_STRIPES = 4

VISIBILITY_WEIGHT = 0.40
CONTINUITY_WEIGHT = 0.25
EDGE_STRENGTH_WEIGHT = 0.20
COUNT_WEIGHT = 0.15

CLEAR_THRESHOLD = 75
FADED_THRESHOLD = 45


def calculate_visibility(cleaned_roi):
    total_pixels = cleaned_roi.shape[0] * cleaned_roi.shape[1]
    if total_pixels == 0:
        return 0.0
    white_pixels = int((cleaned_roi > 0).sum())
    visibility = white_pixels / total_pixels
    return min(visibility * 4, 1.0)


def calculate_continuity(stripe_boxes):
    if len(stripe_boxes) == 0:
        return 0.0

    good_stripes = 0
    for (x, y, w, h, area) in stripe_boxes:
        expected_area = w * h
        if expected_area == 0:
            continue
        fill_ratio = area / float(expected_area)
        if fill_ratio > 0.5:
            good_stripes += 1

    return good_stripes / len(stripe_boxes)


def calculate_count_ratio(stripe_count):
    ratio = stripe_count / EXPECTED_MIN_STRIPES
    return min(ratio, 1.0)


def calculate_quality_score(visibility, continuity, edge_strength, count_ratio):
    score = (
        VISIBILITY_WEIGHT * visibility
        + CONTINUITY_WEIGHT * continuity
        + EDGE_STRENGTH_WEIGHT * edge_strength
        + COUNT_WEIGHT * count_ratio
    )
    return round(score * 100)


def classify_condition(crossing_detected, quality_score):
    if not crossing_detected:
        return "NOT DETECTED"

    if quality_score >= CLEAR_THRESHOLD:
        return "CLEAR"
    elif quality_score >= FADED_THRESHOLD:
        return "FADED"
    else:
        return "DAMAGED / PARTIALLY MISSING"


def normalize_edge_strength(edge_density_value):
    return min(edge_density_value * 5, 1.0)
