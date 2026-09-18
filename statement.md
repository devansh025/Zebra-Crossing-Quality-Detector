# Problem Statement

## Problem Statement

Zebra crossings (pedestrian crossings) painted on roads gradually fade or get damaged due to traffic, weather, and lack of repainting. Faded or damaged crossings reduce pedestrian visibility and safety, but there is no simple, low-cost way for a student, municipal worker, or citizen to quickly assess the visible condition of a crossing from a photograph without manual, subjective inspection.

This project builds a Computer Vision based desktop application that takes a photograph of a road and automatically detects the zebra crossing, analyzes its visible stripes, and reports an explainable quality score and condition label.

## Scope

- The project focuses on **visible surface condition** of zebra crossings from a single 2D photograph.
- It uses classical image processing techniques only (no deep learning), keeping it lightweight enough to run on a normal student laptop.
- It is a **decision-support / demonstration tool** for academic purposes, not a certified road-safety inspection system.
- It does not perform real-time video analysis, GPS tagging, or integration with any government database.

## Target Users

- Computer Vision / Image Processing students studying classical CV techniques
- Municipal or civic-tech volunteers who want a quick, low-cost preliminary check of crossing visibility
- Researchers/hobbyists interested in road-infrastructure monitoring using simple, explainable CV pipelines

## Objectives

1. Detect the presence of a zebra crossing in a road image.
2. Count the number of visible stripes.
3. Quantify visibility, continuity, and edge sharpness of the crossing.
4. Compute an explainable 0–100 quality score from these measurable features.
5. Classify the crossing into CLEAR, FADED, DAMAGED/PARTIALLY MISSING, or NOT DETECTED.
6. Present results through a simple, usable desktop GUI.
7. Handle invalid input and "no crossing found" scenarios without crashing.

## High-Level Features

- Image selection and validation
- Full classical CV processing pipeline (grayscale, denoising, enhancement, ROI, thresholding, morphology, Canny edges, Hough transform, contour analysis)
- Explainable, weighted quality scoring formula
- Three-panel visual result display (original, processed/edge, detected overlay)
- Save-to-disk functionality for results
- Optional local history log of past analyses
- Unit-tested core logic
