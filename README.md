# Zebra Crossing Quality Detector

A desktop Computer Vision application that analyzes a road image and evaluates the visible condition of a zebra (pedestrian) crossing using classical image processing techniques.

## Overview

This project was built as a VITyarthi Computer Vision submission. Given a photo of a road, the application detects whether a zebra crossing is present, counts the visible stripes, and computes a Quality Score (0–100) based on measurable image features. The crossing is finally classified into one of four conditions:

- **CLEAR**
- **FADED**
- **DAMAGED / PARTIALLY MISSING**
- **NOT DETECTED**

The scoring thresholds used in this project are **project-defined for academic purposes only** and are **not** based on any official road-safety standard.

## Features

- Select any road image (JPG/PNG/BMP) from your computer
- Full classical CV pipeline: grayscale conversion, noise removal, contrast enhancement, ROI extraction, thresholding, morphological cleanup, Canny edge detection, Hough Line Transform, and contour-based stripe analysis
- Explainable quality score built from four measurable sub-features (visibility, continuity, edge strength, stripe count)
- Simple Tkinter GUI showing the original image, the processed/edge image, and the detected crossing overlay side by side
- Save the analyzed/overlay image to disk
- Optional local history log (CSV) of every image analyzed
- Handles invalid images and "no crossing found" cases gracefully without crashing

## Technologies Used

- Python 3
- OpenCV (opencv-python)
- NumPy
- Pillow (image display in Tkinter)
- Tkinter (GUI, built into Python)
- Pytest (unit testing)

No deep learning frameworks (YOLO, TensorFlow, PyTorch) are used — this is a purely classical image processing project.

## Installation

1. Make sure Python 3.9+ is installed.
2. Clone or download this project folder.
3. (Recommended) Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      (Windows)
   source venv/bin/activate   (macOS/Linux)
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```
python main.py
```

Steps in the GUI:

1. Click **Select Image** and choose a road photo.
2. Click **Process Image** to run the analysis pipeline.
3. View the Original, Processed/Edge, and Detected Crossing images along with the Stripe Count, Visibility %, Quality Score, and Final Condition.
4. Click **Save Result** to save the overlay image to disk.
5. Click **Reset** to clear the current result and analyze a new image.

Every processed image is also logged to `results/history.csv` with a timestamp.

## Project Structure

```
zebra_crossing_quality_detector/
├── main.py                       Application entry point
├── requirements.txt
├── .gitignore
├── README.md
├── statement.md
├── REPORT.md
├── gui/
│   └── app.py                    Tkinter GUI
├── core/
│   ├── preprocessing.py          Grayscale, noise removal, enhancement, ROI, thresholding
│   ├── edge_detection.py         Canny edges, Hough line transform
│   ├── crossing_detection.py     Contour based stripe detection, overlay drawing
│   ├── quality_analysis.py       Quality score computation, condition classification
│   └── pipeline.py               Orchestrates the full CV pipeline
├── utils/
│   ├── validation.py             Image file validation
│   ├── visualization.py          OpenCV to Tkinter image conversion, saving results
│   └── history.py                Local CSV analysis history
├── tests/                        Pytest unit tests for core and utils modules
├── sample_images/                Place your own test road images here
└── results/                      Saved output images and history.csv (gitignored)
```

## Testing

Unit tests use synthetically generated images so no external dataset is required. Run all tests with:

```
pytest
```

from the project root.

## Screenshots / Results

_Add screenshots of the running application here after testing with your own sample images. This section intentionally left as a placeholder — no fabricated results are included._

| Original | Processed/Edges | Detected Crossing |
|----------|------------------|--------------------|
| (add screenshot) | (add screenshot) | (add screenshot) |

## Limitations

- Designed for reasonably clear, forward-facing road photos where the crossing occupies the lower-middle portion of the frame.
- Performance depends on lighting, camera angle, and image resolution.
- The 0–100 quality score and CLEAR/FADED/DAMAGED thresholds are project-defined heuristics for this coursework, not an official traffic-engineering standard.
