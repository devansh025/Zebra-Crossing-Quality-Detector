# Project Report: Zebra Crossing Quality Detector

## 1. Introduction

Pedestrian safety at road crossings depends heavily on the visibility of the painted zebra crossing markings. Over time, markings fade due to weathering and traffic wear, or get partially erased due to road work, reducing their effectiveness. This project presents a Computer Vision based desktop application that analyzes a photograph of a road and evaluates the visible quality of a zebra crossing using classical image processing techniques, without relying on deep learning models.

## 2. Problem Statement

There is no simple, explainable, low-cost tool that lets a user photograph a crossing and immediately get a quantitative sense of how visible or degraded it is. Manual visual inspection is subjective and not scalable. This project addresses that gap at a small, academic scale using traditional CV methods that are fast, lightweight, and run on ordinary hardware.

## 3. Objectives

- Detect zebra crossings in road images using classical CV techniques.
- Count visible stripes and measure their continuity.
- Compute an explainable, weighted quality score (0–100).
- Classify the crossing as CLEAR, FADED, DAMAGED/PARTIALLY MISSING, or NOT DETECTED.
- Provide a simple, functional desktop GUI for interactive use.
- Ensure the system does not crash on invalid images or images with no crossing.

## 4. Functional Requirements

- FR1: The system shall allow the user to select an image file from local storage.
- FR2: The system shall validate that the selected file is a readable image of sufficient resolution.
- FR3: The system shall preprocess the image (grayscale, denoise, enhance contrast).
- FR4: The system shall detect edges and lines relevant to zebra stripes.
- FR5: The system shall identify and count stripe-like contours.
- FR6: The system shall compute a quality score from visibility, continuity, edge strength, and stripe count.
- FR7: The system shall classify the final condition based on the score and detection status.
- FR8: The system shall display the original, processed/edge, and overlay images in the GUI.
- FR9: The system shall allow saving the overlay result image.
- FR10: The system shall log each analysis to a local history file.

## 5. Non-Functional Requirements

- NFR1: The application must run on a normal student laptop without a GPU.
- NFR2: Dependencies must be minimal and installable via pip (no TensorFlow/PyTorch/YOLO).
- NFR3: The application must not crash on invalid or unreadable images.
- NFR4: Processing a single image should complete within a few seconds on typical hardware.
- NFR5: Code should be organized into clear, single-responsibility modules.

## 6. System Architecture

The system follows a layered architecture:

```
GUI Layer (Tkinter, gui/app.py)
        |
        v
Pipeline Layer (core/pipeline.py)
        |
        v
Core CV Modules (preprocessing -> edge_detection -> crossing_detection -> quality_analysis)
        |
        v
Utility Layer (validation, visualization, history)
```

The GUI depends only on the pipeline's single entry function, `process_image()`, which returns a plain result object. This separation keeps the CV logic independently testable and keeps the GUI code focused purely on presentation.

## 7. Workflow

1. User selects an image through the file dialog.
2. `utils/validation.py` checks the file exists, has a supported extension, is readable by OpenCV, and meets a minimum resolution.
3. `core/preprocessing.py` converts the image to grayscale, removes noise with Gaussian blur, enhances contrast with CLAHE, extracts a Region of Interest (lower-middle portion of the frame), applies Otsu thresholding, and cleans the binary mask with morphological closing/opening.
4. `core/edge_detection.py` runs Canny edge detection on the cleaned mask and applies the Probabilistic Hough Line Transform to find straight line segments.
5. `core/crossing_detection.py` finds contours in the cleaned mask, filters them by area and aspect ratio to identify stripe-shaped blobs, counts horizontal-ish Hough lines, and determines whether a crossing is present.
6. `core/quality_analysis.py` computes four normalized sub-features (visibility, continuity, edge strength, stripe count ratio) and combines them into a weighted 0–100 quality score, then classifies the final condition.
7. `core/pipeline.py` assembles all of the above into a single result object.
8. `gui/app.py` displays the original image, the edge image, and an overlay image with bounding boxes drawn around detected stripes, along with the numeric results.
9. `utils/history.py` appends the result to a local CSV log.

## 8. Design Description (Module Responsibilities)

- **utils/validation.py** — Input Layer. Ensures downstream modules only ever receive a valid OpenCV image.
- **core/preprocessing.py** — Preparation Layer. Normalizes lighting/noise and isolates the road region.
- **core/edge_detection.py** — Feature Extraction Layer. Produces edge and line primitives.
- **core/crossing_detection.py** — Detection Layer. Converts primitives into stripe-level detections and a visual overlay.
- **core/quality_analysis.py** — Scoring Layer. Converts detections into an explainable numeric score and a human-readable condition.
- **core/pipeline.py** — Orchestration Layer. Sequences the layers above and returns one unified result.
- **gui/app.py** — Presentation Layer. Purely handles user interaction and rendering.
- **utils/visualization.py** — Rendering helper for converting OpenCV arrays into Tkinter-displayable images.
- **utils/history.py** — Persistence helper for logging past runs.

A simple sequence per run is: `GUI -> pipeline.process_image() -> validation -> preprocessing -> edge_detection -> crossing_detection -> quality_analysis -> PipelineResult -> GUI display`.

## 9. Computer Vision Techniques Used

- **Grayscale conversion** — reduces the image to a single intensity channel for simpler processing.
- **Noise removal** — Gaussian blur smooths out small sensor noise before thresholding.
- **Image enhancement** — CLAHE (Contrast Limited Adaptive Histogram Equalization) improves local contrast so faded stripes become more distinguishable from the road surface.
- **Region of Interest (ROI)** — restricts analysis to the lower-middle part of the frame where a crossing is expected, reducing false positives from sky, buildings, or vehicles.
- **Thresholding/Segmentation** — Otsu's method automatically separates bright stripe pixels from the darker road background.
- **Morphological operations** — closing joins small gaps in broken stripe segments; opening removes small noise specks.
- **Canny Edge Detection** — highlights strong intensity transitions corresponding to stripe boundaries.
- **Hough Transform** — detects straight line segments consistent with painted stripe edges, used as a secondary signal for crossing detection.
- **Contour/stripe analysis** — extracts individual stripe-shaped blobs from the cleaned mask, used for counting, continuity scoring, and drawing the overlay.

## 10. Quality Scoring Methodology

Four features are computed, each normalized to the 0–1 range:

- **Visibility (weight 0.40)** — proportion of bright pixels inside the ROI relative to an expected stripe coverage baseline.
- **Continuity (weight 0.25)** — fraction of detected stripes whose contour fills a reasonable proportion of their bounding box (i.e. unbroken rather than fragmented).
- **Edge Strength (weight 0.20)** — normalized Canny edge pixel density, reflecting how sharply defined the stripe boundaries are.
- **Stripe Count Ratio (weight 0.15)** — detected stripe count relative to a project-defined expected minimum (4 stripes).

```
quality_score = round(100 * (0.40*visibility + 0.25*continuity + 0.20*edge_strength + 0.15*count_ratio))
```

Condition mapping:

- No crossing detected at all -> **NOT DETECTED**
- Score >= 75 -> **CLEAR**
- 45 <= Score < 75 -> **FADED**
- Score < 45 (crossing present) -> **DAMAGED / PARTIALLY MISSING**

These weights and thresholds are **project-defined choices for this coursework** and are explicitly **not** derived from any official road-safety or traffic-engineering standard.

## 11. Dataset

No fixed external dataset is bundled with this project. The application is designed to work on any user-supplied road photograph placed in the `sample_images/` folder. Unit tests use small synthetically generated images (created directly in code with NumPy/OpenCV) so that the test suite does not depend on any external files. Real-world testing should be performed by the user with their own photographs, and results/screenshots should be added to the README once available.

## 12. Evaluation Methodology

Since no labeled ground-truth dataset of crossing conditions is used, evaluation in this project is primarily:

- **Unit-level correctness** — pytest tests verify that each function behaves correctly on known synthetic inputs (blank images, images with regular stripe patterns, invalid files).
- **Qualitative visual inspection** — running the GUI on sample road photos and manually checking whether the stripe count, overlay boxes, and final condition look reasonable.
- **Robustness checks** — verifying the application does not crash on corrupted files, non-image files, very small images, or images with no visible crossing at all.

No accuracy percentages or benchmark comparisons are reported, as doing so without a real annotated dataset would be fabricated.

## 13. Screenshots / Results

_Placeholder — add screenshots of the GUI, along with example original/processed/overlay images and their computed scores, once you have tested the application on your own sample photos._

## 14. Testing

Pytest-based unit tests are included for:

- Image validation (missing file, unsupported type, too-small image, valid image)
- Preprocessing (grayscale conversion, noise removal, contrast enhancement, ROI extraction)
- Edge detection (Canny output is binary, Hough lines detected on synthetic stripes, no lines on a blank image, edge density is bounded)
- Crossing detection (stripe contours found on a synthetic stripe pattern, none found on a blank mask, crossing detected/not detected logic, overlay image shape)
- Quality analysis (visibility bounds, continuity calculation, count ratio capping, score range, condition classification for all four categories)

Run the full suite with `pytest` from the project root.

## 15. Challenges Faced

- Balancing the ROI so that it reliably captures the crossing region across different camera angles without also being written to fit the images used for testing this specific report.
- Choosing thresholds and weights for the quality score that are reasonable and explainable, given that no official standard exists for this exact scoring scheme.
- Making sure the pipeline degrades gracefully (returns NOT DETECTED rather than crashing) when no stripes are present or the image is very noisy.

## 16. Learnings

- Practical experience combining multiple classical CV techniques (thresholding, morphology, edge detection, Hough transform, contour analysis) into a single coherent pipeline.
- Understanding how to design an explainable scoring system from measurable low-level image features rather than a black-box model.
- Structuring a small desktop application with clear separation between CV logic and GUI presentation for testability.

## 17. Future Enhancements

- Support batch processing of multiple images at once.
- Add perspective transform (bird's-eye view) to normalize stripe geometry regardless of camera angle.
- Allow user-adjustable ROI and thresholds directly from the GUI.
- Build a small labeled dataset to properly evaluate detection accuracy.
- Add GPS/EXIF metadata extraction to tag where each photo was taken.

## 18. References

- OpenCV Documentation, https://docs.opencv.org/
- NumPy Documentation, https://numpy.org/doc/
- Pillow Documentation, https://pillow.readthedocs.io/
- Python Tkinter Documentation, https://docs.python.org/3/library/tkinter.html
- Pytest Documentation, https://docs.pytest.org/
