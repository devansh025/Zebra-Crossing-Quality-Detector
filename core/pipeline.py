from utils import validation
from core import preprocessing
from core import edge_detection
from core import crossing_detection
from core import quality_analysis


class PipelineResult:
    def __init__(self):
        self.success = False
        self.message = ""
        self.original_image = None
        self.edge_image = None
        self.overlay_image = None
        self.stripe_count = 0
        self.visibility_percent = 0
        self.quality_score = 0
        self.condition = "NOT DETECTED"


def process_image(file_path):
    result = PipelineResult()

    image, message = validation.load_and_validate_image(file_path)
    if image is None:
        result.success = False
        result.message = message
        return result

    pre = preprocessing.preprocess_image(image)

    edges = edge_detection.detect_edges(pre["cleaned"])
    lines = edge_detection.detect_hough_lines(edges)
    horizontal_line_count = crossing_detection.count_horizontal_lines(lines)

    stripe_boxes = crossing_detection.find_stripe_contours(pre["cleaned"])
    stripe_count = len(stripe_boxes)

    crossing_found = crossing_detection.is_crossing_detected(stripe_boxes, horizontal_line_count)

    visibility = quality_analysis.calculate_visibility(pre["cleaned"])
    continuity = quality_analysis.calculate_continuity(stripe_boxes)
    density = edge_detection.edge_density(edges)
    edge_strength = quality_analysis.normalize_edge_strength(density)
    count_ratio = quality_analysis.calculate_count_ratio(stripe_count)

    quality_score = quality_analysis.calculate_quality_score(
        visibility, continuity, edge_strength, count_ratio
    )

    condition = quality_analysis.classify_condition(crossing_found, quality_score)

    overlay = crossing_detection.build_overlay(image, stripe_boxes, pre["roi_top"])

    result.success = True
    result.message = "OK"
    result.original_image = image
    result.edge_image = edges
    result.overlay_image = overlay
    result.stripe_count = stripe_count
    result.visibility_percent = round(visibility * 100)
    result.quality_score = quality_score
    result.condition = condition

    return result
